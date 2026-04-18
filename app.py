import streamlit as st
import json
from pathlib import Path
from backend import (
    start_interactive_simulation,
    run_interactive_round,
    compute_win_probability,
    LANGUAGE_NAMES,
    ask_llm
)


UI_CACHE_FILE = Path("ui_translations_cache.json")


UI_TRANSLATIONS = {
    "en": {
        "lang_title": "### 🌐 Language / भाषा",
        "select_interface_language": "Select Interface Language",
        "about_app": "**About This App:**",
        "about_desc": "An AI-powered courtroom simulation that helps you:",
        "about_langs": "**Supported Languages:**",
        "header_title": "⚖️ AI Courtroom Battle Simulator",
        "header_subtitle": "Interactive adversarial legal reasoning · BNS 2023 · Powered by Databricks LLaMA",
        "describe_case": "Describe your case",
        "case_placeholder": "e.g. My client is accused of theft under BNS Section 303. The only evidence is CCTV footage from a store, however the footage quality is poor and the identity is unclear. There are no eyewitnesses...",
        "start_hearing": "⚔️ Start Hearing",
        "warning_enter_case": "⚠️ Please enter your case description before running the simulation.",
        "spinner_init": "🔄 Initializing interactive hearing...",
        "sim_failed": "❌ Simulation failed",
        "legal_context": "📚 Legal Context Retrieved (RAG)",
        "round_completed": "Completed",
        "opposing_counsel": "⚔️ Opposing Counsel",
        "defense_lawyer": "🧑‍💼 Defense Lawyer",
        "judges_ruling": "🧑‍⚖️ Judge's Ruling",
        "round": "Round",
        "defense": "Defense",
        "prosecution": "Prosecution",
        "round_winner": "Round Winner",
        "defense_strengths": "✅ Defense strengths",
        "defense_weaknesses": "⚠️ Defense weaknesses",
        "reasoning": "📋 Reasoning",
        "your_turn": "Your Turn",
        "opposing_attack": "⚔️ Opposing Counsel's Attack",
        "choose_strategy": "### 🎯 Your Defense Lawyer suggests 3 strategies. Choose one:",
        "option": "Option",
        "strength": "💡 Strength",
        "select_option": "Select Option",
        "please_select_strategy": "ℹ️ Please select one of the strategies above to proceed",
        "evidence_required": "### 📎 Evidence Required",
        "evidence_reason_default": "Additional evidence will strengthen your case",
        "upload_evidence": "Upload evidence (PDF, Images)",
        "proceed_argument": "✅ Proceed with this argument",
        "spinner_process_argument": "⚖️ Processing your argument...",
        "error_processing_round": "Error processing round",
        "end_hearing": "🛑 End Hearing",
        "cred_check": "Evidence Credibility Check",
        "ai_evidence_analysis_complete": "### 🔍 AI Evidence Analysis Complete",
        "evidence_analysis_info": "Our AI has analyzed the uploaded evidence for credibility, relevance, and potential issues. Review the analysis below before proceeding.",
        "evidence_document": "📄 Evidence Document",
        "credibility_score": "Credibility Score",
        "relevance": "📊 Relevance",
        "authenticity_concerns": "🔐 Authenticity Concerns",
        "admissibility_issues": "⚖️ Admissibility Issues",
        "strategic_value": "💪 Strategic Value",
        "red_flags_identified": "🚩 Red Flags Identified",
        "recommendations": "💡 Recommendations",
        "overall_assessment": "Overall Assessment",
        "skip_evidence": "⏭️ Skip Evidence",
        "spinner_without_evidence": "⚖️ Proceeding without evidence...",
        "use_this_evidence": "✅ Use This Evidence",
        "spinner_incorporate": "📝 Incorporating evidence into argument...",
        "evidence_needed": "Evidence Needed",
        "evidence_request": "📎 Evidence Request",
        "evidence_request_default": "Please upload evidence documents to strengthen your case",
        "submit_evidence_analysis": "📤 Submit Evidence for Analysis",
        "spinner_analyze_evidence": "🔍 Analyzing evidence credibility...",
        "hearing_complete": "✅ Hearing Complete!",
        "final_verdict": "🏛️ Final Verdict",
        "win_probability_defense": "🎯 Win Probability (Defense)",
        "lose": "Lose",
        "win": "Win",
        "strong_points": "✅ Strong Points",
        "weak_points": "⚠️ Weak Points",
        "strategy_suggestions": "💡 Strategy Suggestions",
        "start_new_hearing": "🔄 Start New Hearing"
    },
    "hi": {
        "lang_title": "### 🌐 भाषा",
        "select_interface_language": "इंटरफेस भाषा चुनें",
        "about_app": "**इस ऐप के बारे में:**",
        "about_desc": "यह AI आधारित कोर्टरूम सिमुलेशन आपकी मदद करता है:",
        "about_langs": "**समर्थित भाषाएं:**",
        "header_title": "⚖️ AI कोर्टरूम बैटल सिम्युलेटर",
        "header_subtitle": "इंटरएक्टिव कानूनी तर्क-वितर्क · BNS 2023 · Databricks LLaMA द्वारा संचालित",
        "describe_case": "अपना केस बताएं",
        "case_placeholder": "उदा. मेरे क्लाइंट पर BNS धारा 303 के तहत चोरी का आरोप है...",
        "start_hearing": "⚔️ सुनवाई शुरू करें",
        "warning_enter_case": "⚠️ कृपया सिमुलेशन चलाने से पहले केस विवरण दर्ज करें।",
        "spinner_init": "🔄 इंटरएक्टिव सुनवाई शुरू की जा रही है...",
        "sim_failed": "❌ सिमुलेशन विफल",
        "legal_context": "📚 प्राप्त कानूनी संदर्भ (RAG)",
        "round_completed": "पूर्ण",
        "opposing_counsel": "⚔️ विरोधी वकील",
        "defense_lawyer": "🧑‍💼 बचाव पक्ष वकील",
        "judges_ruling": "🧑‍⚖️ न्यायाधीश का निर्णय",
        "round": "राउंड",
        "defense": "बचाव",
        "prosecution": "अभियोजन",
        "round_winner": "राउंड विजेता",
        "defense_strengths": "✅ बचाव की ताकत",
        "defense_weaknesses": "⚠️ बचाव की कमजोरियां",
        "reasoning": "📋 तर्क",
        "your_turn": "आपकी बारी",
        "opposing_attack": "⚔️ विरोधी वकील का हमला",
        "choose_strategy": "### 🎯 आपका बचाव वकील 3 रणनीतियां सुझाता है। एक चुनें:",
        "option": "विकल्प",
        "strength": "💡 मजबूती",
        "select_option": "विकल्प चुनें",
        "please_select_strategy": "ℹ️ आगे बढ़ने के लिए ऊपर दी गई रणनीतियों में से एक चुनें",
        "evidence_required": "### 📎 साक्ष्य आवश्यक",
        "evidence_reason_default": "अतिरिक्त साक्ष्य आपके केस को मजबूत करेंगे",
        "upload_evidence": "साक्ष्य अपलोड करें (PDF, Images)",
        "proceed_argument": "✅ इस तर्क के साथ आगे बढ़ें",
        "spinner_process_argument": "⚖️ आपके तर्क को प्रोसेस किया जा रहा है...",
        "error_processing_round": "राउंड प्रोसेसिंग में त्रुटि",
        "end_hearing": "🛑 सुनवाई समाप्त करें",
        "cred_check": "साक्ष्य विश्वसनीयता जांच",
        "ai_evidence_analysis_complete": "### 🔍 AI साक्ष्य विश्लेषण पूरा",
        "evidence_analysis_info": "AI ने अपलोड किए गए साक्ष्य की विश्वसनीयता, प्रासंगिकता और संभावित समस्याओं का विश्लेषण किया है। आगे बढ़ने से पहले समीक्षा करें।",
        "evidence_document": "📄 साक्ष्य दस्तावेज",
        "credibility_score": "विश्वसनीयता स्कोर",
        "relevance": "📊 प्रासंगिकता",
        "authenticity_concerns": "🔐 प्रामाणिकता संबंधी चिंताएं",
        "admissibility_issues": "⚖️ स्वीकार्यता संबंधी मुद्दे",
        "strategic_value": "💪 रणनीतिक मूल्य",
        "red_flags_identified": "🚩 पहचाने गए रेड फ्लैग्स",
        "recommendations": "💡 सिफारिशें",
        "overall_assessment": "समग्र आकलन",
        "skip_evidence": "⏭️ साक्ष्य छोड़ें",
        "spinner_without_evidence": "⚖️ साक्ष्य के बिना आगे बढ़ रहे हैं...",
        "use_this_evidence": "✅ इस साक्ष्य का उपयोग करें",
        "spinner_incorporate": "📝 साक्ष्य को तर्क में शामिल किया जा रहा है...",
        "evidence_needed": "साक्ष्य चाहिए",
        "evidence_request": "📎 साक्ष्य अनुरोध",
        "evidence_request_default": "कृपया अपना केस मजबूत करने के लिए साक्ष्य दस्तावेज़ अपलोड करें",
        "submit_evidence_analysis": "📤 विश्लेषण के लिए साक्ष्य सबमिट करें",
        "spinner_analyze_evidence": "🔍 साक्ष्य विश्वसनीयता का विश्लेषण किया जा रहा है...",
        "hearing_complete": "✅ सुनवाई पूर्ण!",
        "final_verdict": "🏛️ अंतिम निर्णय",
        "win_probability_defense": "🎯 जीत की संभावना (बचाव)",
        "lose": "हार",
        "win": "जीत",
        "strong_points": "✅ मजबूत बिंदु",
        "weak_points": "⚠️ कमजोर बिंदु",
        "strategy_suggestions": "💡 रणनीति सुझाव",
        "start_new_hearing": "🔄 नई सुनवाई शुरू करें"
    }
}


