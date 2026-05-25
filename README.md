# YouTube Comments Sentiment Analyzer

Simple Streamlit app to fetch YouTube comments and run sentiment analysis.

Prerequisites
- Python 3.8+ (this project used a venv)

Setup
1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Run
- Start the app with Streamlit (recommended):

```powershell
streamlit run .\app.py
```

- Alternatively run as a regular script (limited Streamlit features):

```powershell
python .\app.py
```

## Project Architecture

Overview of the project layout and responsibilities:

- `app.py`: Streamlit entrypoint that wires the UI to the core logic.
- `core/`: Main processing modules:
	- `youtube_fetcher.py`: fetches comments from YouTube.
	- `language_detector.py`: detects comment language.
	- `sentiment_analyzer.py`: runs sentiment analysis on comments.
	- `data_processor.py`: cleans and prepares comment data.
- `ui/`: Streamlit UI helpers and pages:
	- `pages.py`: page components and layout.
	- `visualizations.py`: charts and plotting helpers.
- `tools/`: utility scripts and helpers (misc tools).
- `requirements.txt`: Python dependencies.
