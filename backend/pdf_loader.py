
from pypdf import PdfReader
import os

def load_text_from_file(file_path):
    """
    Reads text content from either a PDF or a TXT file based on extension.
    This function replaces the old load_pdf_text.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if file_extension == ".pdf":
        try:
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " \n " 
            return text
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ""
            
    elif file_extension == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return ""
            
    else:
        print(f"Error: Unsupported file type: {file_extension}")
        return ""


def split_into_chunks(text, chunk_size=100, overlap=10):
    """
    Splits text into focused chunks of roughly 100 words with 10 words overlap.
    This optimization is crucial for accurate RAG retrieval.
    """
    words = text.split()
    chunks = []
    
    step = chunk_size - overlap
    
    if step <= 0:
        step = chunk_size 
    
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks
