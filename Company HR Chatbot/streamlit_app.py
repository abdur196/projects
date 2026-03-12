import streamlit as st
from main import qa_chain  # Uncomment when backend is ready

st.set_page_config(page_title="Tintash HR Chatbot", page_icon="🧠")
st.title("🧠 Tintash HR Chatbot")

st.markdown("Ask any HR-related question and I'll try my best to help you.")

# Form for input and button layout
with st.form("chat_form", clear_on_submit=True):  # Clears after submit
    query = st.text_input("Type your question here:", key="query_input")

    col1, col2 = st.columns([1, 1])
    with col1:
        submitted = st.form_submit_button("Submit")
    with col2:
        cleared = st.form_submit_button("Clear")

if submitted:
    if query.strip():
        with st.spinner("Thinking..."):
            result = qa_chain.invoke({"query": query})
            st.markdown("### 📎 Answer:")
            st.write(result["result"])
           
    else:
        st.warning("Please enter a question.")

if cleared:
    st.rerun()

st.write("Made with Langchain and Streamlit. © 2025")
