from pathlib import Path

import requests
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PagedPDFSplitter


def download_pdf(url: str) -> Path:
    """Downloads a PDF from a given URL and saves it to a local file.

    Args:
        url: The URL of the PDF to download.

    Returns:
        The path to the downloaded PDF file.
    """
    out_dir = Path("pdfs")
    out_dir.mkdir(exist_ok=True)

    filename = out_dir / f"{url.split('/')[-1]}.pdf"
    if not filename.is_file():  # download the file if it doesn't exist locally
        if "arxiv.org/abs/" not in url:
            raise ValueError(f"URL {url} is not an arXiv URL.")

        pdf_url = url.replace("abs", "pdf") + ".pdf"
        response = requests.get(pdf_url)
        with filename.open("wb") as f:
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
