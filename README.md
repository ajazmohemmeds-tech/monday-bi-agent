# Monday.com Business Intelligence Agent

## Overview
An AI-powered Business Intelligence Agent that integrates with Monday.com boards to answer founder-level business questions using messy real-world data.

## Features
- Monday.com API Integration (Read-only)
- Conversational BI Agent (Gemini AI)
- Data Cleaning & Resilience
- Missing Data Handling
- Business Visualizations (Leadership Updates)
- Dynamic Query Understanding

## Tech Stack
- Python
- Streamlit
- Monday.com API
- Google Gemini API
- Pandas

## Setup Instructions

### 1. Clone Repository
git clone <repo-link>
cd monday_agent

### 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Add Environment Variables
export GEMINI_API_KEY="your_api_key"
export MONDAY_API_KEY="your_monday_key"

### 5. Run the App
streamlit run app.py

## Architecture
User Query → Streamlit UI → Data Fetch (Monday API) → Data Cleaning → Gemini AI → Business Insights

## Assumptions
- Boards contain Deals and Work Orders
- Data may contain missing/inconsistent values
- Agent provides insights based on available records