import pickle
import faiss
import re
import json
import mlflow.deployments
from sentence_transformers import SentenceTransformer
import PyPDF2
import io
from PIL import Image
import pytesseract
import base64
import math

# ─────────────────────────────────────────────
# MULTI-LANGUAGE SUPPORT
# ─────────────────────────────────────────────

TRANSLATIONS = {
    "en": {
        "page": "Page",
        "no_text_pdf": "No text found in PDF",
        "error_pdf": "Error processing PDF",
        "ocr_extracted": "Text Extracted via OCR",
        "ocr_status": "OCR Status",
        "no_text_image": "No readable text found in image",
        "visual_analysis": "Visual Content Analysis",
        "error_image": "Error processing image",
        "unable_process": "Unable to process image - no text or visual content extracted",
        "error_ocr": "Error in OCR",
        "error_vision": "Error in vision analysis",
        "vision_unavailable": "Vision analysis unavailable",
        "manual_review": "Manual review required",
        "unsupported_file": "Unsupported file type",
        "evidence_doc": "Evidence Document",
        "credibility_score": "Credibility Score",
        "relevance": "Relevance",
        "red_flags": "Red Flags",
        "none": "None",
        "recommendations": "Recommendations",
        "round": "Round",
        "defense": "Defense",
        "prosecution": "Prosecution"
    },
    "hi": {
        "page": "पृष्ठ",
        "no_text_pdf": "पीडीएफ में कोई टेक्स्ट नहीं मिला",
        "error_pdf": "पीडीएफ प्रोसेसिंग में त्रुटि",
        "ocr_extracted": "OCR द्वारा टेक्स्ट निकाला गया",
        "ocr_status": "OCR स्थिति",
        "no_text_image": "छवि में कोई पठनीय टेक्स्ट नहीं मिला",
        "visual_analysis": "दृश्य सामग्री विश्लेषण",
        "error_image": "छवि प्रोसेसिंग में त्रुटि",
        "unable_process": "छवि प्रोसेस करने में असमर्थ - कोई टेक्स्ट या दृश्य सामग्री निकाली नहीं गई",
        "error_ocr": "OCR में त्रुटि",
        "error_vision": "दृश्य विश्लेषण में त्रुटि",
        "vision_unavailable": "दृश्य विश्लेषण उपलब्ध नहीं",
        "manual_review": "मैनुअल समीक्षा आवश्यक",
        "unsupported_file": "असमर्थित फ़ाइल प्रकार",
        "evidence_doc": "साक्ष्य दस्तावेज़",
        "credibility_score": "विश्वसनीयता स्कोर",
        "relevance": "प्रासंगिकता",
        "red_flags": "चेतावनी संकेत",
        "none": "कोई नहीं",
        "recommendations": "सिफारिशें",
        "round": "दौर",
        "defense": "बचाव पक्ष",
        "prosecution": "अभियोजन पक्ष"
    },
    "ta": {
        "page": "பக்கம்",
        "no_text_pdf": "PDF இல் எந்த உரையும் இல்லை",
        "error_pdf": "PDF செயலாக்க பிழை",
        "ocr_extracted": "OCR மூலம் உரை பிரித்தெடுக்கப்பட்டது",
        "ocr_status": "OCR நிலை",
        "no_text_image": "படத்தில் படிக்கக்கூடிய உரை இல்லை",
        "visual_analysis": "காட்சி உள்ளடக்க பகுப்பாய்வு",
        "error_image": "படம் செயலாக்க பிழை",
        "unable_process": "படத்தை செயலாக்க முடியவில்லை - எந்த உரையும் காட்சி உள்ளடக்கமும் பிரித்தெடுக்கப்படவில்லை",
        "error_ocr": "OCR இல் பிழை",
        "error_vision": "காட்சி பகுப்பாய்வில் பிழை",
        "vision_unavailable": "காட்சி பகுப்பாய்வு கிடைக்கவில்லை",
        "manual_review": "கைமுறை மதிப்பாய்வு தேவை",
        "unsupported_file": "ஆதரிக்கப்படாத கோப்பு வகை",
        "evidence_doc": "ஆதார ஆவணம்",
        "credibility_score": "நம்பகத்தன்மை மதிப்பெண்",
        "relevance": "பொருத்தம்",
        "red_flags": "எச்சரிக்கை அறிகுறிகள்",
        "none": "எதுவுமில்லை",
        "recommendations": "பரிந்துரைகள்",
        "round": "சுற்று",
        "defense": "தற்காப்பு",
        "prosecution": "வழக்குத்தரப்பு"
    },
    "te": {
        "page": "పేజీ",
        "no_text_pdf": "PDF లో టెక్స్ట్ కనబడలేదు",
        "error_pdf": "PDF ప్రాసెసింగ్ లో లోపం",
        "ocr_extracted": "OCR ద్వారా టెక్స్ట్ సేకరించబడింది",
        "ocr_status": "OCR స్థితి",
        "no_text_image": "చిత్రంలో చదవదగిన టెక్స్ట్ లేదు",
        "visual_analysis": "దృశ్య కంటెంట్ విశ్లేషణ",
        "error_image": "చిత్రం ప్రాసెసింగ్ లో లోపం",
        "unable_process": "చిత్రాన్ని ప్రాసెస్ చేయలేకపోయింది - టెక్స్ట్ లేదా దృశ్య కంటెంట్ సేకరించబడలేదు",
        "error_ocr": "OCR లో లోపం",
        "error_vision": "దృశ్య విశ్లేషణలో లోపం",
        "vision_unavailable": "దృశ్య విశ్లేషణ అందుబాటులో లేదు",
        "manual_review": "మాన్యువల్ సమీక్ష అవసరం",
        "unsupported_file": "మద్దతు లేని ఫైల్ రకం",
        "evidence_doc": "సాక్ష్య పత్రం",
        "credibility_score": "విశ్వసనీయత స్కోర్",
        "relevance": "సంబంధం",
        "red_flags": "హెచ్చరిక సంకేతాలు",
        "none": "ఏదీ లేదు",
        "recommendations": "సిఫార్సులు",
        "round": "రౌండ్",
        "defense": "రక్షణ",
        "prosecution": "ప్రాసిక్యూషన్"
    },
    "bn": {
        "page": "পাতা",
        "no_text_pdf": "PDF এ কোনো টেক্সট পাওয়া যায়নি",
        "error_pdf": "PDF প্রসেসিং ত্রুটি",
        "ocr_extracted": "OCR দ্বারা টেক্সট নিষ্কাশিত",
        "ocr_status": "OCR স্থিতি",
        "no_text_image": "ছবিতে কোনো পাঠযোগ্য টেক্সট নেই",
        "visual_analysis": "ভিজ্যুয়াল কন্টেন্ট বিশ্লেষণ",
        "error_image": "ছবি প্রসেসিং ত্রুটি",
        "unable_process": "ছবি প্রসেস করতে অক্ষম - কোনো টেক্সট বা ভিজ্যুয়াল কন্টেন্ট নিষ্কাশিত হয়নি",
        "error_ocr": "OCR এ ত্রুটি",
        "error_vision": "ভিজ্যুয়াল বিশ্লেষণে ত্রুটি",
        "vision_unavailable": "ভিজ্যুয়াল বিশ্লেষণ উপলব্ধ নয়",
        "manual_review": "ম্যানুয়াল পর্যালোচনা প্রয়োজন",
        "unsupported_file": "অসমর্থিত ফাইল টাইপ",
        "evidence_doc": "প্রমাণ নথি",
        "credibility_score": "বিশ্বাসযোগ্যতা স্কোর",
        "relevance": "প্রাসঙ্গিকতা",
        "red_flags": "সতর্কতা চিহ্ন",
        "none": "কোনটিই নয়",
        "recommendations": "সুপারিশ",
        "round": "রাউন্ড",
        "defense": "প্রতিরক্ষা",
        "prosecution": "প্রসিকিউশন"
    },
    "mr": {
        "page": "पान",
        "no_text_pdf": "PDF मध्ये मजकूर आढळला नाही",
        "error_pdf": "PDF प्रोसेसिंग त्रुटी",
        "ocr_extracted": "OCR द्वारे मजकूर काढला",
        "ocr_status": "OCR स्थिती",
        "no_text_image": "प्रतिमेत वाचनीय मजकूर नाही",
        "visual_analysis": "दृश्य सामग्री विश्लेषण",
        "error_image": "प्रतिमा प्रोसेसिंग त्रुटी",
        "unable_process": "प्रतिमा प्रक्रिया करण्यात अक्षम - मजकूर किंवा दृश्य सामग्री काढली नाही",
        "error_ocr": "OCR मध्ये त्रुटी",
        "error_vision": "दृश्य विश्लेषणात त्रुटी",
        "vision_unavailable": "दृश्य विश्लेषण उपलब्ध नाही",
        "manual_review": "मॅन्युअल पुनरावलोकन आवश्यक",
        "unsupported_file": "असमर्थित फाइल प्रकार",
        "evidence_doc": "पुरावा दस्तऐवज",
        "credibility_score": "विश्वासार्हता गुण",
        "relevance": "प्रासंगिकता",
        "red_flags": "चेतावणी चिन्हे",
        "none": "काहीही नाही",
        "recommendations": "शिफारसी",
        "round": "फेरी",
        "defense": "बचाव",
        "prosecution": "फिर्याद"
    },
    "gu": {
        "page": "પૃષ્ઠ",
        "no_text_pdf": "PDF માં કોઈ ટેક્સ્ટ મળ્યો નથી",
        "error_pdf": "PDF પ્રોસેસિંગ ભૂલ",
        "ocr_extracted": "OCR દ્વારા ટેક્સ્ટ કાઢ્યો",
        "ocr_status": "OCR સ્થિતિ",
        "no_text_image": "છબીમાં વાંચી શકાય તેવો ટેક્સ્ટ નથી",
        "visual_analysis": "વિઝ્યુઅલ સામગ્રી વિશ્લેષણ",
        "error_image": "છબી પ્રોસેસિંગ ભૂલ",
        "unable_process": "છબી પ્રોસેસ કરવામાં અસમર્થ - કોઈ ટેક્સ્ટ અથવા વિઝ્યુઅલ સામગ્રી કાઢી નથી",
        "error_ocr": "OCR માં ભૂલ",
        "error_vision": "વિઝ્યુઅલ વિશ્લેષણમાં ભૂલ",
        "vision_unavailable": "વિઝ્યુઅલ વિશ્લેષણ ઉપલબ્ધ નથી",
        "manual_review": "મેન્યુઅલ સમીક્ષા જરૂરી",
        "unsupported_file": "અસમર્થિત ફાઇલ પ્રકાર",
        "evidence_doc": "પુરાવા દસ્તાવેજ",
        "credibility_score": "વિશ્વસનીયતા સ્કોર",
        "relevance": "સુસંગતતા",
        "red_flags": "ચેતવણી સંકેતો",
        "none": "કોઈ નહીં",
        "recommendations": "ભલામણો",
        "round": "રાઉન્ડ",
        "defense": "બચાવ",
        "prosecution": "પ્રોસિક્યુશન"
    },
    "kn": {
        "page": "ಪುಟ",
        "no_text_pdf": "PDF ನಲ್ಲಿ ಯಾವುದೇ ಪಠ್ಯ ಕಂಡುಬಂದಿಲ್ಲ",
        "error_pdf": "PDF ಪ್ರಕ್ರಿಯೆ ದೋಷ",
        "ocr_extracted": "OCR ಮೂಲಕ ಪಠ್ಯ ಹೊರತೆಗೆಯಲಾಗಿದೆ",
        "ocr_status": "OCR ಸ್ಥಿತಿ",
        "no_text_image": "ಚಿತ್ರದಲ್ಲಿ ಓದಲು ಸಾಧ್ಯವಾಗುವ ಪಠ್ಯ ಇಲ್ಲ",
        "visual_analysis": "ದೃಶ್ಯ ವಿಷಯ ವಿಶ್ಲೇಷಣೆ",
        "error_image": "ಚಿತ್ರ ಪ್ರಕ್ರಿಯೆ ದೋಷ",
        "unable_process": "ಚಿತ್ರವನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ - ಯಾವುದೇ ಪಠ್ಯ ಅಥವಾ ದೃಶ್ಯ ವಿಷಯ ಹೊರತೆಗೆಯಲಾಗಿಲ್ಲ",
        "error_ocr": "OCR ನಲ್ಲಿ ದೋಷ",
        "error_vision": "ದೃಶ್ಯ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ದೋಷ",
        "vision_unavailable": "ದೃಶ್ಯ ವಿಶ್ಲೇಷಣೆ ಲಭ್ಯವಿಲ್ಲ",
        "manual_review": "ಹಸ್ತಚಾಲಿತ ಪರಿಶೀಲನೆ ಅಗತ್ಯ",
        "unsupported_file": "ಬೆಂಬಲವಿಲ್ಲದ ಫೈಲ್ ಪ್ರಕಾರ",
        "evidence_doc": "ಸಾಕ್ಷ್ಯ ದಾಖಲೆ",
        "credibility_score": "ವಿಶ್ವಾಸಾರ್ಹತೆ ಅಂಕ",
        "relevance": "ಪ್ರಸ್ತುತತೆ",
        "red_flags": "ಎಚ್ಚರಿಕೆ ಸಂಕೇತಗಳು",
        "none": "ಯಾವುದೂ ಇಲ್ಲ",
        "recommendations": "ಶಿಫಾರಸುಗಳು",
        "round": "ಸುತ್ತು",
        "defense": "ರಕ್ಷಣೆ",
        "prosecution": "ಪ್ರಾಸಿಕ್ಯೂಷನ್"
    },
    "ml": {
        "page": "പേജ്",
        "no_text_pdf": "PDF ൽ ടെക്സ്റ്റ് കണ്ടെത്തിയില്ല",
        "error_pdf": "PDF പ്രോസസ്സിംഗ് പിശക്",
        "ocr_extracted": "OCR വഴി ടെക്സ്റ്റ് എക്സ്ട്രാക്റ്റ് ചെയ്തു",
        "ocr_status": "OCR സ്ഥിതി",
        "no_text_image": "ചിത്രത്തിൽ വായിക്കാൻ പറ്റുന്ന ടെക്സ്റ്റ് ഇല്ല",
        "visual_analysis": "വിഷ്വൽ ഉള്ളടക്ക വിശകലനം",
        "error_image": "ചിത്ര പ്രോസസ്സിംഗ് പിശക്",
        "unable_process": "ചിത്രം പ്രോസസ്സ് ചെയ്യാൻ കഴിയില്ല - ടെക്സ്റ്റോ വിഷ്വൽ ഉള്ളടക്കമോ എക്സ്ട്രാക്റ്റ് ചെയ്തില്ല",
        "error_ocr": "OCR ൽ പിശക്",
        "error_vision": "വിഷ്വൽ വിശകലനത്തിൽ പിശക്",
        "vision_unavailable": "വിഷ്വൽ വിശകലനം ലഭ്യമല്ല",
        "manual_review": "മാനുവൽ അവലോകനം ആവശ്യമാണ്",
        "unsupported_file": "പിന്തുണയ്ക്കാത്ത ഫയൽ തരം",
        "evidence_doc": "തെളിവ് രേഖ",
        "credibility_score": "വിശ്വാസ്യത സ്കോർ",
        "relevance": "പ്രസക്തി",
        "red_flags": "മുന്നറിയിപ്പ് അടയാളങ്ങൾ",
        "none": "ഒന്നുമില്ല",
        "recommendations": "ശുപാർശകൾ",
        "round": "റൗണ്ട്",
        "defense": "പ്രതിരോധം",
        "prosecution": "പ്രോസിക്യൂഷൻ"
    }
}

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "ta": "தமிழ் (Tamil)",
    "te": "తెలుగు (Telugu)",
    "bn": "বাংলা (Bengali)",
    "mr": "मराठी (Marathi)",
    "gu": "ગુજરાતી (Gujarati)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "ml": "മലയാളം (Malayalam)"
}

