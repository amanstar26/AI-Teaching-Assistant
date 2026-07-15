import fitz
import io

from PIL import Image
from rapidocr_onnxruntime import RapidOCR

from langchain_text_splitters import (
RecursiveCharacterTextSplitter
)

ocr_engine = RapidOCR()

def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        print(
            f"Processing PDF with {len(doc)} pages..."
        )

        for page_num, page in enumerate(doc):

            page_text = page.get_text().strip()

            if len(page_text) > 50:

                print(
                    f"Page {page_num+1}: Text layer found"
                )

                text += page_text + "\n"

            else:

                print(
                    f"Page {page_num+1}: Running OCR..."
                )

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2)
                )

                image_bytes = pix.tobytes("png")

                image = Image.open(
                    io.BytesIO(image_bytes)
                )

                result, _ = ocr_engine(
                    image
                )

                ocr_text = ""

                if result:

                    for item in result:

                        ocr_text += (
                            item[1]
                            + "\n"
                        )

                text += ocr_text + "\n"

        doc.close()

        print(
            f"Total Extracted Characters: {len(text)}"
        )

        return text

    except Exception as e:

        print(
            f"Error reading PDF: {e}"
        )

        return None

def chunk_text(text,chunk_size=500):

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=100
        )
    )

    chunks = splitter.split_text(
        text
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    return chunks
