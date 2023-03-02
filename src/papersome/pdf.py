from pypdf import PdfReader


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    return text
