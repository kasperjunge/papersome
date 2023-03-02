import os
import requests
from langchain import OpenAI
from langchain.document_loaders import PDFMinerLoader, PagedPDFSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain


def download_pdf(url: str) -> str:
    """Downloads a PDF from a given URL and saves it to a local file.

    Args:
        url: The URL of the PDF to download.

    Returns:
        The path to the downloaded PDF file.
    """
    filename = f"./pdfs/{url.split('/')[-1]}.pdf"
    if not os.path.isfile(filename):  # download the file if it doesn't exist locally
        if "arxiv.org/abs/" not in url:
            raise ValueError(f"URL {url} is not an arXiv URL.")

        pdf_url = url.replace("abs", "pdf") + ".pdf"
        response = requests.get(pdf_url)
        with open(filename, "wb") as f:
            f.write(response.content)

    return filename


def summarize_pdf(filename: str, chain_type: str = "map_reduce") -> str:
    """Summarizes a PDF file using LangChain's summarization chain.

    Args:
        filename: The path to the PDF file to summarize.
        chain_type: The type of summarization chain to use.

    Returns:
        The summary of the PDF.
    """
    loader = PagedPDFSplitter(filename)
    pages = loader.load_and_split()

    chain = load_summarize_chain(llm=OpenAI(temperature=0), chain_type=chain_type)
    summary = chain.run(pages)

    return summary
