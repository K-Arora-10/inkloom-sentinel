import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF
import docx

def extract_sentences_with_offsets(text: str) -> List[Dict[str, Any]]:
    """
    Extracts sentences while preserving start and end character offsets.
    Handles standard sentence delimiters (. ! ? and newlines) reliably.
    """
    sentences = []
    # Pattern to find sentence bounds while respecting punctuation
    pattern = re.compile(r'([^\.\!\?\n]+[\.\!\?]*|\n+)', re.MULTILINE)
    
    current_idx = 0
    raw_sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
    
    pos = 0
    for s in raw_sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        start = text.find(s_clean, pos)
        if start == -1:
            start = pos
        end = start + len(s_clean)
        pos = end
        sentences.append({
            "text": s_clean,
            "start_char": start,
            "end_char": end,
            "index": len(sentences)
        })
        
    if not sentences and text.strip():
        sentences.append({
            "text": text.strip(),
            "start_char": 0,
            "end_char": len(text.strip()),
            "index": 0
        })
        
    return sentences


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts clean readable text from PDF documents using PyMuPDF.
    """
    doc = fitz.open(file_path)
    text_parts = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_parts.append(page.get_text("text"))
    doc.close()
    return "\n\n".join(text_parts).strip()


def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from DOCX files using python-docx.
    """
    doc = docx.Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs).strip()


def extract_content(file_path: str, filename: str) -> Tuple[str, str]:
    """
    Dispatches file extraction based on extension.
    Returns (extracted_text, file_format)
    """
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path), "PDF"
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path), "DOCX"
    elif ext in [".txt", ".md"]:
        text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        return text, "PLAIN_TEXT"
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats are PDF, DOCX, TXT, MD.")
