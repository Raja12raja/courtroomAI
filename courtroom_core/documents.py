"""PDF and image evidence ingestion (text, OCR, vision)."""
import base64
import io
import re

import PyPDF2
import pytesseract
from PIL import Image

from courtroom_core.llm import get_client
from courtroom_core.locales import get_language_instruction, get_translation

def extract_pdf_text(pdf_file, language: str = "en") -> str:
    """
    Extract text from an uploaded PDF file.
    PDFs are treated as TEXT-ONLY documents (no OCR, no image extraction).
    """
    try:
        # Reset file pointer
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        # Extract text using PyPDF2
        pdf_file.seek(0)
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        
        all_text = []
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                page_label = get_translation("page", language)
                all_text.append(f"[{page_label} {page_num + 1}]\n{page_text}")
        
        if not all_text:
            return f"[{get_translation('no_text_pdf', language)}]"
        
        return "\n\n".join(all_text).strip()
    
    except Exception as e:
        return f"[{get_translation('error_pdf', language)}: {str(e)}]"


def image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL Image to base64 string for vision model.
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def describe_image_with_vision(image: Image.Image, language: str = "en") -> str:
    """
    Use a vision model to describe what's in the image.
    Identifies objects, scenes, people, actions, and context.
    """
    try:
        # Convert image to base64
        img_base64 = image_to_base64(image)
        
        # Try using multimodal LLM endpoint
        client = get_client()
        
        lang_instruction = get_language_instruction(language)
        
        # Build vision prompt
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You are an expert forensic image analyst for legal evidence. 
Analyze this image and provide a detailed description of:
1. What objects/items are visible
2. Any people (without identifying them - describe appearance, actions, positions)
3. The scene/location (indoor/outdoor, type of place)
4. Any actions or events taking place
5. Relevant details for legal evidence (timestamps, quality, clarity)
6. Any notable features or anomalies

Be objective, factual, and detailed. Format as a structured evidence description.{lang_instruction}"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ]
        
        # Try calling vision-capable endpoint
        try:
            response = client.predict(
                endpoint="databricks-llama-4-maverick",
                inputs={"messages": messages}
            )
            
            if isinstance(response, dict) and "choices" in response:
                description = response["choices"][0]["message"]["content"].strip()
                return description
            else:
                return str(response).strip()
        
        except Exception as vision_error:
            # If vision endpoint fails, try a simpler text-based approach
            # This is a fallback - may not work as well
            vision_unavail = get_translation("vision_unavailable", language)
            manual_review = get_translation("manual_review", language)
            return f"[{vision_unavail}: {str(vision_error)}. {manual_review}.]"
    
    except Exception as e:
        return f"[{get_translation('error_vision', language)}: {str(e)}]"


def extract_text_from_image(image: Image.Image, language: str = "en") -> str:
    """
    Extract text from an image using OCR (Tesseract).
    """
    try:
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()
    except Exception as e:
        return f"[{get_translation('error_ocr', language)}: {str(e)}]"


def process_image_file(image_file, language: str = "en") -> str:
    """
    Process an uploaded image file.
    
    Does TWO things:
    1. OCR: Extract any text present in the image
    2. Vision: Describe what objects/scenes/people are visible
    
    This handles both text-containing images (screenshots, documents) 
    and non-text images (photos, CCTV, diagrams).
    """
    try:
        # Reset file pointer
        image_file.seek(0)
        image_bytes = image_file.read()
        
        # Open image with PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        result_parts = []
        
        # Part 1: Try OCR for text extraction
        ocr_text = extract_text_from_image(image, language)
        
        if ocr_text and not ocr_text.startswith("["):
            ocr_label = get_translation("ocr_extracted", language)
            result_parts.append(f"[{ocr_label}]\n{ocr_text}")
        elif ocr_text.startswith("["):
            ocr_status = get_translation("ocr_status", language)
            result_parts.append(f"[{ocr_status}: {ocr_text}]")
        else:
            result_parts.append(f"[{get_translation('no_text_image', language)}]")
        
        # Part 2: Describe image content using vision model
        image_description = describe_image_with_vision(image, language)
        
        if image_description and not image_description.startswith("["):
            visual_label = get_translation("visual_analysis", language)
            result_parts.append(f"\n[{visual_label}]\n{image_description}")
        elif image_description.startswith("["):
            result_parts.append(f"\n{image_description}")
        
        # Combine both analyses
        if not result_parts:
            return f"[{get_translation('unable_process', language)}]"
        
        return "\n".join(result_parts)
    
    except Exception as e:
        return f"[{get_translation('error_image', language)}: {str(e)}]"


def process_evidence_file(file, language: str = "en") -> str:
    """
    Process an uploaded evidence file (PDF or image).
    
    - PDFs: Extract text only (no OCR, no images)
    - Images: Extract text (OCR) + Describe visual content (Vision)
    """
    filename = file.name.lower()
    
    # Check file extension
    if filename.endswith('.pdf'):
        return extract_pdf_text(file, language)
    elif filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')):
        return process_image_file(file, language)
    else:
        return f"[{get_translation('unsupported_file', language)}: {filename}]"

