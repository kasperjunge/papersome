import os
import typer
import requests
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.document_loaders import PDFMinerLoader, PagedPDFSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

load_dotenv()  # load environment variables from .env file


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


def main(url: str, chain_type: str = "map_reduce"):
    """Downloads a PDF from a given URL, summarizes it, and saves the summary to a file.

    Args:
        url: The URL of the PDF to summarize.
        chain_type: The type of summarization chain to use.
    """
    filename = download_pdf(url)
    summary = summarize_pdf(filename, chain_type)

    print(summary)

    with open(filename.replace("pdfs", "summaries"), "w") as f:
        f.write(summary)


if __name__ == "__main__":
    typer.run(main)
