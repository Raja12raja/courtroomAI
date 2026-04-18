# CourtRoom AI - Streamlit Application

A Streamlit-based AI application for legal document analysis and courtroom assistance.

## Features

* AI-powered legal document analysis
* Interactive Streamlit interface
* FAISS vector search integration
* Document processing and indexing

## Files

* `app.py` - Main Streamlit application
* `backend.py` - Backend logic and AI processing
* `requirements.txt` - Python dependencies
* `app.yaml` - Databricks app configuration
* `faiss.index` - FAISS vector index for document search
* `texts.pkl` - Processed text data

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   ```
   DATABRICKS_TOKEN=your_token_here
   DATABRICKS_HOST=your_host_here
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Deployment

This application is designed to run on Databricks Apps.

## Environment Variables

Required environment variables (add to `.env` file, not committed to Git):
* `DATABRICKS_TOKEN` - Your Databricks access token
* `DATABRICKS_HOST` - Your Databricks workspace URL

## License

Private project - All rights reserved
