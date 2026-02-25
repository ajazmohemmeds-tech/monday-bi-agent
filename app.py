import streamlit as st
import pandas as pd
import google.generativeai as genai
import os 
from monday_api import * # if you are using monday_api.py
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Monday BI Dashboard", layout="wide")

st.title("📊 Monday.com BI Dashboard")
st.write("Data loaded from Monday API 🚀")


DEALS_BOARD_ID = 5026839802
WORK_ORDERS_BOARD_ID = 5026839899

st.set_page_config(page_title="Monday BI Agent", layout="wide")

st.title("📊 Monday.com Business Intelligence Agent")
st.write("Ask founder-level business questions about Deals and Work Orders")

def clean_data(raw_data):
    try:
        items = raw_data["data"]["boards"][0]["items_page"]["items"]
        rows = []

        for item in items:
            row = {"Item Name": item["name"]}
            for col in item["column_values"]:
                col_name = col["column"]["title"]
                value = col["text"]

                # Handle messy & missing data (Assignment Requirement)
                if value is None or value == "":
                    value = "Missing"

                row[col_name] = value

            rows.append(row)

        df = pd.DataFrame(rows)
        return df

    except Exception as e:
        st.error("Error reading data from Monday.com")
        return pd.DataFrame()
    # 🤖 AI Insights Generator
def generate_ai_insights(deals_df, work_df, user_question):
    try:
        import google.generativeai as genai
        import os

        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-2.5-flash")

        deals_sample = deals_df.head(20).to_string()
        work_sample = work_df.head(20).to_string()

        prompt = f"""
        You are a senior Business Intelligence Analyst.

        Deals Data:
        {deals_sample}

        Work Orders Data:
        {work_sample}

        User Question: {user_question}

        Provide:
        - Key Insights
        - Risks
        - Opportunities
        - Simple Executive Summary
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"

# User question (Conversational Interface Requirement)
user_question = st.text_input(
    "💬 Ask a business question (Example: How is our pipeline this quarter?)"
)

if st.button("Analyze Business Data"):
    st.info("🔄 Fetching live data from Monday.com boards...")

    # Fetch data dynamically (NO CSV hardcoding ✔️)
    deals_raw = fetch_board_data(DEALS_BOARD_ID)
    work_raw = fetch_board_data(WORK_ORDERS_BOARD_ID)

    deals_df = clean_data(deals_raw)
    work_df = clean_data(work_raw)
    st.subheader("📈 Key Business Insights")

    col1, col2 = st.columns(2)
    col1.metric("Total Deals", len(deals_df))
    col2.metric("Total Work Orders", len(work_df))

    # Data quality check (Data Resilience Requirement)
    if not deals_df.empty:
        missing_values = deals_df.isin(["Missing"]).sum().sum()
        if missing_values > 0:
            st.warning(
                "⚠️ Data contains missing/inconsistent values. Insights are based on available records."
            )

    st.subheader("📊 Deals Data Preview")
    if 'deals_df' in locals():
     st.subheader("📊 Deals Data Preview")
    st.dataframe(deals_df)
else:
    st.warning("Deals data not loaded yet.")
    # 📊 Business Visualizations (Leadership Updates Requirement)
st.subheader("📊 Business Visualizations")

# 🛡️ SAFETY CHECK (VERY IMPORTANT)
if 'deals_df' in locals() and 'work_df' in locals():

    try:
        # Deals by Stage Chart
        if not deals_df.empty and "Deal Stage" in deals_df.columns:
            st.write("### Deals by Stage")
            stage_counts = deals_df["Deal Stage"].value_counts()
            st.bar_chart(stage_counts)

        # Work Orders by Status Chart
        if not work_df.empty and "Status" in work_df.columns:
            st.write("### Work Orders by Status")
            status_counts = work_df["Status"].value_counts()
            st.bar_chart(status_counts)

    except Exception as e:
        st.warning("Visualization error due to messy data formats.")

else:
    st.warning("Please click 'Analyze Business Data' first to load data.")
    # Display the dataframe in Streamlit UI
if 'deals_df' in locals():
    st.subheader("Deals Data Preview")
    st.dataframe(deals_df)
elif 'work_df' in locals():
    st.subheader("Work Orders Data Preview")
    st.dataframe(work_df)
else:
    st.warning("No data loaded yet.")
   # 🧠 AI Insights Section
st.subheader("🧠 AI Business Insights")

if 'deals_df' in locals() and 'work_df' in locals():

    # 🔎 Clarification logic (ADD HERE)
    if user_question and "sector" in user_question.lower():
        if "Sector service" not in deals_df.columns:
            st.info("Sector data may be incomplete. Insights are based on available records.")

    if user_question:
        with st.spinner("Generating AI insights from your business data..."):
            ai_result = generate_ai_insights(deals_df, work_df, user_question)
            st.success("AI Analysis Ready")
            st.write(ai_result)
    else:
        st.warning("Please enter a business question above before analyzing.")
else:
    st.warning("Please click 'Analyze Business Data' first to load data.")

