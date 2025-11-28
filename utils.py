import PyPDF2

def extract_text_from_pdf(file):
    """
    Takes a PDF file object (uploaded from Streamlit)
    and returns all text as a single string.
    """
    reader = PyPDF2.PdfReader(file)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)
