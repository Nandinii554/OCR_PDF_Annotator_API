# OCR PDF Annotator with FastAPI, Tesseract, and PyMuPDF

This project is a containerized web service built using **FastAPI** that performs **Optical Character Recognition (OCR)** on PDF documents. It uses **Tesseract OCR** to extract text and **PyMuPDF** to draw bounding boxes around recognized text directly on the original PDF.

---

OCR has become a critical tool in document digitization, automation, and data extraction. However, raw OCR text often lacks visual context, which makes validation and auditing harder. This project provides a solution to:

- Visually **verify OCR accuracy** with bounding boxes
- Retain **PDF structure and layout**
- Make extracted data usable via **structured JSON**

---

## What This App Does

- Accepts PDF files via a web API
- Converts each PDF page into a high-resolution image
- Runs Tesseract OCR on each page image
- Extracts:
  - text
  - bounding box coordinates
  - confidence score
- Maps image coordinates to original PDF coordinates (scaling)
- Draws bounding boxes on the original PDF using PyMuPDF
- Returns:
  - Annotated PDF with visual text markers
  - OCR results as structured JSON

---

- **Frontend**: Swagger UI via FastAPI
- **Backend**: FastAPI + Tesseract OCR + PyMuPDF
- **Storage**: Temporary file system for generated annotated PDFs

---

## 🔄 OCR Workflow (Internals)

1. **PDF Upload**: The user uploads a `.pdf` file via the `/extract` endpoint.
2. **Image Conversion**: Each page is rasterized at 300 DPI using `pdf2image`, creating pixel-perfect images.
3. **Text Detection**: `pytesseract` runs OCR on each image and returns:
   - Recognized text
   - Bounding box: `(left, top, width, height)`
   - Confidence score
4. **Coordinate Scaling**: Image-based coordinates are scaled to match the PDF's point system (1 point = 1/72 inch).
5. **Annotation**: Rectangles are drawn over the text regions using PyMuPDF’s `draw_rect()` function.
6. **Output**:
   - The annotated PDF is saved temporarily
   - A JSON response includes a download link and structured text

---


## Technologies Used

| Tool         | Purpose                                          |
|--------------|--------------------------------------------------|
| **FastAPI**  | Web framework with built-in Swagger UI           |
| **Tesseract**| OCR engine to extract text from image            |
| **pdf2image**| Converts PDF pages into high-resolution images   |
| **PyMuPDF**  | Edits and annotates the original PDF             |
| **Pillow**   | Image object manipulation                        |
| **Docker**   | Ensures consistent environment across systems    |

---

## ✨ Features

- 🔄 OCR on multi-page PDFs
- 📐 Accurate coordinate scaling for annotations
- 📄 Annotated PDF download
-  Returns structured JSON (text, confidence, positions)
- 📦 Docker-ready for deployment
- ⚙️ Interactive Swagger UI

---
