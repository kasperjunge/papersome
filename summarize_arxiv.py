import sys

sys.path.append("./src")

from pathlib import Path

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
    summary = summarize_pdf(filename.as_posix(), chain_type)

    print(summary)

    summary_dir = Path("summaries")
    summary_dir.mkdir(exist_ok=True)

    summary_file = summary_dir / (filename.with_suffix(".txt").name)
    summary_file.write_text(summary)


if __name__ == "__main__":
    typer.run(main)
