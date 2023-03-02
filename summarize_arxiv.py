import sys

sys.path.append("./src")
import typer
from dotenv import load_dotenv
from papersome.pdf import download_pdf, summarize_pdf

load_dotenv()  # load environment variables from .env file


def main(url: str, chain_type: str = "map_reduce"):
    """Downloads a PDF from a given URL, summarizes it, and saves the summary to a file.

    Args:
        url: The URL of the PDF to summarize.
        chain_type: The type of summarization chain to use.
    """
    filename = download_pdf(url)
    summary = summarize_pdf(filename, chain_type)

    print(summary)

    with open(filename.replace("pdfs", "summaries").replace(".pdf", ".txt"), "w") as f:
        f.write(summary)


if __name__ == "__main__":
    typer.run(main)
