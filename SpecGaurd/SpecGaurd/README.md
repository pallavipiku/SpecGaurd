# SpecSense AI

SpecSense AI is a modular product recommendation system that interprets natural-language shopping requirements and recommends the best product matches from a structured catalog.

## Features

- Natural-language query parsing
- Budget and product category extraction
- Soft preference detection for portability, coding suitability, and battery life
- Hybrid filtering and ranking
- Explainable recommendation output
- Streamlit-based user interface

## Project Structure

- `app.py` – Streamlit user interface
- `specsense/data_loader.py` – loads and normalizes catalog data
- `specsense/query_parser.py` – parses free-form user intent
- `specsense/matcher.py` – filters and ranks products
- `specsense/recommendation.py` – recommendation orchestration
- `data/sample_products.csv` – sample product catalog

## Setup

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the app

```bash
.venv\Scripts\streamlit.exe run app.py
```

## Run tests

```bash
.venv\Scripts\python.exe -m pytest -q
```