def tr(key: str) -> str:
    language = st.session_state.get("selected_language", "en")
    translations = get_ui_translations(language)
    return translations.get(
        key,
        UI_TRANSLATIONS["en"].get(key, key)
    )


def _extract_json_dict(raw_text: str) -> dict:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return {}
    try:
        obj = json.loads(text[start:end + 1])
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _load_persistent_ui_cache() -> dict:
    if not UI_CACHE_FILE.exists():
        return {}
    try:
        with UI_CACHE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_persistent_ui_cache(cache: dict) -> None:
    try:
        with UI_CACHE_FILE.open("w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception:
        # Cache write failures should never block UI rendering.
        pass


def get_ui_translations(language: str) -> dict:
    if language in UI_TRANSLATIONS:
        return UI_TRANSLATIONS[language]

    if language == "en":
        return UI_TRANSLATIONS["en"]

    cache_key = f"ui_translations_{language}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    persistent_cache = _load_persistent_ui_cache()
    if language in persistent_cache and isinstance(persistent_cache[language], dict):
        merged_cached = {
            **UI_TRANSLATIONS["en"],
            **{k: v for k, v in persistent_cache[language].items() if isinstance(v, str)}
        }
        st.session_state[cache_key] = merged_cached
        return merged_cached

    base = UI_TRANSLATIONS["en"]
    prompt = (
        "Translate the JSON values below into the target language for a legal app UI. "
        "Keep keys exactly the same. Preserve emojis and punctuation. "
        "Return ONLY valid JSON object with same keys.\n\n"
        f"Target language code: {language}\n"
        f"JSON:\n{json.dumps(base, ensure_ascii=False)}"
    )

    try:
        translated_raw = ask_llm(prompt, system="You are a professional UI translator. Return strict JSON only.", language=language)
        translated = _extract_json_dict(translated_raw)
        merged = {**base, **{k: v for k, v in translated.items() if isinstance(v, str)}}
        st.session_state[cache_key] = merged

        persistent_cache[language] = {k: v for k, v in merged.items() if isinstance(v, str)}
        _save_persistent_ui_cache(persistent_cache)

        return merged
    except Exception:
        return base

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Courtroom Battle Simulator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed to expanded to show language selector
)

