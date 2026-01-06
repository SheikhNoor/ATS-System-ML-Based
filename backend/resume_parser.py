"""
Resume Parser Module
Handles PDF and DOCX file uploads and extracts clean text from resumes.
"""

import io
import re
import os
from typing import Optional, Dict, Any
import pdfplumber
from docx import Document
from fastapi import UploadFile, HTTPException
try:
    from pdf2image import convert_from_bytes
    import pytesseract
    
    # Configure Tesseract and Poppler paths
    if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # Check for poppler in user directory
    poppler_path = None
    user_poppler = os.path.join(os.path.expanduser("~"), "poppler", "poppler-24.08.0", "Library", "bin")
    if os.path.exists(user_poppler):
        poppler_path = user_poppler
    
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    poppler_path = None


class ResumeParser:
    """
    A class to parse resume files (PDF and DOCX) and extract clean text.
    """

    def __init__(self):
        """Initialize the ResumeParser."""
        self.supported_formats = ['.pdf', '.docx']

    def parse_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Main method to parse uploaded resume file.

        Args:
            file (UploadFile): The uploaded resume file

        Returns:
            Dict[str, Any]: Dictionary containing extracted text and metadata

        Raises:
            HTTPException: If file format is unsupported or parsing fails
        """
        try:
            # Validate file format
            filename = file.filename.lower()
            file_extension = self._get_file_extension(filename)

            if file_extension not in self.supported_formats:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}"
                )

            # Read file content
            file_content = file.file.read()
            file.file.seek(0)  # Reset file pointer for potential re-reads

            # Parse based on file type
            if file_extension == '.pdf':
                extracted_text = self._parse_pdf(file_content)
            elif file_extension == '.docx':
                extracted_text = self._parse_docx(file_content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="File format not recognized"
                )

            # Clean the extracted text
            cleaned_text = self._clean_text(extracted_text)

            if not cleaned_text or len(cleaned_text.strip()) < 50:
                raise HTTPException(
                    status_code=400,
                    detail="Unable to extract sufficient text from the resume. Please ensure the file is not corrupted or empty."
                )

            return {
                "filename": file.filename,
                "file_type": file_extension,
                "raw_text": extracted_text,
                "cleaned_text": cleaned_text,
                "character_count": len(cleaned_text),
                "word_count": len(cleaned_text.split())
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error parsing resume: {str(e)}"
            )

    def _get_file_extension(self, filename: str) -> str:
        """
        Extract file extension from filename.

        Args:
            filename (str): The filename

        Returns:
            str: File extension with dot (e.g., '.pdf')
        """
        if '.' not in filename:
            return ''
        return '.' + filename.rsplit('.', 1)[1].lower()

    def _parse_pdf(self, file_content: bytes) -> str:
        """
        Parse PDF file and extract text.

        Args:
            file_content (bytes): PDF file content

        Returns:
            str: Extracted text from PDF

        Raises:
            Exception: If PDF parsing fails
        """
        try:
            text_content = []
            pdf_file = io.BytesIO(file_content)

            with pdfplumber.open(pdf_file) as pdf:
                if len(pdf.pages) == 0:
                    raise Exception("PDF file has no pages")

                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)

            extracted_text = '\n'.join(text_content)

            # If no text extracted, try OCR for image-based PDFs
            if not extracted_text.strip():
                if OCR_AVAILABLE:
                    try:
                        # Convert PDF to images and use OCR
                        if poppler_path:
                            images = convert_from_bytes(file_content, poppler_path=poppler_path)
                        else:
                            images = convert_from_bytes(file_content)
                        
                        ocr_text = []
                        for image in images:
                            page_text = pytesseract.image_to_string(image)
                            if page_text.strip():
                                ocr_text.append(page_text)
                        
                        extracted_text = '\n'.join(ocr_text)
                        
                        if not extracted_text.strip():
                            raise Exception("No text could be extracted from PDF (OCR returned empty)")
                    except Exception as ocr_error:
                        raise Exception(f"Image-based PDF detected. OCR processing failed: {str(ocr_error)}")
                else:
                    raise Exception(
                        "Cannot extract text from this PDF. This is likely an image-based (scanned) PDF. "
                        "Please try one of these solutions:\\n\\n"
                        "✓ RECOMMENDED: Upload your resume as a DOCX file instead\\n"
                        "✓ Convert the PDF to a text-based format using Adobe Acrobat or online tools\\n"
                        "✓ Copy text from the PDF and paste into a Word document, then save as DOCX\\n\\n"
                        "Note: Image-based PDF support requires Tesseract OCR and Poppler (advanced setup)"
                    )

            return extracted_text

        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")

    def _parse_docx(self, file_content: bytes) -> str:
        """
        Parse DOCX file and extract text.

        Args:
            file_content (bytes): DOCX file content

        Returns:
            str: Extracted text from DOCX

        Raises:
            Exception: If DOCX parsing fails
        """
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)

            # Extract text from paragraphs
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

            # Extract text from tables
            table_text = []
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        table_text.append(' | '.join(row_text))

            # Combine all text
            all_text = paragraphs + table_text
            extracted_text = '\n'.join(all_text)

            if not extracted_text.strip():
                raise Exception("No text could be extracted from DOCX")

            return extracted_text

        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.

        Args:
            text (str): Raw extracted text

        Returns:
            str: Cleaned text
        """
        if not text:
            return ""

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\@\+\(\)\#\&\/]', '', text)

        # Remove multiple consecutive dots
        text = re.sub(r'\.{2,}', '.', text)

        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def extract_email(self, text: str) -> Optional[str]:
        """
        Extract email address from text.

        Args:
            text (str): Text to search

        Returns:
            Optional[str]: Email address if found, None otherwise
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        """
        Extract phone number from text.

        Args:
            text (str): Text to search

        Returns:
            Optional[str]: Phone number if found, None otherwise
        """
        # Pattern for various phone formats
        phone_patterns = [
            r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',  # US format
            r'\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}',  # International
        ]

        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        return None