def get_translation(key: str, language: str = "en") -> str:
    """Get translated text for a given key and language."""
    if language not in TRANSLATIONS:
        language = "en"
    return TRANSLATIONS[language].get(key, TRANSLATIONS["en"].get(key, key))

def get_language_instruction(language: str) -> str:
    """Get instruction for LLM to respond in specified language."""
    if language == "en":
        return ""
    
    lang_map = {
        "hi": "Hindi (हिंदी)",
        "ta": "Tamil (தமிழ்)",
        "te": "Telugu (తెలుగు)",
        "bn": "Bengali (বাংলা)",
        "mr": "Marathi (मराठी)",
        "gu": "Gujarati (ગુજરાતી)",
        "kn": "Kannada (ಕನ್ನಡ)",
        "ml": "Malayalam (മലയാളം)"
    }
    
    lang_name = lang_map.get(language, "English")
    return f"\n\n⚠️ CRITICAL: You MUST respond ENTIRELY in {lang_name}. All legal arguments, analysis, reasoning, and recommendations must be in {lang_name}. Do NOT use English except for citations (BNS sections, IPC sections, case names)."


# ─────────────────────────────────────────────
# RAG SETUP
# ─────────────────────────────────────────────

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("texts.pkl", "rb") as f:
    texts = pickle.load(f)

