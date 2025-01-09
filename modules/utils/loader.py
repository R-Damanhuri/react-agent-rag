# from langchain_core.document_loaders import BaseLoader
# from docling.document_converter import DocumentConverter

# class DoclingPDFLoader(BaseLoader):

#     def __init__(self, file_path: str | list[str]) -> None:
#         self._file_paths = file_path if isinstance(file_path, list) else [file_path]
#         self._converter = DocumentConverter()

#     def lazy_load(self):
#         for source in self._file_paths:
#             dl_doc = self._converter.convert(source).document
#             text = dl_doc.export_to_markdown()
#             yield text

from typing import Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from docling.document_converter import DocumentConverter
from docling.utils.export import generate_multimodal_pages


class DoclingPDFLoader(BaseLoader):

    def __init__(self, file_path: str | list[str]) -> None:
        self._file_paths = file_path if isinstance(file_path, list) else [file_path]
        self._converter = DocumentConverter()

    def lazy_load(self) -> Iterator[Document]:
        for source in self._file_paths:
            conv_res = self._converter.convert(source)
            for (content_text, content_md, content_dt, page_cells, page_segments, page) in generate_multimodal_pages(conv_res):
                yield Document(page_content=content_md, metadata={"source": conv_res.input.file.name, "page_no": page.page_no})