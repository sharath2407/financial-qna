# app.py
import streamlit as st
from extractor import extract_from_file
from qna import QnAEngine
import tempfile

st.set_page_config(page_title="Financial Document Q&A", layout="wide")

st.title("📊 Financial Document Q&A — Local")
st.write("Upload a PDF or Excel file containing financial statements, then ask questions.")

uploaded_file = st.file_uploader("Upload PDF or Excel", type=['pdf','xlsx','xls'])

if 'engine' not in st.session_state:
    st.session_state.engine = QnAEngine()

if uploaded_file:
    with st.spinner("Saving and extracting..."):
        tf = tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1])
        tf.write(uploaded_file.getvalue())
        tf.flush()
        extracted = extract_from_file(tf.name)
    st.success("Extraction complete — preview below")

    st.header("Extracted Summary")
    for k,v in extracted.get('metrics', {}).items():
        st.metric(label=k, value=v)

    if extracted.get('tables'):
        st.header("Detected Tables (sample)")
        for i, tbl in enumerate(extracted['tables'][:3]):
            st.write(f"Table {i+1}")
            st.dataframe(tbl.head(10))

    if st.button("Index document for Q&A"):
        with st.spinner("Indexing document for Q&A..."):
            st.session_state.engine.index_document(extracted)
        st.success("Document indexed — ask questions below")

    st.header("Ask questions")
    query = st.text_input("Enter your question (e.g. 'What was net income for 2023?')")
    if st.button("Ask") and query.strip():
        if not st.session_state.engine.is_indexed():
            st.warning("Please index the document first (click 'Index document for Q&A').")
        else:
            with st.spinner("Generating answer..."):
                answer = st.session_state.engine.answer_query(query)
            st.markdown("**Answer:**")
            st.write(answer)
else:
    st.info("Upload a PDF or Excel to begin")