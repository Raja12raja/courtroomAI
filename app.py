import streamlit as st
from backend import (
    start_interactive_simulation,
    run_interactive_round,
    compute_win_probability,
    LANGUAGE_NAMES
)


UI_TRANSLATIONS = {
    "en": {
        "sidebar_language": "### 🌐 Language / भाषा",
        "select_interface_language": "Select Interface Language",
        "about_app": "About This App",
        "about_points": """
An AI-powered courtroom simulation that helps you:
* Test legal arguments
* Analyze evidence credibility
* Get strategic recommendations
* Understand case strengths & weaknesses
""",
        "supported_languages": "Supported Languages",
        "main_title": "⚖️ AI Courtroom  ",
        "subtitle": "Interactive adversarial legal reasoning · BNS 2023 · Powered by Databricks LLaMA",
        "describe_case": "Describe your case",
        "case_placeholder": "e.g. My client is accused of theft under BNS Section 303. The only evidence is CCTV footage from a store, however the footage quality is poor and the identity is unclear. There are no eyewitnesses...",
        "start_hearing": "⚔️ Start Hearing",
        "enter_case_warning": "⚠️ Please enter your case description before running the simulation.",
        "initializing_hearing": "🔄 Initializing interactive hearing...",
        "simulation_failed": "❌ Simulation failed",
        "legal_context": "📚 Legal Context Retrieved (RAG)",
        "round_completed": "Completed",
        "your_turn": "Your Turn",
        "opposing_counsel": "⚔️ Opposing Counsel",
        "opposing_attack": "⚔️ Opposing Counsel's Attack",
        "defense_lawyer": "🧑‍💼 Defense Lawyer",
        "judge_ruling": "🧑‍⚖️ Judge's Ruling",
        "defense": "Defense",
        "prosecution": "Prosecution",
        "round_winner": "Round Winner",
        "defense_strengths": "✅ Defense strengths",
        "defense_weaknesses": "⚠️ Defense weaknesses",
        "reasoning": "📋 Reasoning",
        "choose_strategy": "### 🎯 Your Defense Lawyer suggests 3 strategies. Choose one:",
        "option": "Option",
        "strength": "💡 Strength",
        "select_option": "Select Option",
        "select_strategy_info": "ℹ️ Please select one of the strategies above to proceed",
        "evidence_required": "### 📎 Evidence Required",
        "additional_evidence_help": "Additional evidence will strengthen your case",
        "upload_evidence": "Upload evidence (PDF, Images)",
        "proceed_argument": "✅ Proceed with this argument",
        "processing_argument": "⚖️ Processing your argument...",
        "end_hearing": "🛑 End Hearing",
        "credibility_check": "Evidence Credibility Check",
        "ai_evidence_complete": "### 🔍 AI Evidence Analysis Complete",
        "ai_evidence_info": "Our AI has analyzed the uploaded evidence for credibility, relevance, and potential issues. Review the analysis below before proceeding.",
        "evidence_document": "📄 Evidence Document",
        "credibility_score": "Credibility Score",
        "relevance": "📊 Relevance",
        "authenticity_concerns": "🔐 Authenticity Concerns",
        "admissibility_issues": "⚖️ Admissibility Issues",
        "strategic_value": "💪 Strategic Value",
        "red_flags": "🚩 Red Flags Identified",
        "recommendations": "💡 Recommendations",
        "overall_assessment": "Overall Assessment",
        "skip_evidence": "⏭️ Skip Evidence",
        "proceed_without_evidence": "⚖️ Proceeding without evidence...",
        "use_evidence": "✅ Use This Evidence",
        "incorporating_evidence": "📝 Incorporating evidence into argument...",
        "evidence_needed": "Evidence Needed",
        "evidence_request": "📎 Evidence Request",
        "upload_evidence_prompt": "Please upload evidence documents to strengthen your case",
        "submit_evidence": "📤 Submit Evidence for Analysis",
        "analyzing_evidence": "🔍 Analyzing evidence credibility...",
        "hearing_complete": "✅ Hearing Complete!",
        "final_verdict": "🏛️ Final Verdict",
        "win_probability_defense": "🎯 Win Probability (Defense)",
        "lose": "Lose",
        "win": "Win",
        "strong_points": "✅ Strong Points",
        "weak_points": "⚠️ Weak Points",
        "strategy_suggestions": "💡 Strategy Suggestions",
        "start_new_hearing": "🔄 Start New Hearing",
        "error_processing_round": "Error processing round"
    },
    "hi": {
        "sidebar_language": "### 🌐 भाषा / Language",
        "select_interface_language": "इंटरफ़ेस भाषा चुनें",
        "about_app": "इस ऐप के बारे में",
        "about_points": """
यह AI-आधारित कोर्टरूम सिमुलेशन आपकी मदद करता है:
* कानूनी तर्कों का परीक्षण
* साक्ष्य की विश्वसनीयता का विश्लेषण
* रणनीतिक सुझाव प्राप्त करना
* केस की ताकत और कमजोरियां समझना
""",
        "supported_languages": "समर्थित भाषाएं",
        "main_title": "⚖️ AI कोर्टरूम बैटल सिमुलेटर",
        "subtitle": "इंटरैक्टिव प्रतिद्वंद्वी कानूनी तर्क · BNS 2023 · Databricks LLaMA द्वारा संचालित",
        "describe_case": "अपना केस लिखें",
        "case_placeholder": "उदा. मेरे क्लाइंट पर BNS धारा 303 के तहत चोरी का आरोप है। एकमात्र सबूत दुकान का CCTV फुटेज है, लेकिन फुटेज की गुणवत्ता खराब है और पहचान स्पष्ट नहीं है...",
        "start_hearing": "⚔️ सुनवाई शुरू करें",
        "enter_case_warning": "⚠️ सिमुलेशन चलाने से पहले अपना केस विवरण दर्ज करें।",
        "initializing_hearing": "🔄 इंटरैक्टिव सुनवाई प्रारंभ हो रही है...",
        "simulation_failed": "❌ सिमुलेशन विफल",
        "legal_context": "📚 प्राप्त कानूनी संदर्भ (RAG)",
        "round_completed": "पूरा",
        "your_turn": "आपकी बारी",
        "opposing_counsel": "⚔️ विपक्षी वकील",
        "opposing_attack": "⚔️ विपक्षी वकील का हमला",
        "defense_lawyer": "🧑‍💼 बचाव पक्ष का वकील",
        "judge_ruling": "🧑‍⚖️ न्यायाधीश का निर्णय",
        "defense": "बचाव",
        "prosecution": "अभियोजन",
        "round_winner": "राउंड विजेता",
        "defense_strengths": "✅ बचाव की मजबूतियां",
        "defense_weaknesses": "⚠️ बचाव की कमजोरियां",
        "reasoning": "📋 तर्क",
        "choose_strategy": "### 🎯 आपका बचाव वकील 3 रणनीतियां सुझाता है। एक चुनें:",
        "option": "विकल्प",
        "strength": "💡 ताकत",
        "select_option": "विकल्प चुनें",
        "select_strategy_info": "ℹ️ आगे बढ़ने के लिए ऊपर दी गई रणनीतियों में से एक चुनें",
        "evidence_required": "### 📎 साक्ष्य आवश्यक",
        "additional_evidence_help": "अतिरिक्त साक्ष्य आपके केस को मजबूत करेंगे",
        "upload_evidence": "साक्ष्य अपलोड करें (PDF, Images)",
        "proceed_argument": "✅ इसी तर्क के साथ आगे बढ़ें",
        "processing_argument": "⚖️ आपके तर्क को प्रोसेस किया जा रहा है...",
        "end_hearing": "🛑 सुनवाई समाप्त करें",
        "credibility_check": "साक्ष्य विश्वसनीयता जांच",
        "ai_evidence_complete": "### 🔍 AI साक्ष्य विश्लेषण पूरा",
        "ai_evidence_info": "AI ने अपलोड किए गए साक्ष्य की विश्वसनीयता, प्रासंगिकता और संभावित समस्याओं का विश्लेषण किया है। आगे बढ़ने से पहले समीक्षा करें।",
        "evidence_document": "📄 साक्ष्य दस्तावेज़",
        "credibility_score": "विश्वसनीयता स्कोर",
        "relevance": "📊 प्रासंगिकता",
        "authenticity_concerns": "🔐 प्रामाणिकता संबंधी चिंताएं",
        "admissibility_issues": "⚖️ ग्राह्यता संबंधी मुद्दे",
        "strategic_value": "💪 रणनीतिक मूल्य",
        "red_flags": "🚩 चेतावनी संकेत",
        "recommendations": "💡 सिफारिशें",
        "overall_assessment": "समग्र आकलन",
        "skip_evidence": "⏭️ साक्ष्य छोड़ें",
        "proceed_without_evidence": "⚖️ साक्ष्य के बिना आगे बढ़ रहे हैं...",
        "use_evidence": "✅ इन साक्ष्यों का उपयोग करें",
        "incorporating_evidence": "📝 तर्क में साक्ष्य जोड़े जा रहे हैं...",
        "evidence_needed": "साक्ष्य आवश्यक",
        "evidence_request": "📎 साक्ष्य अनुरोध",
        "upload_evidence_prompt": "कृपया अपना केस मजबूत करने के लिए साक्ष्य दस्तावेज़ अपलोड करें",
        "submit_evidence": "📤 विश्लेषण के लिए साक्ष्य जमा करें",
        "analyzing_evidence": "🔍 साक्ष्य विश्वसनीयता का विश्लेषण हो रहा है...",
        "hearing_complete": "✅ सुनवाई पूर्ण!",
        "final_verdict": "🏛️ अंतिम निर्णय",
        "win_probability_defense": "🎯 जीत की संभावना (बचाव)",
        "lose": "हार",
        "win": "जीत",
        "strong_points": "✅ मजबूत बिंदु",
        "weak_points": "⚠️ कमजोर बिंदु",
        "strategy_suggestions": "💡 रणनीति सुझाव",
        "start_new_hearing": "🔄 नई सुनवाई शुरू करें",
        "error_processing_round": "राउंड प्रोसेस करने में त्रुटि"
    },
    "ta": {
        "select_interface_language": "இடைமுக மொழியை தேர்வு செய்யவும்",
        "main_title": "⚖️ AI நீதிமன்ற போராட்ட சிமுலேட்டர்",
        "describe_case": "உங்கள் வழக்கை விவரிக்கவும்",
        "start_hearing": "⚔️ விசாரணையை தொடங்கு",
        "your_turn": "உங்கள் முறை",
        "proceed_argument": "✅ இந்த வாதத்துடன் தொடரவும்",
        "end_hearing": "🛑 விசாரணையை முடிக்கவும்",
        "skip_evidence": "⏭️ ஆதாரத்தை தவிர்க்கவும்",
        "use_evidence": "✅ இந்த ஆதாரத்தை பயன்படுத்தவும்",
        "submit_evidence": "📤 பகுப்பாய்வுக்காக ஆதாரம் சமர்ப்பிக்கவும்",
        "hearing_complete": "✅ விசாரணை முடிந்தது!",
        "final_verdict": "🏛️ இறுதி தீர்ப்பு",
        "strong_points": "✅ வலுவான புள்ளிகள்",
        "weak_points": "⚠️ பலவீனமான புள்ளிகள்",
        "strategy_suggestions": "💡 மூலோபாய பரிந்துரைகள்",
        "start_new_hearing": "🔄 புதிய விசாரணையை தொடங்கு"
    },
    "te": {
        "select_interface_language": "ఇంటర్ఫేస్ భాషను ఎంచుకోండి",
        "main_title": "⚖️ AI కోర్ట్‌రూమ్ బ్యాటిల్ సిమ్యులేటర్",
        "describe_case": "మీ కేసును వివరించండి",
        "start_hearing": "⚔️ విచారణ ప్రారంభించండి",
        "your_turn": "మీ వంతు",
        "proceed_argument": "✅ ఈ వాదనతో కొనసాగండి",
        "end_hearing": "🛑 విచారణ ముగించండి",
        "skip_evidence": "⏭️ సాక్ష్యాన్ని దాటవేయండి",
        "use_evidence": "✅ ఈ సాక్ష్యాన్ని ఉపయోగించండి",
        "submit_evidence": "📤 విశ్లేషణ కోసం సాక్ష్యం సమర్పించండి",
        "hearing_complete": "✅ విచారణ పూర్తైంది!",
        "final_verdict": "🏛️ తుది తీర్పు",
        "strong_points": "✅ బలమైన అంశాలు",
        "weak_points": "⚠️ బలహీన అంశాలు",
        "strategy_suggestions": "💡 వ్యూహ సూచనలు",
        "start_new_hearing": "🔄 కొత్త విచారణ ప్రారంభించండి"
    },
    "bn": {
        "select_interface_language": "ইন্টারফেস ভাষা নির্বাচন করুন",
        "main_title": "⚖️ AI কোর্টরুম ব্যাটল সিমুলেটর",
        "describe_case": "আপনার কেস বর্ণনা করুন",
        "start_hearing": "⚔️ শুনানি শুরু করুন",
        "your_turn": "আপনার পালা",
        "proceed_argument": "✅ এই যুক্তি নিয়ে এগিয়ে যান",
        "end_hearing": "🛑 শুনানি শেষ করুন",
        "skip_evidence": "⏭️ প্রমাণ বাদ দিন",
        "use_evidence": "✅ এই প্রমাণ ব্যবহার করুন",
        "submit_evidence": "📤 বিশ্লেষণের জন্য প্রমাণ জমা দিন",
        "hearing_complete": "✅ শুনানি সম্পন্ন!",
        "final_verdict": "🏛️ চূড়ান্ত রায়",
        "strong_points": "✅ শক্তিশালী দিক",
        "weak_points": "⚠️ দুর্বল দিক",
        "strategy_suggestions": "💡 কৌশলগত পরামর্শ",
        "start_new_hearing": "🔄 নতুন শুনানি শুরু করুন"
    },
    "mr": {
        "select_interface_language": "इंटरफेस भाषा निवडा",
        "main_title": "⚖️ AI न्यायालयीन बॅटल सिम्युलेटर",
        "describe_case": "तुमचे प्रकरण वर्णन करा",
        "start_hearing": "⚔️ सुनावणी सुरू करा",
        "your_turn": "तुमची पाळी",
        "proceed_argument": "✅ या युक्तिवादासह पुढे जा",
        "end_hearing": "🛑 सुनावणी समाप्त करा",
        "skip_evidence": "⏭️ पुरावा वगळा",
        "use_evidence": "✅ हा पुरावा वापरा",
        "submit_evidence": "📤 विश्लेषणासाठी पुरावा सादर करा",
        "hearing_complete": "✅ सुनावणी पूर्ण!",
        "final_verdict": "🏛️ अंतिम निकाल",
        "strong_points": "✅ मजबूत मुद्दे",
        "weak_points": "⚠️ कमकुवत मुद्दे",
        "strategy_suggestions": "💡 धोरणात्मक सूचना",
        "start_new_hearing": "🔄 नवीन सुनावणी सुरू करा"
    },
    "gu": {
        "select_interface_language": "ઇન્ટરફેસ ભાષા પસંદ કરો",
        "main_title": "⚖️ AI કોર્ટરૂમ બેટલ સિમ્યુલેટર",
        "describe_case": "તમારો કેસ વર્ણવો",
        "start_hearing": "⚔️ સુનાવણી શરૂ કરો",
        "your_turn": "તમારો વારો",
        "proceed_argument": "✅ આ દલીલ સાથે આગળ વધો",
        "end_hearing": "🛑 સુનાવણી સમાપ્ત કરો",
        "skip_evidence": "⏭️ પુરાવો છોડો",
        "use_evidence": "✅ આ પુરાવાનો ઉપયોગ કરો",
        "submit_evidence": "📤 વિશ્લેષણ માટે પુરાવો સબમિટ કરો",
        "hearing_complete": "✅ સુનાવણી પૂર્ણ!",
        "final_verdict": "🏛️ અંતિમ ચુકાદો",
        "strong_points": "✅ મજબૂત મુદ્દાઓ",
        "weak_points": "⚠️ નબળા મુદ્દાઓ",
        "strategy_suggestions": "💡 વ્યૂહાત્મક સૂચનો",
        "start_new_hearing": "🔄 નવી સુનાવણી શરૂ કરો"
    },
    "kn": {
        "select_interface_language": "ಇಂಟರ್ಫೇಸ್ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "main_title": "⚖️ AI ನ್ಯಾಯಾಲಯ ಬ್ಯಾಟಲ್ ಸಿಮ್ಯುಲೇಟರ್",
        "describe_case": "ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು ವಿವರಿಸಿ",
        "start_hearing": "⚔️ ವಿಚಾರಣೆಯನ್ನು ಪ್ರಾರಂಭಿಸಿ",
        "your_turn": "ನಿಮ್ಮ ಬಾರಿ",
        "proceed_argument": "✅ ಈ ವಾದದೊಂದಿಗೆ ಮುಂದುವರಿಯಿರಿ",
        "end_hearing": "🛑 ವಿಚಾರಣೆಯನ್ನು ಮುಗಿಸಿ",
        "skip_evidence": "⏭️ ಸಾಕ್ಷ್ಯವನ್ನು ಬಿಟ್ಟುಬಿಡಿ",
        "use_evidence": "✅ ಈ ಸಾಕ್ಷ್ಯವನ್ನು ಬಳಸಿ",
        "submit_evidence": "📤 ವಿಶ್ಲೇಷಣೆಗೆ ಸಾಕ್ಷ್ಯವನ್ನು ಸಲ್ಲಿಸಿ",
        "hearing_complete": "✅ ವಿಚಾರಣೆ ಪೂರ್ಣಗೊಂಡಿದೆ!",
        "final_verdict": "🏛️ ಅಂತಿಮ ತೀರ್ಪು",
        "strong_points": "✅ ಬಲವಾದ ಅಂಶಗಳು",
        "weak_points": "⚠️ ದುರ್ಬಲ ಅಂಶಗಳು",
        "strategy_suggestions": "💡 ತಂತ್ರಾತ್ಮಕ ಸಲಹೆಗಳು",
        "start_new_hearing": "🔄 ಹೊಸ ವಿಚಾರಣೆಯನ್ನು ಪ್ರಾರಂಭಿಸಿ"
    },
    "ml": {
        "select_interface_language": "ഇന്റർഫേസ് ഭാഷ തിരഞ്ഞെടുക്കുക",
        "main_title": "⚖️ AI കോടതി ബാറ്റിൽ സിമുലേറ്റർ",
        "describe_case": "നിങ്ങളുടെ കേസ് വിശദീകരിക്കുക",
        "start_hearing": "⚔️ ഹിയറിംഗ് ആരംഭിക്കുക",
        "your_turn": "നിങ്ങളുടെ ടേൺ",
        "proceed_argument": "✅ ഈ വാദവുമായി തുടരുക",
        "end_hearing": "🛑 ഹിയറിംഗ് അവസാനിപ്പിക്കുക",
        "skip_evidence": "⏭️ തെളിവ് ഒഴിവാക്കുക",
        "use_evidence": "✅ ഈ തെളിവ് ഉപയോഗിക്കുക",
        "submit_evidence": "📤 വിശകലനത്തിനായി തെളിവ് സമർപ്പിക്കുക",
        "hearing_complete": "✅ ഹിയറിംഗ് പൂർത്തിയായി!",
        "final_verdict": "🏛️ അന്തിമ വിധി",
        "strong_points": "✅ ശക്തമായ പോയിന്റുകൾ",
        "weak_points": "⚠️ ദുർബല പോയിന്റുകൾ",
        "strategy_suggestions": "💡 തന്ത്ര നിർദേശങ്ങൾ",
        "start_new_hearing": "🔄 പുതിയ ഹിയറിംഗ് ആരംഭിക്കുക"
    }
}


