from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import io
import os
import uuid

# Tesseract & Poppler paths (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = "/opt/anaconda3/envs/ocr-env/bin/tesseract"
POPPLER_PATH = "/opt/anaconda3/envs/ocr-env/bin"

app = FastAPI(
    title="OCR PDF Annotator",
    version="1.1",
    description="Upload a PDF and get back a version with bounding boxes drawn over recognized text (properly scaled)."
)

@app.post("/extract", summary="Extract and visualize text on PDF", tags=["OCR"])
async def extract_and_visualize(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})

    try:
        # Step 1: Load the original PDF
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Step 2: Convert PDF to images for OCR
        dpi = 300
        images = convert_from_bytes(pdf_bytes, dpi=dpi, poppler_path=POPPLER_PATH)

        # Step 3: Annotate each page with scaled boxes
        for page_index, image in enumerate(images):
            page = doc[page_index]

            # OCR the image
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            # Get image and PDF sizes
            img_width, img_height = image.size
            pdf_width, pdf_height = page.rect.width, page.rect.height

            # Calculate scale from image (pixels) to PDF (points)
            scale_x = pdf_width / img_width
            scale_y = pdf_height / img_height

            for i in range(len(ocr_data["text"])):
                text = ocr_data["text"][i].strip()
                conf = int(ocr_data["conf"][i])
                if text and conf > 60:
                    x = ocr_data["left"][i]
                    y = ocr_data["top"][i]
                    w = ocr_data["width"][i]
                    h = ocr_data["height"][i]

                    # Scale image coordinates to PDF coordinates
                    rect = fitz.Rect(
                        x * scale_x,
                        y * scale_y,
                        (x + w) * scale_x,
                        (y + h) * scale_y
                    )
                    # Draw the bounding box on the PDF
                    page.draw_rect(rect, color=(1, 0, 0), width=0.8)

        # Step 4: Save and return the annotated PDF
        output_path = f"annotated_{uuid.uuid4().hex}.pdf"
        doc.save(output_path)
        doc.close()

        return FileResponse(
            path=output_path,
            filename="annotated.pdf",
            media_type="application/pdf"
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
