# ReguMind — AI-Powered Compliance Assistant

## Overview
ReguMind is an AI-driven compliance assistant that helps organizations interpret and apply major regulatory frameworks such as SOC 2, HIPAA, GDPR, and ISO 27001.  
It provides concise, factual summaries and guidance drawn from official sources—helping security, privacy, and risk professionals save time without sacrificing accuracy.

## Key Features
- **Targeted search:** Query by framework, article, or section (e.g., GDPR Article 30).
- **Source accuracy:** Returns official citations with verbatim excerpts.
- **Operational guidance:** Generates short action checklists based on each control.
- **Confidence metric:** Displays a similarity-based confidence score for retrieved answers.
- **Expandable knowledge base:** Add new frameworks and sections via `snippets.json`.

## Tech Stack
| Layer | Technology | Purpose |
|-------|-------------|----------|
| Backend | Python 3.11 | Core logic and data processing |
| Frameworks | Streamlit | User interface and visualization |
| Libraries | scikit-learn (TFIDF retrieval), json, pathlib | Document similarity and data handling |
| Environment | Conda (`regumind`) | Isolated environment for reproducibility |
| Data | Public compliance frameworks (EU GDPR, HHS HIPAA, NIST AI RMF, AICPA SOC 2) | Source material for analysis |

## Folder Structure
```
ReguMind/
│
├── app.py               # Streamlit interface
├── analyzer.py          # Retrieval and text-similarity logic
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── kb/
    └── snippets.json    # Knowledge base of framework excerpts
```

## How It Works
1. **Load data** – Compliance excerpts and metadata are read from `kb/snippets.json`.
2. **Vectorize** – TF-IDF converts text into weighted vectors for similarity scoring.
3. **Search** – User queries are matched against stored framework data.
4. **Respond** – The most relevant regulation section is displayed with citation, summary, and confidence score.

## Getting Started
1. **Activate the environment:**
   ```bash
   conda activate regumind
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
4. Open your browser at [http://localhost:8501](http://localhost:8501)

## Future Enhancements
- Add multi-framework comparisons (e.g., SOC 2 vs ISO 27001).
- Integrate a vector database (e.g., Chroma or FAISS) for scalable retrieval.
- Include semantic search using a transformer-based embedding model.
- Optionally deploy via FastAPI or Streamlit Cloud.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
