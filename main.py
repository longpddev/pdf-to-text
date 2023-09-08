from typing import Annotated, IO, Union
import ocrmypdf
import os
from fastapi import FastAPI, File, Form, UploadFile
from PyPDF2 import PdfReader
from uuid import uuid1
from pathlib import Path

app = FastAPI()

def pdfToString(fileOrPath: Union[IO, Path]):
    reader = PdfReader(fileOrPath)
    return "\n".join([page.extract_text() for page in reader.pages])

def loadTextFromPDF(path: str):
    if not (os.path.exists(path)):
        raise ValueError(f"file: {path} does not exit")
    result = pdfToString(path)
    os.remove(path)
    return result

@app.post("/files/")
async def create_file(
    file: Annotated[UploadFile, File()],
    ocr: Annotated[bool, Form()]
):
    tmpFile = 'tmp/' + uuid1().hex
    content: str
    
    if(ocr):
        ocrmypdf.ocr(file.file, tmpFile, skip_text=True)
        content = loadTextFromPDF(tmpFile)
    else:
        content = pdfToString(file.file)

    return {
        "result": content
    }