# ─────────────────────────────────────────────
# SIDEBAR - LANGUAGE SELECTOR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(tr("lang_title"))
    
    # Initialize language in session state
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en"

    # Keep widget state aligned with app language state.
    if "language_selector" not in st.session_state:
        st.session_state.language_selector = st.session_state.selected_language
    
    # Language dropdown
    st.selectbox(
        tr("select_interface_language"),
        options=list(LANGUAGE_NAMES.keys()),
        format_func=lambda x: LANGUAGE_NAMES[x],
        key="language_selector"
    )
    
    # Update session state if changed
    if st.session_state.language_selector != st.session_state.selected_language:
        st.session_state.selected_language = st.session_state.language_selector
        # Reset simulation when language changes
        st.session_state.error = None
        st.session_state.interactive_state = None
        st.session_state.round_phase = None
        st.session_state.completed_rounds = []
    
    st.markdown("---")
    st.markdown(f"""
    {tr("about_app")}
    
    {tr("about_desc")}
    * Test legal arguments
    * Analyze evidence credibility
    * Get strategic recommendations
    * Understand case strengths & weaknesses
    
    {tr("about_langs")}
    * English
    * Hindi (हिंदी)
    * Tamil (தமிழ்)
    * Telugu (తెలుగు)
    * Bengali (বাংলা)
    * Marathi (मराठी)
    * Gujarati (ગુજરાતી)
    * Kannada (ಕನ್ನಡ)
    * Malayalam (മലയാളം)
    """)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
        background-color: #0e0f14;
        color: #e8e4d9;
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        text-align: center;
        color: #f0c96b;
        margin-bottom: 0.2rem;
        letter-spacing: 1px;
    }

    .subtitle {
        text-align: center;
        color: #8a8577;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .agent-card {
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    .opponent-card {
        background: linear-gradient(135deg, #2a1010, #1e0e0e);
        border-left: 4px solid #c0392b;
    }

    .lawyer-card {
        background: linear-gradient(135deg, #0f1f10, #0b1a0c);
        border-left: 4px solid #27ae60;
    }

    .judge-card {
        background: linear-gradient(135deg, #141428, #0d0d22);
        border-left: 4px solid #f0c96b;
    }

    .credibility-card {
        background: linear-gradient(135deg, #1a1b24, #14151e);
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    .credibility-high {
        border-color: #27ae60;
    }

    .credibility-medium {
        border-color: #f39c12;
    }

    .credibility-low {
        border-color: #c0392b;
    }

    .credibility-score {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .score-high {
        background: #1a3a1e;
        color: #5dba6e;
        border: 1px solid #2e6b38;
    }

    .score-medium {
        background: #3a2e1a;
        color: #f39c12;
        border: 1px solid #6b4e2e;
    }

    .score-low {
        background: #3a1a1a;
        color: #d96b6b;
        border: 1px solid #7a3030;
    }

    .red-flag-item {
        background: #3a1a1a;
        border-left: 3px solid #c0392b;
        padding: 0.5rem 0.8rem;
        margin: 0.3rem 0;
        border-radius: 4px;
        font-size: 0.9rem;
    }

    .cred-field {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
        padding: 0.6rem;
        margin-bottom: 0.6rem;
    }

    .option-card {
    background: linear-gradient(135deg, #1a1b24, #14151e);
    border: 2px solid #2e3046;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.3s;

    height: 100%;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

    .option-card:hover {
        border-color: #f0c96b;
        box-shadow: 0 0 15px rgba(240, 201, 107, 0.3);
    }

    .option-card.selected {
        border-color: #27ae60;
        background: linear-gradient(135deg, #0f1f10, #0b1a0c);
    }

    .option-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #f0c96b;
        margin-bottom: 0.5rem;
    }

    .option-strength {
        font-size: 0.85rem;
        color: #8a8577;
        font-style: italic;
        margin-top: auto;
    }

    .agent-label {
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .round-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #f0c96b;
        border-bottom: 1px solid #333;
        padding-bottom: 0.4rem;
        margin: 1.5rem 0 1rem 0;
    }

    .score-box {
        display: flex;
        gap: 1rem;
        margin: 0.5rem 0;
    }

    .score-pill {
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.88rem;
    }

    .score-defense { background: #1a3a1e; color: #5dba6e; border: 1px solid #2e6b38; }
    .score-prosecution { background: #3a1a1a; color: #d96b6b; border: 1px solid #7a3030; }

    .win-probability-bar {
        height: 28px;
        border-radius: 14px;
        background: linear-gradient(90deg, #27ae60, #f39c12, #c0392b);
        margin: 0.5rem 0 0.3rem 0;
        position: relative;
        overflow: visible;
    }

    .win-marker {
        position: absolute;
        top: -6px;
        width: 4px;
        height: 40px;
        background: white;
        border-radius: 2px;
        box-shadow: 0 0 8px rgba(255,255,255,0.6);
    }

    .final-card {
        background: #12131a;
        border: 1px solid #2a2b3d;
        border-radius: 14px;
        padding: 1.8rem;
        margin-top: 1.5rem;
    }

    .final-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: #f0c96b;
        margin-bottom: 1rem;
    }

    .point-item {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
    }

    .stTextArea textarea {
        background: #1a1b24 !important;
        color: #e8e4d9 !important;
        border: 1px solid #2e3046 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #f0c96b, #d4a843);
        color: #0e0f14;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2.5rem;
        font-size: 1rem;
        letter-spacing: 0.5px;
        width: 100%;
        transition: opacity 0.2s;
    }

    .stButton > button:hover { opacity: 0.85; }

    .stSelectbox > div > div {
        background: #1a1b24 !important;
        color: #e8e4d9 !important;
        border: 1px solid #2e3046 !important;
        border-radius: 8px !important;
    }

    .divider {
        border: none;
        border-top: 1px solid #1e2030;
        margin: 2rem 0;
    }

    .winner-badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .badge-defense { background: #1a3a1e; color: #5dba6e; }
    .badge-prosecution { background: #3a1a1a; color: #d96b6b; }
    .badge-tie { background: #2a2b1a; color: #d4c46b; }

    .evidence-box {
        background: #1a1b24;
        border: 2px dashed #f0c96b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }

    .end-hearing-btn button {
        background: linear-gradient(135deg, #c0392b, #962d22) !important;
        color: white !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #12131a;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e8e4d9;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown(f'<div class="main-title">{tr("header_title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{tr("header_subtitle")}</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────

user_case = st.text_area(
    tr("describe_case"),
    placeholder=tr("case_placeholder"),
    height=160,
    label_visibility="visible"
)

st.markdown("<br>", unsafe_allow_html=True)
run_btn = st.button(tr("start_hearing"))


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "error" not in st.session_state:
    st.session_state.error = None

if "interactive_state" not in st.session_state:
    st.session_state.interactive_state = None

if "round_phase" not in st.session_state:
    st.session_state.round_phase = None

if "completed_rounds" not in st.session_state:
    st.session_state.completed_rounds = []


# ─────────────────────────────────────────────
# RESET HELPER
# ─────────────────────────────────────────────

def reset_simulation():
    st.session_state.error = None
    st.session_state.interactive_state = None
    st.session_state.round_phase = None
    st.session_state.completed_rounds = []


# ─────────────────────────────────────────────
# RUN SIMULATION
# ─────────────────────────────────────────────

if run_btn:
    if not user_case.strip():
        st.warning(tr("warning_enter_case"))
    else:
        reset_simulation()
        
        # Get selected language
        language = st.session_state.selected_language
        
        # Interactive mode - continuous until user ends
        with st.spinner(tr("spinner_init")):
            try:
                state = start_interactive_simulation(user_case.strip(), language)
                st.session_state.interactive_state = state
                
                # Start first round
                round_result = run_interactive_round(state)
                st.session_state.round_phase = round_result
                
            except Exception as e:
                st.session_state.error = str(e)


# ─────────────────────────────────────────────
# ERROR DISPLAY
# ─────────────────────────────────────────────

if st.session_state.error:
    st.error(f"{tr('sim_failed')}: {st.session_state.error}")


# ─────────────────────────────────────────────
# INTERACTIVE MODE HANDLING
# ─────────────────────────────────────────────

if st.session_state.interactive_state and st.session_state.round_phase:
    state = st.session_state.interactive_state
    phase = st.session_state.round_phase
    language = state.get("language", "en")
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # Show context
    if st.session_state.completed_rounds == []:
        with st.expander(tr("legal_context"), expanded=False):
            st.markdown(f"<div style='color:#8a8577; font-size:0.87rem; line-height:1.7'>{state['context'][:400]}...</div>", unsafe_allow_html=True)
    
    # Display completed rounds
    for round_data in st.session_state.completed_rounds:
        rn = round_data["round"]
        judge = round_data["judge"]
        
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {rn} - {tr("round_completed")}</div>', unsafe_allow_html=True)
        
        col_opp, col_law = st.columns(2)
        
        with col_opp:
            st.markdown(f"""
            <div class="agent-card opponent-card">
                <div class="agent-label" style="color:#c0392b">{tr("opposing_counsel")}</div>
                {round_data['opponent']}
            </div>
            """, unsafe_allow_html=True)
        
        with col_law:
            st.markdown(f"""
            <div class="agent-card lawyer-card">
                <div class="agent-label" style="color:#27ae60">{tr("defense_lawyer")}</div>
                {round_data['lawyer']}
            </div>
            """, unsafe_allow_html=True)
        
        # Judge evaluation
        d_score = judge.get("defense_score", "?")
        p_score = judge.get("prosecution_score", "?")
        winner = judge.get("round_winner", "tie")
        badge_cls = {"defense": "badge-defense", "prosecution": "badge-prosecution"}.get(winner, "badge-tie")
        badge_label = winner.upper()
        
        st.markdown(f"""
        <div class="agent-card judge-card">
            <div class="agent-label" style="color:#f0c96b">{tr("judges_ruling")} — {tr("round")} {rn}</div>
            <div style="margin-bottom:0.6rem">
                <span class="score-pill score-defense">{tr("defense")}: {d_score}/10</span>&nbsp;
                <span class="score-pill score-prosecution">{tr("prosecution")}: {p_score}/10</span>&nbsp;
                <span class="winner-badge {badge_cls}">{tr("round_winner")}: {badge_label}</span>
            </div>
            <div style="margin-bottom:0.4rem"><strong>{tr("defense_strengths")}:</strong> {judge.get("defense_strengths", "—")}</div>
            <div style="margin-bottom:0.4rem"><strong>{tr("defense_weaknesses")}:</strong> {judge.get("defense_weaknesses", "—")}</div>
            <div style="margin-bottom:0.4rem"><strong>{tr("reasoning")}:</strong> {judge.get("reasoning", "—")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current round
    current_round_num = state["current_round"]
    
    if phase["status"] == "awaiting_choice":
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {current_round_num} - {tr("your_turn")}</div>', unsafe_allow_html=True)
        
        # Show opponent's attack
        st.markdown(f"""
        <div class="agent-card opponent-card">
            <div class="agent-label" style="color:#c0392b">{tr("opposing_attack")}</div>
            {phase['opponent_attack']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(tr("choose_strategy"))
        
        # Display all options in columns
        cols = st.columns(3)

        selected_option_id = None

        for idx, opt in enumerate(phase['options']):
            with cols[idx]:
                is_selected = st.session_state.get(f"selected_opt_{current_round_num}", None) == opt['id']
                card_style = "option-card selected" if is_selected else "option-card"

                st.markdown(f"""
                <div class="{card_style}">
                    <div class="option-title">{tr("option")} {opt['id']}: {opt['title']}</div>
                    <div style="margin: 0.8rem 0; line-height:1.6; flex-grow:1">{opt['argument']}</div>
                    <div class="option-strength">{tr("strength")}: {opt['strength']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{tr('select_option')} {opt['id']}", key=f"select_opt_{opt['id']}_r{current_round_num}", use_container_width=True):
                    st.session_state[f"selected_opt_{current_round_num}"] = opt['id']
                    

        selected_option_id = st.session_state.get(f"selected_opt_{current_round_num}", None)
        
        # Get selected option
        selected_option_id = st.session_state.get(f"selected_opt_{current_round_num}", None)
        
        if selected_option_id is None:
            st.info(tr("please_select_strategy"))
            selected_opt = None
        else:
            selected_opt = next(opt for opt in phase['options'] if opt['id'] == selected_option_id)

        # Show evidence request if needed
        evidence_files = None
        if phase.get('needs_evidence'):
            st.markdown(tr("evidence_required"))
            st.info(f"💡 {phase.get('evidence_reason', tr('evidence_reason_default'))}")
            
            evidence_files = st.file_uploader(
                tr("upload_evidence"),
                type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
                accept_multiple_files=True,
                key="evidence_uploader"
            )
        
        # Buttons row
        col_proceed, col_end = st.columns([3, 1])
        
        with col_proceed:
            proceed_disabled = selected_option_id is None
            if st.button(tr("proceed_argument"), key="proceed_btn", disabled=proceed_disabled):
                with st.spinner(tr("spinner_process_argument")):
                    try:
                        # Run round with selection
                        round_result = run_interactive_round(
                            state,
                            selected_option_id=selected_option_id,
                            evidence_files=evidence_files
                        )
                        
                        if round_result["status"] == "awaiting_evidence":
                            st.session_state.round_phase = round_result
                           
                        
                        elif round_result["status"] == "checking_credibility":
                            st.session_state.round_phase = round_result
                            
                        
                        elif round_result["status"] == "round_complete":
                            st.session_state.completed_rounds.append(round_result["round_data"])
                            
                            # Always continue to next round (no limit)
                            next_round_result = run_interactive_round(state)
                            st.session_state.round_phase = next_round_result
                            
                    
                    except Exception as e:
                        st.error(f"{tr('error_processing_round')}: {str(e)}")
        
        with col_end:
            st.markdown('<div class="end-hearing-btn">', unsafe_allow_html=True)
            if st.button(tr("end_hearing"), key="end_hearing_btn"):
                # End the simulation and show final verdict
                st.session_state.round_phase = {"status": "simulation_complete"}
               
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif phase["status"] == "checking_credibility":
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {current_round_num} - {tr("cred_check")}</div>', unsafe_allow_html=True)
        
        st.markdown(tr("ai_evidence_analysis_complete"))
        st.info(tr("evidence_analysis_info"))
        
        credibility_reports = phase.get("credibility_reports", [])
        
        for i, report in enumerate(credibility_reports):
            score = report.get("credibility_score", 5)
            
            # Determine score class
            if score >= 7:
                score_class = "score-high"
                card_class = "credibility-high"
            elif score >= 4:
                score_class = "score-medium"
                card_class = "credibility-medium"
            else:
                score_class = "score-low"
                card_class = "credibility-low"
            
            # Document header
            st.markdown(f"""
            <div class="credibility-card {card_class}">
                <div class="agent-label" style="color:#3498db">{tr("evidence_document")} {i+1}</div>
                <div style="margin-bottom:1rem">
                    <span class="credibility-score {score_class}">{tr("credibility_score")}: {score}/10</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Display fields using streamlit components to avoid HTML rendering issues
            st.markdown(f"**{tr('relevance')}:** {report.get('relevance', 'N/A')}")
            st.markdown(f"**{tr('authenticity_concerns')}:** {report.get('authenticity_concerns', 'N/A')}")
            st.markdown(f"**{tr('admissibility_issues')}:** {report.get('admissibility_issues', 'N/A')}")
            st.markdown(f"**{tr('strategic_value')}:** {report.get('strategic_value', 'N/A')}")
            
            # Red flags
            red_flags = report.get("red_flags", [])
            if red_flags:
                st.markdown(f"**{tr('red_flags_identified')}:**")
                for flag in red_flags:
                    st.markdown(f'<div class="red-flag-item">⚠️ {flag}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**{tr('recommendations')}:** {report.get('recommendations', 'N/A')}")
            st.markdown("---")
            st.markdown(f"*{tr('overall_assessment')}:* {report.get('overall_assessment', 'N/A')}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Two buttons: Skip or Use Evidence
        col_skip, col_use = st.columns(2)
        
        with col_skip:
            if st.button(tr("skip_evidence"), key="skip_after_cred"):
                with st.spinner(tr("spinner_without_evidence")):
                    # Clear credibility state and proceed without evidence
                    if "credibility_reports" in state:
                        del state["credibility_reports"]
                    if "evidence_texts" in state:
                        del state["evidence_texts"]
                    
                    # Re-run the round without evidence
                    round_result = run_interactive_round(state)
                    
                    if round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])
                        
                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result
                    
                    
        
        with col_use:
            if st.button(tr("use_this_evidence"), key="use_evidence"):
                with st.spinner(tr("spinner_incorporate")):
                    # Proceed with evidence
                    round_result = run_interactive_round(state)
                    
                    if round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])
                        
                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result
                    
                    
    
    elif phase["status"] == "awaiting_evidence":
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {current_round_num} - {tr("evidence_needed")}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="evidence-box">
            <h3 style="color:#f0c96b; margin-bottom:1rem">{tr("evidence_request")}</h3>
            <p>{phase.get('reason', tr('evidence_request_default'))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        evidence_files = st.file_uploader(
            tr("upload_evidence"),
            type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
            accept_multiple_files=True,
            key="evidence_uploader_2"
        )
        
        col_skip, col_submit = st.columns(2)
        
        with col_skip:
            if st.button(tr("skip_evidence"), key="skip_evidence"):
                with st.spinner(tr("spinner_without_evidence")):
                    round_result = run_interactive_round(state, evidence_files=None)
                    
                    if round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])
                        
                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result
                    
                    
        
        with col_submit:
            if st.button(tr("submit_evidence_analysis"), key="submit_evidence") and evidence_files:
                with st.spinner(tr("spinner_analyze_evidence")):
                    round_result = run_interactive_round(state, evidence_files=evidence_files)
                    
                    if round_result["status"] == "checking_credibility":
                        st.session_state.round_phase = round_result
                        
                    elif round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])
                        
                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result
                        
                        
    
    elif phase["status"] == "simulation_complete":
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.success(tr("hearing_complete"))
        
        # Calculate final verdict
        final = compute_win_probability(state["round_results"], language)
        win_prob = final["win_probability"]
        
        st.markdown(f'<div class="final-title">{tr("final_verdict")}</div>', unsafe_allow_html=True)
        
        # Win probability bar
        st.markdown(f"**{tr('win_probability_defense')}**")
        marker_left = max(2, min(97, win_prob))
        st.markdown(f"""
        <div class="win-probability-bar">
            <div class="win-marker" style="left:{marker_left}%"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#8a8577; margin-bottom:0.8rem">
            <span>0% ({tr('lose')})</span>
            <span style="font-size:1.2rem; font-weight:700; color:{'#27ae60' if win_prob >= 55 else '#c0392b' if win_prob < 45 else '#f0c96b'}">{win_prob}%</span>
            <span>100% ({tr('win')})</span>
        </div>
        """, unsafe_allow_html=True)
        
        col_s, col_w, col_sg = st.columns(3)
        
        with col_s:
            st.markdown(f"**{tr('strong_points')}**")
            for pt in final.get("strong_points", []):
                if pt:
                    st.markdown(f"<div class='point-item'><span style='color:#27ae60'>▸</span> {pt}</div>", unsafe_allow_html=True)
        
        with col_w:
            st.markdown(f"**{tr('weak_points')}**")
            for pt in final.get("weak_points", []):
                if pt:
                    st.markdown(f"<div class='point-item'><span style='color:#e67e22'>▸</span> {pt}</div>", unsafe_allow_html=True)
        
        with col_sg:
            st.markdown(f"**{tr('strategy_suggestions')}**")
            for sug in final.get("suggestions", []):
                if sug:
                    st.markdown(f"<div class='point-item'><span style='color:#f0c96b'>▸</span> {sug}</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(tr("start_new_hearing")):
            reset_simulation()
            st.rerun()