index = faiss.read_index("faiss.index")


def search(query: str, top_k: int = 3) -> str:
    """Retrieve top-k relevant legal context chunks for a given query."""
    q = model.encode([query])
    D, I = index.search(q, top_k)
    chunks = [texts[i][:600] for i in I[0] if i < len(texts)]
    return "\n\n---\n\n".join(chunks)


# ─────────────────────────────────────────────
# PDF & IMAGE PROCESSING
# ─────────────────────────────────────────────

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


def check_evidence_credibility(evidence_text: str, case_description: str, context: str, language: str = "en") -> dict:
    """
    Performs credibility check on uploaded evidence.
    Analyzes relevance, authenticity concerns, and strategic value.
    Returns dict with credibility score, issues, and recommendations.
    """
    # Detect if this is image evidence (contains OCR/Vision markers)
    is_image_evidence = any([
        "OCR" in evidence_text,
        get_translation("ocr_extracted", language) in evidence_text,
        get_translation("visual_analysis", language) in evidence_text
    ])
    
    lang_instruction = get_language_instruction(language)
    
    evidence_type_note = ""
    if is_image_evidence:
        evidence_type_note = f"""
NOTE: This is IMAGE EVIDENCE containing both OCR text extraction and visual content analysis.
Evaluate both the textual content AND the visual scene description.
Consider image quality, clarity, and forensic authenticity indicators."""
    
    system = f"""You are an experienced legal evidence analyst in Indian courts. 
You evaluate documentary evidence for authenticity, relevance, and strategic value. 
You identify potential credibility issues, contradictions, and procedural concerns. 
IMPORTANT: The credibility score MUST reflect the severity of any red flags you identify. 
Each significant red flag should reduce the score by 2-3 points from a baseline of 8-9.{lang_instruction}"""

    prompt = f"""
CASE DESCRIPTION:
{case_description[:500]}

LEGAL CONTEXT:
{context[:400]}

EVIDENCE CONTENT:
{evidence_text[:2000]}
{evidence_type_note}

Your task:
Perform a thorough credibility check on this evidence. Analyze:

1. **Relevance**: How directly does this evidence relate to the case?
2. **Authenticity Concerns**: Any signs of potential tampering, inconsistencies, or missing authentication?
3. **Legal Admissibility**: Procedural issues that might affect admissibility in court?
4. **Strategic Value**: How strong is this evidence for the defense?
5. **Red Flags**: Any contradictions with the case narrative or potential prosecution attacks?
6. **Recommendations**: How should this evidence be used (or not used)?

SCORING GUIDELINES:
- Start with baseline 8-9 for clean, relevant evidence
- Deduct 2-3 points for EACH major red flag (tampering signs, contradictions, quality issues)
- Deduct 1-2 points for EACH moderate concern (missing authentication, procedural issues)
- Score 1-3: Highly questionable, should NOT be used
- Score 4-6: Significant concerns, use with caution
- Score 7-8: Minor concerns, generally reliable
- Score 9-10: Highly credible, strong evidence

Respond in this EXACT JSON format:
{{
  "credibility_score": <integer 1-10 based on red flags identified>,
  "relevance": "<brief assessment>",
  "authenticity_concerns": "<list concerns or 'None identified'>",
  "admissibility_issues": "<list issues or 'None identified'>",
  "strategic_value": "<brief assessment>",
  "red_flags": ["<flag 1>", "<flag 2>", ...] or [],
  "recommendations": "<how to use this evidence effectively>",
  "overall_assessment": "<2-3 sentence summary>"
}}

CRITICAL: Ensure credibility_score is proportional to red_flags. More red flags = lower score.
Return ONLY valid JSON. No extra text.
"""
    raw = ask_llm(prompt, system, language)

    try:
        cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
        result = json.loads(cleaned)
        
        # Validate that score makes sense with red flags
        num_red_flags = len(result.get("red_flags", []))
        score = result.get("credibility_score", 5)
        
        # If there are 2+ red flags but score is still high, adjust it
        if num_red_flags >= 2 and score > 6:
            result["credibility_score"] = max(3, 7 - (num_red_flags * 2))
        elif num_red_flags == 1 and score > 7:
            result["credibility_score"] = 6
        
        return result
        
    except json.JSONDecodeError as e:
        # Log the actual response for debugging
        print(f"JSON Decode Error: {e}")
        print(f"Raw LLM response: {raw[:500]}")
        
        # Fallback structure
        return {
            "credibility_score": 5,
            "relevance": "Unable to fully analyze",
            "authenticity_concerns": "Analysis incomplete",
            "admissibility_issues": "Requires manual review",
            "strategic_value": "Uncertain",
            "red_flags": [],
            "recommendations": "Consult with legal expert before using this evidence.",
            "overall_assessment": "Credibility analysis could not be completed. Manual review recommended."
        }


