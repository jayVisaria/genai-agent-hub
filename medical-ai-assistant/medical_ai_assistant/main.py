from fastapi import FastAPI, File, UploadFile, Form
from typing import List, Optional
import pydicom
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

app = FastAPI()

def process_dicom(file_bytes: bytes):
    """Processes a DICOM file and extracts relevant information."""
    try:
        ds = pydicom.dcmread(io.BytesIO(file_bytes))
        # Extract relevant information from the DICOM file
        return {"patient_id": ds.PatientID, "study_description": ds.StudyDescription}
    except Exception as e:
        return {"error": f"Failed to process DICOM file: {e}"}

def ocr_image(file_bytes: bytes):
    """Performs OCR on an image and extracts text."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return {"text": text}
    except Exception as e:
        return {"error": f"Failed to perform OCR on image: {e}"}

def ocr_pdf(file_bytes: bytes):
    """Performs OCR on a PDF and extracts text."""
    try:
        images = convert_from_bytes(file_bytes)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return {"text": text}
    except Exception as e:
        return {"error": f"Failed to perform OCR on PDF: {e}"}

@app.post("/analyze/text")
async def analyze_text(text: str = Form(...)):
    """Analyzes a text input."""
    return {"status": "text received", "text": text}

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyzes an image input (including DICOM)."""
    contents = await file.read()
    if file.content_type == "application/dicom":
        result = process_dicom(contents)
    else:
        result = ocr_image(contents)
    return {"filename": file.filename, "content_type": file.content_type, "result": result}

@app.post("/analyze/document")
async def analyze_document(file: UploadFile = File(...)):
    """Analyzes a document input (PDF)."""
    contents = await file.read()
    if file.content_type == "application/pdf":
        result = ocr_pdf(contents)
    else:
        result = {"error": "Unsupported document type"}
    return {"filename": file.filename, "content_type": file.content_type, "result": result}

@app.post("/analyze/multi")
