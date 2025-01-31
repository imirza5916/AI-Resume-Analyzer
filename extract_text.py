import fitz  # PyMuPDF for PDFs
import docx
import os

def extract_text_from_file(file):
    """Extract text from a PDF or DOCX file."""

    # Ensure we are dealing with an uploaded file (not just a file path)
    if hasattr(file, "filename"):  # It's an uploaded file
        filename = file.filename.lower()
        file_path = os.path.join("uploads", filename)
        file.save(file_path)  # Save the uploaded file temporarily
    else:  # It's a file path string
        filename = file.lower()
        file_path = file

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()