import io

import PyPDF2
import requests


def download_pdf(url):
    """
    Download a PDF from a given URL.

    Args:
    url (str): URL of the PDF file.

    Returns:
    BytesIO: In-memory binary stream of the PDF file.
    """
    response = requests.get(url)
    response.raise_for_status()
    return io.BytesIO(response.content)


def extract_text_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream.

    Args:
    file_stream (io.BytesIO): The binary stream of the PDF document.

    Returns:
    str: The extracted text from the PDF.
    """
    text = ""
    pdf_reader = PyPDF2.PdfReader(file_stream)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def get_arxiv_paper_text(url):
    """
    Extracts text from an arXiv paper given its URL.

    Args:
    url (str): The URL of the arXiv paper, either an abstract or PDF link.

    Returns:
    str: The extracted text from the arXiv paper.
    """
    # Check if the URL is for an abstract or direct PDF
    if "abs" in url:
        url = url.replace("abs", "pdf") + ".pdf"

    try:
        pdf_stream = download_pdf(url)
        return extract_text_from_pdf(pdf_stream)
    except Exception as e:
        return str(e)
