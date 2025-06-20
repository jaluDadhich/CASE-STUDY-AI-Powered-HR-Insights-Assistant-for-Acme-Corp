import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(f"*********Printing the current word {os.getcwd()}")  # Debugging line to check current working directory
# Ensure the app directory is in the Python path
from eda.utils import load_insights
from chatbot.rag_pipeline import get_hr_answer

# Set page config
st.set_page_config(
    page_title="AI HR Insights Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define tabs
tabs = st.tabs(["📊 HR Dashboard", "💬 Ask HR Assistant"])

# --- TAB 1: HR Dashboard ---
with tabs[0]:
    st.title("📊 HR Dashboard")
    st.markdown("""
        This dashboard presents key insights from the attrition data analysis.
        Use the filters and charts below to understand trends and risk areas.
    """)

    # Load insights (assumes figures are pre-generated and stored as images or returned by a function)
    insights = load_insights()  # returns a list of (title, description, matplotlib fig or image)

    for title, desc, fig in insights:
        with st.container():
            st.subheader(title)
            st.markdown(desc)
            st.pyplot(fig)
            st.markdown("---")

# --- TAB 2: Ask HR Assistant ---
with tabs[1]:
    st.title("💬 Ask HR Assistant")
    st.markdown("""
        Ask any policy-related HR question below. The assistant will respond using Acme's official HR policy document.
    """)

    # User Input
    user_question = st.text_input("Enter your HR-related question:", placeholder="e.g., How many casual leaves can I take?")

    if user_question:
        with st.spinner("Generating response..."):
            try:
                response = get_hr_answer(user_question)
                # response = "we will use the get_hr_answer function to generate a response based on the user question"
                st.success("Response:")
                st.markdown(response)
            except Exception as e:
                st.error(f"Failed to generate answer: {str(e)}")

    st.markdown("---")
    st.caption("Powered by RAG + LangChain")
# --- End of app.py ---