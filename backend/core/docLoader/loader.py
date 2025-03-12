from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, TextSplitter

# file_path = "./test1.pdf"
# loader = PyMuPDF4LLMLoader(file_path, extract_images=False, images_parser=TesseractBlobParser(), table_strategy="lines")
# docs = loader.load()
# print(docs)