def tr(key: str, language: str = None) -> str:
    lang = language or st.session_state.get("selected_language", "en")
    lang_table = UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS["en"])
    return lang_table.get(key, UI_TRANSLATIONS["en"].get(key, key))

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Courtroom ",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed to expanded to show language selector
)

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "en"

# ─────────────────────────────────────────────
# SIDEBAR - LANGUAGE SELECTOR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown(tr("sidebar_language"))
    
    # Language dropdown
    selected_lang = st.selectbox(
        tr("select_interface_language"),
        options=list(LANGUAGE_NAMES.keys()),
        format_func=lambda x: LANGUAGE_NAMES[x],
        index=list(LANGUAGE_NAMES.keys()).index(st.session_state.selected_language),
        key="language_selector"
    )
    
    # Update session state if changed
    if selected_lang != st.session_state.selected_language:
        st.session_state.selected_language = selected_lang
        # Reset simulation when language changes
        st.session_state.error = None
        st.session_state.interactive_state = None
        st.session_state.round_phase = None
        st.session_state.completed_rounds = []
        st.rerun()
    
    st.markdown("---")
    supported_langs = "\n".join([f"* {name}" for name in LANGUAGE_NAMES.values()])
    st.markdown(
        f"**{tr('about_app')}**\n\n"
        f"{tr('about_points')}\n"
        f"**{tr('supported_languages')}:**\n"
        f"{supported_langs}"
    )

    st.markdown("---")
    if "show_dashboard" not in st.session_state:
        st.session_state.show_dashboard = False

    if st.button("📊 Toggle Analytics Dashboard", key="toggle_dashboard_btn"):
        st.session_state.show_dashboard = not st.session_state.show_dashboard
        st.rerun()

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

