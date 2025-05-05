import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SHL Assessment Recommendation System", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>🧠 SHL Assessment Recommendation System</h1>
    <h4 style='text-align: center; color: #ccc;'>Find the best assessments based on your query using AI!</h4>
    <hr style="border: 1px solid #333;">
    """,
    unsafe_allow_html=True
)

query = st.text_input("🔍 Enter your search query here:", placeholder="e.g. Python SQL coding test")

if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("🤖 Thinking... Fetching the best matches for you!"):
            try:
                response = requests.post("http://localhost:8000/recommend", json={"query": query})
                
                if response.status_code != 200:
                    st.error(f"🚨 Backend error: {response.status_code} - {response.text}")
                else:
                    data = response.json()
                    results = data["recommended_assessments"]
                    df = pd.DataFrame(results)

                    if "duration" in df.columns:
                        df = df.rename(columns={"duration": "Duration in mins"})

                    df['url'] = df['url'].apply(lambda x: f"<a href='{x}' target='_blank'>🔗 View</a>")

                    st.success("✅ Here are your top assessment recommendations:")
                    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"🚨 Something went wrong: {e}")
