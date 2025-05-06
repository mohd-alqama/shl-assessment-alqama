import streamlit as st
import requests
import pandas as pd

# Set the API URL for your FastAPI deployed on Render
API_URL = "https://your-fastapi-url.onrender.com/recommend"

# Set page configuration for Streamlit
st.set_page_config(page_title="SHL Assessment Recommendation System", layout="centered")

# Streamlit header and description
st.markdown(
    """
    <h1 style='text-align: center; color: #4B8BBE;'>🧠 SHL Assessment Recommendation System</h1>
    <h4 style='text-align: center; color: #ccc;'>Find the best assessments based on your query using AI!</h4>
    <hr style="border: 1px solid #333;">
    """,
    unsafe_allow_html=True
)

# User input query
query = st.text_input("🔍 Enter your search query here:", placeholder="e.g. Python SQL coding test")

# On search button click
if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("🤖 Thinking... Fetching the best matches for you!"):
            try:
                # Send the query to FastAPI backend
                response = requests.post(API_URL, json={"query": query})

                if response.status_code == 200:
                    data = response.json()

                    recommended_assessments = data.get("recommended_assessments", [])

                    if recommended_assessments:
                        # Prepare DataFrame for displaying
                        df = pd.DataFrame(recommended_assessments)

                        # Displaying columns and URL links
                        if 'Score' in df.columns:
                            df = df.drop(columns=['Score'])

                        if "Duration" in df.columns:
                            df = df.rename(columns={"Duration": "Duration in mins"})

                        display_cols = ["Assessment Name", "Skills", "Test Type", "Description", "Remote Testing Support", "Adaptive/IRT", "Duration in mins", "URL"]
                        df = df[[col for col in display_cols if col in df.columns]]

                        # Make URLs clickable
                        df['URL'] = df['URL'].apply(lambda x: f"<a href='{x}' target='_blank'>🔗 View</a>" if pd.notna(x) else "")

                        st.success("✅ Here are your top assessment recommendations:")

                        # Build styled HTML table for display
                        table_html = """
                        <style>
                            table.custom-table {
                                width: 100%;
                                border-collapse: collapse;
                                font-family: Arial, sans-serif;
                            }
                            table.custom-table thead {
                                background-color: #2e2e2e;
                                color: white;
                            }
                            table.custom-table th, table.custom-table td {
                                border: 1px solid #444;
                                padding: 10px;
                                text-align: left;
                                vertical-align: top;
                                color: #eee;
                            }
                            table.custom-table tr:nth-child(even) {
                                background-color: #1e1e1e;
                            }
                            table.custom-table tr:nth-child(odd) {
                                background-color: #2a2a2a;
                            }
                            a {
                                color: #1a73e8;
                                text-decoration: none;
                            }
                        </style>
                        <table class="custom-table">
                            <thead>
                                <tr>
                        """

                        for col in df.columns:
                            table_html += f"<th>{col}</th>"
                        table_html += "</tr></thead><tbody>"

                        for _, row in df.iterrows():
                            table_html += "<tr>"
                            for cell in row:
                                table_html += f"<td>{cell}</td>"
                            table_html += "</tr>"

                        table_html += "</tbody></table>"

                        # Display the table in Streamlit
                        st.markdown(table_html, unsafe_allow_html=True)

                    else:
                        st.warning("😕 No assessments matched your query. Try rephrasing it!")

                else:
                    st.error(f"🚨 Error fetching data from API: {response.status_code}")

            except Exception as e:
                st.error(f"🚨 Something went wrong: {e}")