# ─────────────────────────────────────────────
# LLM CLIENT
# ─────────────────────────────────────────────

_client = None

def get_client():
    global _client
    if _client is None:
        _client = mlflow.deployments.get_deploy_client("databricks")
    return _client


def ask_llm(prompt: str, system: str = "", language: str = "en") -> str:
    """Call the LLM with an optional system prompt and language support."""
    client = get_client()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.predict(
        endpoint="databricks-llama-4-maverick",
        inputs={"messages": messages}
    )

    if isinstance(response, dict) and "choices" in response:
        return response["choices"][0]["message"]["content"].strip()
    return str(response).strip()


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def extract_json_from_text(text: str) -> str:
    """
    Extract JSON from text that may contain markdown code blocks or other formatting.
    Tries multiple extraction strategies.
    """
    # Strategy 1: Remove markdown code blocks (```json ... ``` or ``` ... ```)
    # Match both opening and closing code blocks
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = re.sub(r"```\s*$", "", cleaned)
    cleaned = cleaned.strip()
    
    # Strategy 2: If that didn't work, try to find JSON object/array boundaries
    if not cleaned.startswith(("{", "[")):
        # Look for first { or [
        start_brace = cleaned.find("{")
        start_bracket = cleaned.find("[")
        
        if start_brace == -1 and start_bracket == -1:
            return text  # No JSON found, return original
        
        if start_brace != -1 and (start_bracket == -1 or start_brace < start_bracket):
            # Found { first
            start = start_brace
            # Find matching closing }
            brace_count = 0
            for i in range(start, len(cleaned)):
                if cleaned[i] == '{':
                    brace_count += 1
                elif cleaned[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        cleaned = cleaned[start:i+1]
                        break
        else:
            # Found [ first
            start = start_bracket
            # Find matching closing ]
            bracket_count = 0
            for i in range(start, len(cleaned)):
                if cleaned[i] == '[':
                    bracket_count += 1
                elif cleaned[i] == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        cleaned = cleaned[start:i+1]
                        break
    
    return cleaned.strip()


# ─────────────────────────────────────────────
# AGENTS - INTERACTIVE VERSION
# ─────────────────────────────────────────────

def lawyer_ai_with_options(user_argument: str, context: str, history: list, opponent_attack: str = "", language: str = "en") -> dict:
    """
    Defense Lawyer AI — generates multiple argument strategy options for user to choose from.
    Returns dict with 3 options and whether evidence is needed.
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] Opponent said: {r['opponent']}\nPrevious Lawyer response: {r['lawyer']}\n"

    opponent_context = f"\n\nOPPONENT'S LATEST ATTACK:\n{opponent_attack}" if opponent_attack else ""
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an experienced defense lawyer in an Indian court. 
You cite relevant sections from BNS 2023 and IPC where applicable. 
Be precise, strategic, and legally sound.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ROUNDS:
{history_text if history_text else "This is the first round."}

CURRENT USER ARGUMENT:
{user_argument}
{opponent_context}

Your task:
Generate 3 different defense strategy options for the user to choose from.

Each option should:
1. Take a different legal angle (e.g., evidence-based, procedural, constitutional rights)
2. Be specific and actionable
3. Reference relevant BNS 2023 or IPC sections
4. Be under 150 words

Also, determine if additional evidence documents would significantly strengthen any argument.

Respond in this EXACT JSON format:
{{
  "needs_evidence": true or false,
  "evidence_reason": "<brief explanation if true, otherwise empty string>",
  "options": [
    {{
      "id": 1,
      "title": "<Short strategy title>",
      "argument": "<Full argument text>",
      "strength": "<Why this approach is strong>"
    }},
    {{
      "id": 2,
      "title": "<Short strategy title>",
      "argument": "<Full argument text>",
      "strength": "<Why this approach is strong>"
    }},
    {{
      "id": 3,
      "title": "<Short strategy title>",
      "argument": "<Full argument text>",
      "strength": "<Why this approach is strong>"
    }}
  ]
}}

Return ONLY valid JSON.
"""
    raw = ask_llm(prompt, system, language)

    try:
        cleaned = extract_json_from_text(raw)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback structure
        return {
            "needs_evidence": False,
            "evidence_reason": "",
            "options": [
                {
                    "id": 1,
                    "title": "Direct Defense",
                    "argument": user_argument,
                    "strength": "Straightforward approach based on user's input."
                }
            ]
        }


def lawyer_ai_with_evidence(
    selected_argument: str,
    context: str,
    history: list,
    evidence_texts: list,
    credibility_reports: list,
    language: str = "en"
) -> str:
    """
    Defense Lawyer AI — strengthens the selected argument using uploaded evidence
    and incorporating credibility assessments.
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] Opponent said: {r['opponent']}\nPrevious Lawyer response: {r['lawyer']}\n"

    evidence_summary = ""
    for i, (txt, cred_report) in enumerate(zip(evidence_texts, credibility_reports)):
        evidence_doc = get_translation("evidence_doc", language)
        cred_score = get_translation("credibility_score", language)
        relevance = get_translation("relevance", language)
        red_flags = get_translation("red_flags", language)
        none = get_translation("none", language)
        recommendations = get_translation("recommendations", language)
        
        evidence_summary += f"\n\n[{evidence_doc} {i+1}]:\n"
        evidence_summary += f"Content: {txt[:800]}\n"
        evidence_summary += f"{cred_score}: {cred_report['credibility_score']}/10\n"
        evidence_summary += f"{relevance}: {cred_report['relevance']}\n"
        evidence_summary += f"{red_flags}: {', '.join(cred_report['red_flags']) if cred_report['red_flags'] else none}\n"
        evidence_summary += f"{recommendations}: {cred_report['recommendations']}\n"
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an experienced defense lawyer in an Indian court. 
You cite relevant sections from BNS 2023 and IPC where applicable. 
Incorporate evidence intelligently, address any credibility concerns preemptively, 
and use only the strongest parts of the evidence.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ROUNDS:
{history_text if history_text else "This is the first round."}

UPLOADED EVIDENCE (with credibility analysis):
{evidence_summary}

SELECTED ARGUMENT STRATEGY:
{selected_argument}

Your task:
Strengthen the selected argument by:
1. Incorporating specific facts/details from the uploaded evidence
2. Addressing any credibility concerns proactively
3. Using only evidence with high credibility scores strategically
4. Avoiding or downplaying evidence with red flags
5. Citing relevant legal sections from BNS 2023/IPC
6. Preemptively countering opposition attacks on evidence authenticity
7. Keeping response under 200 words, structured and persuasive

Respond as the defense lawyer now:
"""
    return ask_llm(prompt, system, language)


def lawyer_ai(user_argument: str, context: str, history: list, language: str = "en") -> str:
    """
    Defense Lawyer AI — strengthens the user's argument using legal context
    and prior round history. (Original non-interactive version for fallback)
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] Opponent said: {r['opponent']}\nPrevious Lawyer response: {r['lawyer']}\n"
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an experienced defense lawyer in an Indian court. 
You cite relevant sections from BNS 2023 and IPC where applicable. 
Be precise, strategic, and legally sound. Do NOT repeat yourself.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ROUNDS:
{history_text if history_text else "This is the first round."}

CURRENT USER ARGUMENT:
{user_argument}

Your task:
1. Identify the strongest legal points in the user's argument.
2. Strengthen weak points using the legal context above.
3. Preemptively counter any likely opposition attacks.
4. Keep your response under 200 words, structured and persuasive.

Respond as the defense lawyer now:
"""
    return ask_llm(prompt, system, language)


def opponent_ai(user_argument: str, context: str, history: list, language: str = "en") -> str:
    """
    Opposing Counsel AI — attacks the user's argument, finds loopholes,
    challenges evidence using legal context.
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] You previously attacked: {r['opponent']}\n"
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an aggressive opposing counsel in an Indian court. 
You exploit legal loopholes, challenge evidence credibility, 
and reference procedural weaknesses. Be sharp and adversarial. 
Do NOT repeat prior attacks.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ATTACKS (avoid repeating):
{history_text if history_text else "This is the first round."}

ARGUMENT TO ATTACK:
{user_argument}

Your task:
1. Identify the 2-3 biggest weaknesses or contradictions.
2. Challenge the evidence or witness credibility if applicable.
3. Raise procedural or legal objections using the context above.
4. Keep your response under 200 words. Be aggressive but professional.

Respond as the opposing counsel now:
"""
    return ask_llm(prompt, system, language)


def judge_ai(user_argument: str, lawyer_arg: str, opponent_arg: str, round_num: int, credibility_reports: list = None, language: str = "en") -> dict:
    """
    Judge AI — evaluates both sides, gives scores and structured reasoning.
    Now considers evidence credibility scores in evaluation.
    Returns a dict with scores and analysis.
    """
    lang_instruction = get_language_instruction(language)
    
    system = f"""You are a neutral, senior judge in an Indian court. 
You evaluate arguments on: legal soundness, evidence use, clarity, and persuasiveness. 
You are fair, objective, and concise. 
When evidence is presented, you MUST consider its credibility score and red flags in your scoring. 
Low-credibility evidence (score < 6) should significantly reduce the argument's score. 
CRITICAL: You MUST return ONLY valid JSON with no additional text before or after.{lang_instruction}"""

    # Build evidence credibility section if reports are provided
    evidence_section = ""
    if credibility_reports and len(credibility_reports) > 0:
        evidence_doc = get_translation("evidence_doc", language)
        cred_score = get_translation("credibility_score", language)
        red_flags = get_translation("red_flags", language)
        none = get_translation("none", language)
        
        evidence_section = f"\n\nEVIDENCE CREDIBILITY ANALYSIS ({get_translation('defense', language)}):\n"
        for i, report in enumerate(credibility_reports):
            score = report.get("credibility_score", 5)
            flags = report.get("red_flags", [])
            concerns = report.get("authenticity_concerns", "Unknown")
            
            evidence_section += f"\n[{evidence_doc} {i+1}]:\n"
            evidence_section += f"- {cred_score}: {score}/10\n"
            evidence_section += f"- {red_flags}: {', '.join(flags) if flags else none}\n"
            evidence_section += f"- Authenticity Concerns: {concerns}\n"
            evidence_section += f"- Overall: {report.get('overall_assessment', 'N/A')}\n"
        
        evidence_section += "\n⚠️ SCORING GUIDANCE:\n"
        evidence_section += "- Evidence with score 7-10: Strong support, minimal deduction\n"
        evidence_section += "- Evidence with score 4-6: Moderate concerns, deduct 1-2 points from defense\n"
        evidence_section += "- Evidence with score 1-3: Serious issues, deduct 2-4 points from defense\n"
        evidence_section += "- Multiple red flags: Each should further reduce defense score\n"
    
    round_label = get_translation("round", language)
    defense = get_translation("defense", language)
    prosecution = get_translation("prosecution", language)

    prompt = f"""
{round_label.upper()} {round_num} EVALUATION

{defense.upper()} (User + Lawyer AI):
{lawyer_arg}

{prosecution.upper()} (Opponent AI):
{opponent_arg}
{evidence_section}

Your task:
Evaluate this round considering ALL factors including evidence credibility.

CRITICAL EVALUATION RULES:
1. If defense used evidence with credibility score < 6, their score MUST be reduced by 1-3 points
2. If defense evidence has 2+ red flags, their score MUST be reduced by 2-4 points
3. Strong legal arguments cannot fully compensate for weak/questionable evidence
4. Evidence with authenticity concerns undermines the entire defense strategy

Respond ONLY in this exact JSON format (no markdown, no extra text):
{{
  "defense_score": <integer 1-10, ADJUSTED DOWN if evidence has low credibility>,
  "prosecution_score": <integer 1-10>,
  "defense_strengths": "<1-2 sentences>",
  "defense_weaknesses": "<1-2 sentences, MUST mention evidence credibility issues if present>",
  "prosecution_strengths": "<1-2 sentences>",
  "prosecution_weaknesses": "<1-2 sentences>",
  "round_winner": "defense" or "prosecution",
  "reasoning": "<2-3 sentences explaining your scoring, MUST address evidence credibility if reports provided>",
  "evidence_impact": "<1 sentence on how evidence quality affected the scoring, or 'N/A' if no evidence>"
}}

IMPORTANT: Return ONLY the JSON object above. No ```json markers, no explanation, nothing else.
"""
    raw = ask_llm(prompt, system, language)

    # Safely parse JSON from LLM output
    try:
        cleaned = extract_json_from_text(raw)
        result = json.loads(cleaned)
        
        # Additional validation: If evidence was provided with low credibility, ensure defense score reflects it
        if credibility_reports and len(credibility_reports) > 0:
            avg_cred_score = sum(r.get("credibility_score", 5) for r in credibility_reports) / len(credibility_reports)
            total_red_flags = sum(len(r.get("red_flags", [])) for r in credibility_reports)
            
            defense_score = result.get("defense_score", 5)
            
            # Apply automatic deductions if LLM didn't adjust properly
            if avg_cred_score < 6 and defense_score > 6:
                # Low credibility evidence but high defense score - adjust down
                penalty = int((6 - avg_cred_score) * 0.5) + 1
                result["defense_score"] = max(3, defense_score - penalty)
                
            if total_red_flags >= 2 and defense_score > 5:
                # Multiple red flags - additional penalty
                result["defense_score"] = max(3, result["defense_score"] - 1)
        
        # Ensure evidence_impact field exists
        if "evidence_impact" not in result:
            result["evidence_impact"] = "N/A"
        
        return result
        
    except json.JSONDecodeError as e:
        # Enhanced error logging
        print(f"[Judge AI] JSON Decode Error: {e}")
        print(f"[Judge AI] Raw response length: {len(raw)}")
        print(f"[Judge AI] Raw response (first 500 chars): {raw[:500]}")
        print(f"[Judge AI] Cleaned text (first 500 chars): {extract_json_from_text(raw)[:500]}")
        
        return {
            "defense_score": 5,
            "prosecution_score": 5,
            "defense_strengths": "Could not parse judge response - see logs for details.",
            "defense_weaknesses": "JSON parsing failed.",
            "prosecution_strengths": "Unable to evaluate.",
            "prosecution_weaknesses": "Unable to evaluate.",
            "round_winner": "tie",
            "reasoning": f"Error parsing judge response. First 200 chars: {raw[:200]}",
            "evidence_impact": "Unable to evaluate"
        }


# ─────────────────────────────────────────────
# WIN PROBABILITY ENGINE
# ─────────────────────────────────────────────

def sigmoid(x):
    """
    Sigmoid function to convert score differential to probability.
    Maps [-infinity, +infinity] to [0, 1] in an S-curve.
    """
    return 1 / (1 + math.exp(-x))


def compute_win_probability(round_results: list, language: str = "en") -> dict:
    """
    Compute final win probability from judge scores across all rounds.
    Uses a sophisticated algorithm that considers:
    1. Round winners (who won more rounds) - adjusted for narrow margins
    2. Score differentials (margin of victory)
    3. Recent performance (later rounds weighted more)
    4. Overall momentum
    5. Evidence quality impact across rounds
    
    Also generates final strengths, weaknesses, and strategy suggestions.
    """
    if not round_results:
        return {
            "win_probability": 50,
            "strong_points": [],
            "weak_points": [],
            "suggestions": [],
            "detailed_breakdown": {
                "rounds_won": {"defense": 0, "prosecution": 0},
                "total_scores": {"defense": 0, "prosecution": 0},
                "average_margin": 0,
                "momentum": "neutral",
                "evidence_quality": "unknown"
            }
        }

    num_rounds = len(round_results)
    
    # Calculate basic statistics
    defense_rounds_won = sum(1 for r in round_results if r.get("round_winner") == "defense")
    prosecution_rounds_won = sum(1 for r in round_results if r.get("round_winner") == "prosecution")
    ties = sum(1 for r in round_results if r.get("round_winner") not in ["defense", "prosecution"])
    
    total_defense = sum(r.get("defense_score", 5) for r in round_results)
    total_prosecution = sum(r.get("prosecution_score", 5) for r in round_results)
    
    # Calculate average scores and margin
    avg_defense = total_defense / num_rounds
    avg_prosecution = total_prosecution / num_rounds
    avg_margin = avg_defense - avg_prosecution
    
    # Analyze evidence quality impact
    evidence_rounds = [r for r in round_results if r.get("evidence_impact") and r.get("evidence_impact") != "N/A"]
    if evidence_rounds:
        evidence_quality = "evidence_used"
    else:
        evidence_quality = "no_evidence"
    
    # Component 1: Round Win Percentage with Margin Adjustment (30% weight)
    # Reduce the impact of narrow victories
    if defense_rounds_won + prosecution_rounds_won > 0:
        raw_round_win = defense_rounds_won / (defense_rounds_won + prosecution_rounds_won)
        
        # Adjust based on how narrow the wins were
        # If average margin is small (< 1.5), reduce the round win impact
        if abs(avg_margin) < 1.5:
            # Narrow victories - move closer to 0.5
            round_win_factor = 0.5 + (raw_round_win - 0.5) * 0.5
        else:
            round_win_factor = raw_round_win
    else:
        round_win_factor = 0.5
    
    # Component 2: Score-Based Probability (45% weight)
    # Primary component - directly based on score differential
    # Use a more sensitive sigmoid that responds better to score differences
    # Dividing by 2.5 instead of 3 makes it more responsive
    score_diff = avg_margin
    score_factor = sigmoid(score_diff / 2.5)
    
    # Component 3: Consistency Factor (15% weight)
    # Rewards consistent performance across rounds
    defense_margins = []
    for r in round_results:
        margin = r.get("defense_score", 5) - r.get("prosecution_score", 5)
        defense_margins.append(margin)
    
    # Standard deviation of margins (lower = more consistent)
    if len(defense_margins) > 1:
        mean_margin = sum(defense_margins) / len(defense_margins)
        variance = sum((m - mean_margin) ** 2 for m in defense_margins) / len(defense_margins)
        std_dev = math.sqrt(variance)
        
        # Higher consistency = lower std dev = higher factor
        # Normalize: std_dev of 0 = 1.0, std_dev of 3+ = 0.5
        consistency_factor = max(0.5, 1.0 - (std_dev / 6))
        
        # Apply the mean margin direction
        if mean_margin > 0:
            consistency_factor = 0.5 + (consistency_factor - 0.5)
        else:
            consistency_factor = 0.5 - (consistency_factor - 0.5)
    else:
        # Single round - base on that round's margin
        consistency_factor = sigmoid(defense_margins[0] / 3)
    
    # Component 4: Momentum (10% weight)
    # Check if defense is improving over time
    if num_rounds >= 2:
        first_half = round_results[:num_rounds//2]
        second_half = round_results[num_rounds//2:]
        
        first_half_avg = sum(r.get("defense_score", 5) - r.get("prosecution_score", 5) for r in first_half) / len(first_half)
        second_half_avg = sum(r.get("defense_score", 5) - r.get("prosecution_score", 5) for r in second_half) / len(second_half)
        
        momentum_diff = second_half_avg - first_half_avg
        # Positive momentum boosts, negative momentum reduces
        momentum_factor = 0.5 + (momentum_diff / 10)
        momentum_factor = max(0, min(1, momentum_factor))
        
        if momentum_diff > 1:
            momentum_label = "improving"
        elif momentum_diff < -1:
            momentum_label = "declining"
        else:
            momentum_label = "stable"
    else:
        momentum_factor = 0.5
        momentum_label = "insufficient_data"
    
    # Combine all components with adjusted weights
    # Score factor has the highest weight since it's most directly related to performance
    win_probability = (
        round_win_factor * 0.30 +    # Reduced from 35% to 30%
        score_factor * 0.45 +          # Increased from 35% to 45%
        consistency_factor * 0.15 +    # New component
        momentum_factor * 0.10
    ) * 100
    
    # Clamp to reasonable bounds (never show 0% or 100%)
    win_probability = max(5, min(95, win_probability))
    win_probability = round(win_probability)
    
    # Extract strengths and weaknesses
    strong_points = [r["defense_strengths"] for r in round_results if r.get("defense_strengths")]
    weak_points = [r["defense_weaknesses"] for r in round_results if r.get("defense_weaknesses")]
    
    lang_instruction = get_language_instruction(language)
    
    # Generate strategy suggestions using LLM
    evidence_context = ""
    if evidence_rounds:
        evidence_context = f"\n- Evidence was used in {len(evidence_rounds)}/{num_rounds} rounds"
    
    defense = get_translation("defense", language)
    prosecution = get_translation("prosecution", language)
    
    summary_prompt = f"""
Based on this courtroom simulation analysis:
- {defense} rounds won: {defense_rounds_won}/{num_rounds}
- {prosecution} rounds won: {prosecution_rounds_won}/{num_rounds}
- {defense} average score: {avg_defense:.1f}
- {prosecution} average score: {avg_prosecution:.1f}
- Average margin: {avg_margin:.1f} points per round
- Performance momentum: {momentum_label}{evidence_context}
- Current win probability: {win_probability}%

Key weaknesses identified across rounds:
{'; '.join(weak_points) if weak_points else 'None identified'}

Give 3-4 concrete, actionable legal strategy suggestions to improve the defense case.
Focus on addressing the weaknesses and building on strengths.
If evidence quality was an issue, suggest how to obtain better evidence.
Format as a JSON array of strings. Return ONLY the JSON array.{lang_instruction}
"""
    raw_suggestions = ask_llm(summary_prompt, language=language)
    try:
        cleaned = extract_json_from_text(raw_suggestions)
        suggestions = json.loads(cleaned)
        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]
    except Exception:
        suggestions = [
            "Review and strengthen evidence documentation.",
            "Prepare stronger witness statements.",
            "Research applicable BNS 2023 sections.",
            "Address procedural weaknesses identified by prosecution."
        ]

    return {
        "win_probability": win_probability,
        "strong_points": strong_points,
        "weak_points": weak_points,
        "suggestions": suggestions,
        "detailed_breakdown": {
            "rounds_won": {
                "defense": defense_rounds_won,
                "prosecution": prosecution_rounds_won,
                "ties": ties
            },
            "total_scores": {
                "defense": total_defense,
                "prosecution": total_prosecution
            },
            "average_scores": {
                "defense": round(avg_defense, 1),
                "prosecution": round(avg_prosecution, 1)
            },
            "average_margin": round(avg_margin, 1),
            "momentum": momentum_label,
            "evidence_quality": evidence_quality,
            "component_contributions": {
                "round_wins_adjusted": f"{round(round_win_factor * 30, 1)}%",
                "score_based": f"{round(score_factor * 45, 1)}%",
                "consistency": f"{round(consistency_factor * 15, 1)}%",
                "momentum": f"{round(momentum_factor * 10, 1)}%"
            }
        }
    }


# ─────────────────────────────────────────────
# SIMULATION RUNNERS
# ─────────────────────────────────────────────

def run_simulation(case_description: str, num_rounds: int = 2, language: str = "en") -> dict:
    """
    Orchestrates the full courtroom simulation (non-interactive version).
    Returns all round data + final verdict.
    """
    context = search(case_description)
    history = []
    round_results = []
    rounds_data = []

    current_argument = case_description

    for round_num in range(1, num_rounds + 1):
        opp = opponent_ai(current_argument, context, history, language)
        law = lawyer_ai(current_argument, context, history, language)
        verdict = judge_ai(current_argument, law, opp, round_num, credibility_reports=None, language=language)

        history.append({"opponent": opp, "lawyer": law})
        round_results.append(verdict)
        rounds_data.append({
            "round": round_num,
            "opponent": opp,
            "lawyer": law,
            "judge": verdict
        })

        # Next round argues from lawyer's improved position
        current_argument = law

    final = compute_win_probability(round_results, language)

    return {
        "rounds": rounds_data,
        "final": final,
        "context_used": context[:400] + "..."
    }


def start_interactive_simulation(case_description: str, language: str = "en") -> dict:
    """
    Initializes an interactive simulation session.
    Returns context and initial state.
    Simulation runs continuously until user ends it.
    """
    context = search(case_description)
    return {
        "context": context,
        "current_round": 1,
        "history": [],
        "round_results": [],
        "current_argument": case_description,
        "case_description": case_description,  # Store for credibility checks
        "language": language  # Store language preference
    }


def run_interactive_round(
    state: dict,
    selected_option_id: int = None,
    evidence_files: list = None
) -> dict:
    """
    Runs one round of the interactive simulation.
    
    Returns:
    - If waiting for user choice: {"status": "awaiting_choice", "options": [...], "opponent_attack": "..."}
    - If checking credibility: {"status": "checking_credibility", "credibility_reports": [...]}
    - If round complete: {"status": "round_complete", "round_data": {...}}
    """
    context = state["context"]
    history = state["history"]
    current_round = state["current_round"]
    current_argument = state["current_argument"]
    case_description = state.get("case_description", current_argument)
    language = state.get("language", "en")
    
    # Step 1: Generate opponent attack if not yet done
    if "pending_opponent" not in state:
        opp = opponent_ai(current_argument, context, history, language)
        state["pending_opponent"] = opp
        
        # Step 2: Generate lawyer options
        options_data = lawyer_ai_with_options(current_argument, context, history, opp, language)
        state["pending_options"] = options_data
        
        return {
            "status": "awaiting_choice",
            "opponent_attack": opp,
            "options": options_data["options"],
            "needs_evidence": options_data["needs_evidence"],
            "evidence_reason": options_data.get("evidence_reason", "")
        }
    
    # Step 3: User has selected an option (or we have selected_argument from previous call)
    if (selected_option_id is not None or "selected_argument" in state) and "final_lawyer_response" not in state:
        # Get or retrieve selected argument
        if "selected_argument" not in state:
            options_data = state["pending_options"]
            selected = next((opt for opt in options_data["options"] if opt["id"] == selected_option_id), None)
            
            if not selected:
                selected = options_data["options"][0]  # Fallback
            
            state["selected_argument"] = selected["argument"]
        
        # Step 4: If evidence provided, perform credibility check
        if evidence_files and "credibility_reports" not in state:
            evidence_texts = []
            credibility_reports = []
            
            for f in evidence_files:
                # Reset file pointer
                f.seek(0)
                
                # Process file based on type (PDF or image)
                txt = process_evidence_file(f, language)
                evidence_texts.append(txt)
                
                # Perform credibility check
                cred_report = check_evidence_credibility(txt, case_description, context, language)
                credibility_reports.append(cred_report)
            
            state["evidence_texts"] = evidence_texts
            state["credibility_reports"] = credibility_reports
            
            return {
                "status": "checking_credibility",
                "credibility_reports": credibility_reports,
                "evidence_texts": evidence_texts
            }
        
        # Step 5: Generate final lawyer response with or without evidence
        credibility_reports_for_judge = None
        
        if "credibility_reports" in state and "evidence_texts" in state:
            # User has reviewed credibility - proceed with evidence
            law = lawyer_ai_with_evidence(
                state["selected_argument"],
                context,
                history,
                state["evidence_texts"],
                state["credibility_reports"],
                language
            )
            credibility_reports_for_judge = state["credibility_reports"]
            
        elif evidence_files:
            # Evidence provided but credibility not checked yet (shouldn't happen)
            evidence_texts = [process_evidence_file(f, language) for f in evidence_files]
            credibility_reports = [
                check_evidence_credibility(txt, case_description, context, language)
                for txt in evidence_texts
            ]
            law = lawyer_ai_with_evidence(
                state["selected_argument"],
                context,
                history,
                evidence_texts,
                credibility_reports,
                language
            )
            credibility_reports_for_judge = credibility_reports
        else:
            # No evidence - use selected argument directly
            law = state["selected_argument"]
            credibility_reports_for_judge = None
        
        state["final_lawyer_response"] = law
        opp = state["pending_opponent"]
        
        # Judge evaluation - NOW INCLUDES CREDIBILITY REPORTS
        verdict = judge_ai(current_argument, law, opp, current_round, credibility_reports=credibility_reports_for_judge, language=language)
        
        # Update state
        history.append({"opponent": opp, "lawyer": law})
        state["round_results"].append(verdict)
        
        round_data = {
            "round": current_round,
            "opponent": opp,
            "lawyer": law,
            "judge": verdict
        }
        
        # Prepare for next round
        state["current_argument"] = law
        state["current_round"] += 1
        state["history"] = history
        
        # Clean up temporary state
        del state["pending_opponent"]
        del state["pending_options"]
        del state["final_lawyer_response"]
        if "selected_argument" in state:
            del state["selected_argument"]
        if "evidence_texts" in state:
            del state["evidence_texts"]
        if "credibility_reports" in state:
            del state["credibility_reports"]
        
        # Round is complete - continuous mode (no round limit)
        return {
            "status": "round_complete",
            "round_data": round_data
        }
    
    # Should not reach here in normal flow
    return {"status": "error", "message": "Invalid state"}
