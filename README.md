# 🏛️ CourtRoom AI - Interactive Legal Platform

An AI-powered courtroom system built on Databricks that enables interactive legal case analysis through multi-agent debate, RAG-based evidence retrieval, and credibility scoring across multiple Indian languages.

![Landing Page](https://raw.githubusercontent.com/Raja12raja/courtroomAI/refs/heads/main/landing.png)

## 📊 Architecture Diagram

### Data Processing Pipeline

The system uses a 4-stage Databricks Jobs pipeline for document processing and embedding generation:


**Pipeline Stages:**
1. **01_ingestion** - Document ingestion and raw data extraction
2. **02_processing** - Text cleaning, normalization, and preprocessing
3. **03_embeddings** - Vector embedding generation using Sentence Transformers
4. **04_inference** - FAISS index creation and similarity search optimization

### Application Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                         │
│                     (Streamlit Web Application)                      │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Layer (app.py)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │   Sidebar    │  │ Hearing Flow │  │  Language Selection (i18n) │  │
│  │   Controls   │  │   Renderer   │  │ (EN/HI/TA/TE/BN/MR/GU/KN/ML) │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   Core Business Logic Layer                          │
│                      (courtroom_core/)                               │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Interactive Processing Engine                   │   │
│  │  • Round Management  • State Tracking  • Flow Control        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  Multi-Agent │  │ Credibility  │  │   Scoring & Analytics    │  │
│  │   System     │  │  Evaluator   │  │   (Evidence Assessment)  │  │
│  │              │  │              │  │                          │  │
│  │ • Prosecution│  │ • Document   │  │ • Argument Strength      │  │
│  │ • Defense    │  │   Analysis   │  │ • Relevance Scoring      │  │
│  │ • Judge      │  │ • OCR        │  │ • Win Probability        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │           RAG (Retrieval-Augmented Generation)                │  │
│  │                                                               │  │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │  │
│  │  │   Document   │───▶│    FAISS     │───▶│   Context    │  │  │
│  │  │   Processor  │    │ Vector Index │    │  Retrieval   │  │  │
│  │  │              │    │              │    │              │  │  │
│  │  │ • PDF Parse  │    │ • Embeddings │    │ • Top-K      │  │  │
│  │  │ • OCR        │    │ • Similarity │    │ • Relevance  │  │  │
│  │  │ • Vision AI  │    │   Search     │    │   Filtering  │  │  │
│  │  └──────────────┘    └──────────────┘    └──────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              LLM Integration Layer                            │  │
│  │                                                               │  │
│  │        Databricks Foundation Model API (MLflow)               │  │
│  │   • Sarvam AI  • Databricks Llama 4 Maverick                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Data & Storage Layer                              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ faiss.index  │  │  texts.pkl   │  │   Document Uploads       │  │
│  │ (Vector DB)  │  │ (Text Store) │  │   (PDF/Images)           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                                                        
┌─────────────────────────────────────────────────────────────────────┐
│                    Deployment Platform                               │
│                       Databricks Apps                                │
│                                                                       │
│                 • Serverless Compute                                │
└─────────────────────────────────────────────────────────────────────┘
```

![Pipeline Architecture](/Workspace/Users/ee220002058@iiti.ac.in/databricks_apps/courtroomai_2026_04_17-13_53/streamlit-hello-world-app/2.jpeg)


## 🎯 Features

### Core Capabilities
* **🤖 Multi-Agent System**: AI agents representing prosecution, defense, and judge engage in realistic legal debates
* **🌐 Multi-Language Support**: Full interface and analysis in 9 languages (English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam)
* **📄 Document Intelligence**: OCR and vision AI for processing legal documents (PDFs, images, scanned documents)
* **🔍 RAG-Powered Research**: FAISS vector search retrieves relevant legal precedents and evidence
* **📊 Credibility Scoring**: Automated assessment of evidence quality, relevance, and authenticity
* **⚖️ Interactive Rounds**: Turn-based hearing flow with real-time argument generation and rebuttals
* **📈 Analytics Dashboard**: Argument strength metrics, detailed scoring, and final win probability

### Technical Features
* Built on **Databricks Apps** for enterprise-grade deployment
* **Sentence Transformers** for semantic search embeddings
* **MLflow** integration for LLM management
* **Streamlit** for responsive, interactive UI
* **FAISS** for efficient similarity search at scale

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit 1.38.0 |
| **Backend** | Python 3.10+ |
| **Vector Database** | FAISS (CPU) |
| **Embeddings** | Sentence Transformers |
| **LLM** | Sarvam AI, Databricks Llama 4 Maverick (via MLflow) |
| **Document Processing** | PyPDF2, pytesseract, PIL |
| **Deployment** | Databricks Apps |
| **Data Science** | Pandas, NumPy |

## 📁 Project Structure

```
streamlit-hello-world-app/
│
├── app.py                      # Main Streamlit entrypoint
├── backend.py                  # Core AI and document processing logic
├── requirements.txt            # Python dependencies
├── app.yaml                    # Databricks Apps configuration
├── .env                        # Environment variables (not in Git)
│
├── courtroom_core/             # Core business logic
│   ├── __init__.py
│   ├── simulation.py           # Orchestration logic
│   ├── agents.py               # Prosecution/Defense/Judge agents
│   ├── rag.py                  # Retrieval-Augmented Generation
│   ├── credibility.py          # Evidence credibility scoring
│   ├── documents.py            # Document processing pipeline
│   ├── llm.py                  # LLM integration (Databricks)
│   ├── scoring.py              # Argument strength & win probability
│   ├── locales.py              # Multi-language support
│   ├── settings.py             # Configuration management
│   └── json_utils.py           # JSON parsing utilities
│
├── courtroom_ui/               # User interface components
│   ├── __init__.py
│   ├── components.py           # Reusable UI widgets
│   ├── config.py               # UI configuration
│   ├── hearing_flow.py         # Hearing round renderer
│   ├── i18n.py                 # Internationalization
│   ├── session.py              # Session state management
│   ├── sidebar.py              # Settings sidebar
│   ├── strings.py              # UI text strings
│   ├── styles.py               # CSS styling
│   └── static/                 # Static assets (images, icons)
│
├── docs/                       # Documentation & images
│   └── images/                 # Architecture diagrams & screenshots
│       ├── pipeline-architecture.png
│       └── job-run-details.png
│
├── faiss.index                 # Pre-built FAISS vector index
├── texts.pkl                   # Indexed document texts
│
├── .git/                       # Git repository
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── GITHUB_SETUP.md             # GitHub connection guide
├── QUICK_START.md              # Quick start guide
├── connect_github.sh           # GitHub setup script
└── git_helper.sh               # Git utility scripts
```

## 🚀 How to Run

### Prerequisites

* **Python 3.10 or higher**
* **Databricks workspace** (for LLM access via Sarvam AI / Llama 4 Maverick)
* **Tesseract OCR** installed (for image text extraction)
* **Git** (for cloning the repository)

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/courtroom-ai.git
cd courtroom-ai
```

#### 2. Install System Dependencies (OCR)

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

#### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# LLM API Key (Required)
LLM_API_KEY=your_api_key_here

```

**To get your LLM API key:**
1. Log into your Databricks workspace
2. Navigate to your LLM provider settings
3. Generate or copy your API key

#### 6. Initialize FAISS Index (First Time Only)

If `faiss.index` and `texts.pkl` don't exist, you'll need to index your legal documents:

```bash
python -c "from backend import initialize_vector_store; initialize_vector_store('path/to/legal/documents')"
```

Or use the provided sample documents (if included).

#### 7. Run the Application

```bash
streamlit run app.py
```

The application will open automatically at `http://localhost:8501`

### Databricks Apps Deployment

#### 1. Upload Project to Databricks Workspace

```bash
databricks workspace import-dir . /Users/your.email@company.com/courtroom-ai -o
```

Or use the Databricks UI:
* Go to Workspace → Your user folder
* Click "Create" → "Import" → Upload the entire project folder

#### 2. Create Databricks App

```bash
databricks apps create courtroom-ai --workspace-path /Users/your.email@company.com/courtroom-ai
```

Or via UI:
* Navigate to "Apps" in the sidebar
* Click "Create App"
* Select your project folder
* App configuration is auto-detected from `app.yaml`

#### 3. Access Your App

* Go to Apps → Find "courtroom-ai"
* Click the URL to access your deployed application
* Share the URL with your team (respects workspace permissions)

## 🎮 Demo Steps - Interactive Walkthrough

### Scenario 1: Simple Property Dispute

**What to do:**

1. **Launch the application** and ensure it loads successfully
2. **Select language** (sidebar): Choose "English" or any of the 9 supported Indian languages
3. **Enter this case description** in the text area:

```
Ramesh claims that Suresh illegally occupied his agricultural land in 
Maharashtra. Ramesh has property documents from 1995. Suresh claims he 
bought the land from Ramesh's uncle in 2010 and has a sale deed. There 
are no witnesses, but Suresh has been paying property tax for 13 years.
```

4. **Click "Start Hearing"** button
5. **Watch Round 1 unfold:**
   * Prosecution presents opening arguments
   * Defense responds with counter-arguments
   * Judge provides interim assessment
6. **Review the round analytics:**
   * Review "Argument Strength" scores for each side
   * Examine "Evidence Credibility" ratings
7. **Upload supporting evidence** (in sidebar):
   * Upload a sample property deed PDF
   * Upload a tax payment receipt image
   * Watch OCR extract text automatically
8. **Click "Continue to Next Round"**
9. **Observe Round 2:**
   * Agents reference uploaded documents
   * Credibility scores update
   * Judge weighs new evidence
10. **Continue through 3-4 rounds** until final verdict
11. **Review final judgment** with detailed reasoning
12. **Check final outcome:**
    * View "Win Probability" analysis
    * Final prosecution vs. defense strength percentages
    * Comprehensive verdict summary

**Expected outcome (after complete hearing):** 
* Prosecution strength: ~65%
* Defense strength: ~35%
* Likely verdict: Favor Ramesh (original owner with older documents)

### Scenario 2: Multi-Language Testing

**What to do:**

1. **Test Hindi interface:**
   * Select "हिंदी" from language dropdown
   * Enter a case in Hindi or English
   * Observe all UI elements and arguments in Hindi

2. **Test regional language:**
   * Try Tamil, Telugu, Malayalam, or other supported languages
   * Watch multi-language document processing
   * Verify OCR works with bilingual documents

**Demonstrates:**
* Language selection must be done before starting the hearing
* Once hearing starts, language remains fixed throughout
* Document uploads work in all supported languages
## 🔧 Configuration Options

> **Note:** Language must be selected before starting the hearing. Language cannot be changed during an active hearing session.


## 🙏 Acknowledgments

* Built on **Databricks Lakehouse Platform**
* Powered by **Sarvam AI** and **Databricks Llama 4 Maverick**
* Embeddings via **Sentence Transformers** (Hugging Face)
* UI framework: **Streamlit**
* Vector search: **FAISS** (Meta AI Research)
* OCR: **Tesseract** (Google)

---

