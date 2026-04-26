import streamlit as st
from dotenv import load_dotenv
import requests
import os

load_dotenv()
BASE_URL = os.getenv("API_URL")

st.title("Streamlit + Flask File System")

# ------------------ Upload ------------------
st.header("Upload File")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    
    response = requests.post(f"{BASE_URL}/upload", files={
        "file": (uploaded_file.name, uploaded_file.getvalue())
    })
    
    if response.status_code == 200:
        st.success("File uploaded successfully")
    else:
        st.error("Upload failed")


# ------------------ List Files ------------------
st.header("Available Files")

response = requests.get(f"{BASE_URL}/files")

if response.status_code == 200:
    file_list = response.json().get("files", [])
    
    if file_list:
        selected_file = st.selectbox("Select file", file_list)

        # ------------------ Download ------------------
        if st.button("Download"):
            file_response = requests.get(f"{BASE_URL}/download/{selected_file}")
            
            st.download_button(
                label="Click to Download",
                data=file_response.content,
                file_name=selected_file
            )
    else:
        st.info("No files available")
else:
    st.error("Could not fetch file list")