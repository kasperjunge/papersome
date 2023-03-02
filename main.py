import typer
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.document_loaders import PDFMinerLoader
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

from langchain.document_loaders import PagedPDFSplitter

load_dotenv()

# point at url?


def main(path: str, chain_type: str = "map_reduce"):

    loader = PagedPDFSplitter(path)
    pages = loader.load_and_split()

    chain = load_summarize_chain(
        llm=OpenAI(temperature=0),
        chain_type=chain_type,
    )

    summary = chain.run(pages)

    return summary


if __name__ == "__main__":
    typer.run(main)
