import streamlit as st
from app.pipeline import AppCompiler

st.set_page_config(page_title="AI App Compiler", layout="wide")

st.title("AI App Compiler")
st.write("Natural language → structured app configuration → validation → executable preview")

prompt = st.text_area(
    "Enter app requirement",
    "Build a CRM with login, contacts, dashboard, analytics, and admin role access."
)

compiler = AppCompiler()

if st.button("Compile App"):
    result = compiler.compile(prompt)

    st.subheader("Metrics")
    st.json(result.metrics)

    st.subheader("Validation Issues")
    st.json([issue.model_dump() for issue in result.validation_issues])

    st.subheader("Intent")
    st.json(result.intent.model_dump())

    st.subheader("Architecture")
    st.json(result.architecture.model_dump())

    st.subheader("Final App Config")
    st.json(result.config.model_dump())

    st.subheader("Executable Preview")
    st.components.v1.html(result.executable_preview_html, height=500, scrolling=True)