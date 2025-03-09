from mistralai import Mistral, DocumentURLChunk, ImageURLChunk, TextChunk
from mistralai.models import OCRResponse
from IPython.display import Markdown, display
from pathlib import Path
import json
import pandoc
import os 
import argparse
import dotenv

def init_mistral_client():
    """Initialise le client Mistral avec la clé API."""
    dotenv.load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if api_key is None:
        raise ValueError("Please set the MISTRAL_API_KEY environment variable.")
    return Mistral(api_key=api_key)

def process_pdf_file(pdf_path: str | Path) -> OCRResponse:
    """Traite un fichier PDF et retourne la réponse OCR."""
    pdf_file = Path(pdf_path)
    if not pdf_file.is_file():
        raise FileNotFoundError(f"File not found: {pdf_file}")

    client = init_mistral_client()
    
    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    return client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url), 
        model="mistral-ocr-latest", 
        include_image_base64=True
    )

def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    """Remplace les références d'images dans le markdown par leur contenu base64."""
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})")
    return markdown_str

def get_combined_markdown(ocr_response: OCRResponse) -> str:
    """Combine le markdown de toutes les pages avec les images."""
    markdowns: list[str] = []
    for page in ocr_response.pages:
        image_data = {img.id: img.image_base64 for img in page.images}
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))
    return "\n\n".join(markdowns)

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown using Mistral OCR")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output markdown file path")
    args = parser.parse_args()

    try:
        ocr_response = process_pdf_file(args.pdf_path)
        markdown_content = get_combined_markdown(ocr_response)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Markdown saved to: {args.output}")
        else:
            print(markdown_content)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())