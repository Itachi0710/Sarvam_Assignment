import streamlit as st
import requests

st.title("RAG System Demo")

query = st.text_input("Enter your query:")

if st.button("Get Response"):
    response = requests.post("http://localhost:8000/query", json={"query": query})
    if response.status_code == 200:
        data = response.json()
        st.write("### Query:", data["query"])
        st.write("### Response:", data["response"])
        st.write("### Documents:", data["documents"])
    else:
        st.write("Error:", response.status_code)