st.markdown(f'<div class="main-title">{tr("main_title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{tr("subtitle")}</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if st.session_state.get("show_dashboard", False):
        st.markdown("### 📊 Analytics Dashboard")
        st.components.v1.html(
                """
                <iframe
                    src="https://dbc-ff1aed05-a06b.cloud.databricks.com/embed/dashboardsv3/01f13afc66f8112fad1f288fe02a2573?o=7474657629287924"
                    width="100%"
                    height="600"
                    frameborder="0">
                </iframe>
                """,
                height=620,
                scrolling=True,
        )
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

if "scroll_to_proceed" not in st.session_state:
    st.session_state.scroll_to_proceed = False


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
        st.warning(tr("enter_case_warning"))
    else:
        reset_simulation()
        
        # Get selected language
        language = st.session_state.selected_language
        
        # Interactive mode - continuous until user ends
        with st.spinner(tr("initializing_hearing")):
            try:
                state = start_interactive_simulation(user_case.strip(), language)
                st.session_state.interactive_state = state
                
                # Start first round
                round_result = run_interactive_round(state)
                st.session_state.round_phase = round_result
                st.rerun()
                
            except Exception as e:
                st.session_state.error = str(e)


# ─────────────────────────────────────────────
# ERROR DISPLAY
# ─────────────────────────────────────────────

if st.session_state.error:
    st.error(f"{tr('simulation_failed')}: {st.session_state.error}")


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
        
        st.markdown(f'<div class="round-header">⚔️ Round {rn} - {tr("round_completed", language)}</div>', unsafe_allow_html=True)
        
        col_opp, col_law = st.columns(2)
        
        with col_opp:
            st.markdown(f"""
            <div class="agent-card opponent-card">
                <div class="agent-label" style="color:#c0392b">{tr("opposing_counsel", language)}</div>
                {round_data['opponent']}
            </div>
            """, unsafe_allow_html=True)
        
        with col_law:
            st.markdown(f"""
            <div class="agent-card lawyer-card">
                <div class="agent-label" style="color:#27ae60">{tr("defense_lawyer", language)}</div>
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
            <div class="agent-label" style="color:#f0c96b">{tr("judge_ruling", language)} — Round {rn}</div>
            <div style="margin-bottom:0.6rem">
                <span class="score-pill score-defense">{tr("defense", language)}: {d_score}/10</span>&nbsp;
                <span class="score-pill score-prosecution">{tr("prosecution", language)}: {p_score}/10</span>&nbsp;
                <span class="winner-badge {badge_cls}">{tr("round_winner", language)}: {badge_label}</span>
            </div>
            <div style="margin-bottom:0.4rem"><strong>{tr("defense_strengths", language)}:</strong> {judge.get("defense_strengths", "—")}</div>
            <div style="margin-bottom:0.4rem"><strong>{tr("defense_weaknesses", language)}:</strong> {judge.get("defense_weaknesses", "—")}</div>
            <div style="margin-bottom:0.4rem"><strong>{tr("reasoning", language)}:</strong> {judge.get("reasoning", "—")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current round
    current_round_num = state["current_round"]
    
    if phase["status"] == "awaiting_choice":
        st.markdown(f'<div class="round-header">⚔️ Round {current_round_num} - {tr("your_turn", language)}</div>', unsafe_allow_html=True)
        
        # Show opponent's attack
        st.markdown(f"""
        <div class="agent-card opponent-card">
            <div class="agent-label" style="color:#c0392b">{tr("opposing_attack", language)}</div>
            {phase['opponent_attack']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(tr("choose_strategy", language))
        
        # Display all options in columns
        cols = st.columns(3)

        selected_option_id = None

        for idx, opt in enumerate(phase['options']):
            with cols[idx]:
                is_selected = st.session_state.get(f"selected_opt_{current_round_num}", None) == opt['id']
                card_style = "option-card selected" if is_selected else "option-card"

                st.markdown(f"""
                <div class="{card_style}">
                    <div class="option-title">{tr("option", language)} {opt['id']}: {opt['title']}</div>
                    <div style="margin: 0.8rem 0; line-height:1.6; flex-grow:1">{opt['argument']}</div>
                    <div class="option-strength">{tr("strength", language)}: {opt['strength']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{tr('select_option', language)} {opt['id']}", key=f"select_opt_{opt['id']}_r{current_round_num}", use_container_width=True):
                    st.session_state[f"selected_opt_{current_round_num}"] = opt['id']
                    st.session_state.scroll_to_proceed = True
                    

        selected_option_id = st.session_state.get(f"selected_opt_{current_round_num}", None)
        
        # Get selected option
        selected_option_id = st.session_state.get(f"selected_opt_{current_round_num}", None)
        
        if selected_option_id is None:
            st.info(tr("select_strategy_info", language))
            selected_opt = None
        else:
            selected_opt = next(opt for opt in phase['options'] if opt['id'] == selected_option_id)

        # Show evidence request if needed
        evidence_files = None
        if phase.get('needs_evidence'):
            st.markdown(tr("evidence_required", language))
            st.info(f"💡 {phase.get('evidence_reason', tr('additional_evidence_help', language))}")
            
            evidence_files = st.file_uploader(
                tr("upload_evidence", language),
                type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
                accept_multiple_files=True,
                key="evidence_uploader"
            )
        
        # Buttons row
        st.markdown('<div id="proceed-anchor"></div>', unsafe_allow_html=True)
        if st.session_state.get("scroll_to_proceed", False):
            st.components.v1.html(
                """
                <script>
                    const scrollToProceed = () => {
                        const target = window.parent.document.getElementById('proceed-anchor');
                        if (target) {
                            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    };
                    setTimeout(scrollToProceed, 100);
                </script>
                """,
                height=0,
            )
            st.session_state.scroll_to_proceed = False

        col_proceed, col_end = st.columns([3, 1])
        
        with col_proceed:
            proceed_disabled = selected_option_id is None
            if st.button(tr("proceed_argument", language), key="proceed_btn", disabled=proceed_disabled):
                with st.spinner(tr("processing_argument", language)):
                    try:
                        # Run round with selection
                        round_result = run_interactive_round(
                            state,
                            selected_option_id=selected_option_id,
                            evidence_files=evidence_files
                        )
                        
                        if round_result["status"] == "awaiting_evidence":
                            st.session_state.round_phase = round_result
                            st.rerun()
                           
                        
                        elif round_result["status"] == "checking_credibility":
                            st.session_state.round_phase = round_result
                            st.rerun()
                            
                        
                        elif round_result["status"] == "round_complete":
                            st.session_state.completed_rounds.append(round_result["round_data"])
                            
                            # Always continue to next round (no limit)
                            next_round_result = run_interactive_round(state)
                            st.session_state.round_phase = next_round_result
                            st.rerun()
                            
                    
                    except Exception as e:
                        st.error(f"{tr('error_processing_round', language)}: {str(e)}")
        
        with col_end:
            st.markdown('<div class="end-hearing-btn">', unsafe_allow_html=True)
            if st.button(tr("end_hearing", language), key="end_hearing_btn"):
                # End the simulation and show final verdict
                st.session_state.round_phase = {"status": "simulation_complete"}
                st.rerun()
               
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif phase["status"] == "checking_credibility":
        st.markdown(f'<div class="round-header">⚔️ Round {current_round_num} - {tr("credibility_check", language)}</div>', unsafe_allow_html=True)
        
        st.markdown(tr("ai_evidence_complete", language))
        st.info(tr("ai_evidence_info", language))
        
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
                <div class="agent-label" style="color:#3498db">{tr("evidence_document", language)} {i+1}</div>
                <div style="margin-bottom:1rem">
                    <span class="credibility-score {score_class}">{tr("credibility_score", language)}: {score}/10</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Display fields using streamlit components to avoid HTML rendering issues
            st.markdown(f"**{tr('relevance', language)}:** {report.get('relevance', 'N/A')}")
            st.markdown(f"**{tr('authenticity_concerns', language)}:** {report.get('authenticity_concerns', 'N/A')}")
            st.markdown(f"**{tr('admissibility_issues', language)}:** {report.get('admissibility_issues', 'N/A')}")
            st.markdown(f"**{tr('strategic_value', language)}:** {report.get('strategic_value', 'N/A')}")
            
            # Red flags
            red_flags = report.get("red_flags", [])
            if red_flags:
                st.markdown(f"**{tr('red_flags', language)}:**")
                for flag in red_flags:
                    st.markdown(f'<div class="red-flag-item">⚠️ {flag}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**{tr('recommendations', language)}:** {report.get('recommendations', 'N/A')}")
            st.markdown("---")
            st.markdown(f"*{tr('overall_assessment', language)}:* {report.get('overall_assessment', 'N/A')}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(tr("use_evidence", language), key="use_evidence"):
            with st.spinner(tr("incorporating_evidence", language)):
                # Proceed with evidence
                round_result = run_interactive_round(state)
                
                if round_result.get("status") == "round_complete":
                    st.session_state.completed_rounds.append(round_result["round_data"])
                    
                    # Continue to next round
                    next_round_result = run_interactive_round(state)
                    st.session_state.round_phase = next_round_result
                    st.rerun()
                    
                    
    
    elif phase["status"] == "awaiting_evidence":
        st.markdown(f'<div class="round-header">⚔️ Round {current_round_num} - {tr("evidence_needed", language)}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="evidence-box">
            <h3 style="color:#f0c96b; margin-bottom:1rem">{tr('evidence_request', language)}</h3>
            <p>{phase.get('reason', tr('upload_evidence_prompt', language))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        evidence_files = st.file_uploader(
            tr("upload_evidence", language),
            type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
            accept_multiple_files=True,
            key="evidence_uploader_2"
        )
        
        if st.button(tr("submit_evidence", language), key="submit_evidence") and evidence_files:
            with st.spinner(tr("analyzing_evidence", language)):
                round_result = run_interactive_round(state, evidence_files=evidence_files)
                
                if round_result["status"] == "checking_credibility":
                    st.session_state.round_phase = round_result
                    st.rerun()
                    
                elif round_result.get("status") == "round_complete":
                    st.session_state.completed_rounds.append(round_result["round_data"])
                    
                    # Continue to next round
                    next_round_result = run_interactive_round(state)
                    st.session_state.round_phase = next_round_result
                    st.rerun()
                        
                        
    
    elif phase["status"] == "simulation_complete":
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.success(tr("hearing_complete", language))
        
        # Calculate final verdict
        final = compute_win_probability(state["round_results"], language)
        win_prob = final["win_probability"]
        
        st.markdown(f'<div class="final-title">{tr("final_verdict", language)}</div>', unsafe_allow_html=True)
        
        # Win probability bar
        st.markdown(f"**{tr('win_probability_defense', language)}**")
        marker_left = max(2, min(97, win_prob))
        st.markdown(f"""
        <div class="win-probability-bar">
            <div class="win-marker" style="left:{marker_left}%"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#8a8577; margin-bottom:0.8rem">
            <span>0% ({tr("lose", language)})</span>
            <span style="font-size:1.2rem; font-weight:700; color:{'#27ae60' if win_prob >= 55 else '#c0392b' if win_prob < 45 else '#f0c96b'}">{win_prob}%</span>
            <span>100% ({tr("win", language)})</span>
        </div>
        """, unsafe_allow_html=True)
        
        col_s, col_w, col_sg = st.columns(3)
        
        with col_s:
            st.markdown(f"**{tr('strong_points', language)}**")
            for pt in final.get("strong_points", []):
                if pt:
                    st.markdown(f"<div class='point-item'><span style='color:#27ae60'>▸</span> {pt}</div>", unsafe_allow_html=True)
        
        with col_w:
            st.markdown(f"**{tr('weak_points', language)}**")
            for pt in final.get("weak_points", []):
                if pt:
                    st.markdown(f"<div class='point-item'><span style='color:#e67e22'>▸</span> {pt}</div>", unsafe_allow_html=True)
        
        with col_sg:
            st.markdown(f"**{tr('strategy_suggestions', language)}**")
            for sug in final.get("suggestions", []):
                if sug:
                    st.markdown(f"<div class='point-item'><span style='color:#f0c96b'>▸</span> {sug}</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(tr("start_new_hearing", language)):
            reset_simulation()
            st.rerun()
