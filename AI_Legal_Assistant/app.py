import streamlit as st
import os
from dotenv import load_dotenv
from crew import legal_assistant_crew
from ipc_vectordb_builder import build_ipc_vectordb
import faiss
import json
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables (local fallback)
load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️", layout="wide")

# ------------------------------
# IPC FAISS DB rebuild if missing
# ------------------------------
INDEX_PATH = "./ipc_vectordb.faiss"
METADATA_PATH = "./ipc_vectordb_meta.json"

if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
    with st.spinner("⚡ Building IPC FAISS DB..."):
        try:
            build_ipc_vectordb()  # builds FAISS index and metadata
            st.success("✅ IPC FAISS DB built successfully!")
        except Exception as e:
            st.error(f"❌ Failed to build IPC FAISS DB: {e}")
            st.stop()

# Verify FAISS index and metadata
try:
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
except Exception as e:
    st.error(f"❌ IPC FAISS DB is not accessible: {e}")
    st.stop()

# ------------------------------
# Session state for API key validation
# ------------------------------
if "api_keys_valid" not in st.session_state:
    st.session_state.api_keys_valid = False
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "tavily_api_key" not in st.session_state:
    st.session_state.tavily_api_key = ""

# Sidebar: API key inputs
st.sidebar.title("🔑 API Key Validation")

def validate_keys():
    groq = st.session_state.groq_api_key
    tavily = st.session_state.tavily_api_key
    if groq.startswith("gsk_") and tavily.startswith("tvly"):
        st.session_state.api_keys_valid = True
        st.sidebar.success("✅ Both API Keys are valid!")
    else:
        st.session_state.api_keys_valid = False
        st.sidebar.error("❌ Invalid API Keys. Please check both keys.")

st.sidebar.text_input(
    "Enter your Groq API Key",
    type="password",
    key="groq_api_key",
    on_change=validate_keys,
    help="Your Groq API key should start with 'gsk_'"
)

st.sidebar.text_input(
    "Enter your Tavily API Key",
    type="password",
    key="tavily_api_key",
    on_change=validate_keys,
    help="Your Tavily API key should start with 'tvly'"
)

# ------------------------------
# IPC FAISS Search Tool
# ------------------------------
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_ipc_sections(query: str, top_k: int = 3):
    embed_model = HuggingFaceEmbeddings()
    query_embedding = np.array(embed_model.embed_query(query), dtype=np.float32).reshape(1, -1)

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        results.append(metadata[i])
    return results

# ------------------------------
# Main app screen (only if API keys are valid)
# ------------------------------
if st.session_state.api_keys_valid:
    st.success("🎉 API Keys validated successfully! You can now use the AI Legal Assistant.")

    st.title("⚖️ Personal AI Legal Assistant")
    st.markdown(
        "Fill in the details below. This assistant will help you:\n"
        "- Understand the legal issue\n"
        "- Find applicable IPC sections\n"
        "- Retrieve matching precedent cases\n"
        "- Generate a formal legal complaint document"
    )

    with st.form("legal_form"):
        user_name = st.text_input("Your Full Name")
        incident_date = st.date_input("Date of Incident")
        incident_time = st.time_input("Time of Incident")
        user_address = st.text_area("Your Address")
        police_station_name = st.text_input("Police Station Name")
        police_station_address = st.text_area("Police Station Address")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        user_input = st.text_area("Describe the Incident in Detail")
        submitted = st.form_submit_button("🔍 Run Legal Assistant")

    if submitted:
        if not user_input.strip():
            st.warning("⚠️ Please enter your incident details to analyze.")
        else:
            with st.spinner("🔎 Analyzing your case and preparing legal output..."):
                inputs_dict = {
                    "user_name": user_name,
                    "incident_date": str(incident_date),
                    "incident_time": str(incident_time),
                    "user_address": user_address,
                    "police_station_name": police_station_name,
                    "police_station_address": police_station_address,
                    "phone_number": phone_number,
                    "email": email,
                    "user_input": user_input,
                    "groq_api_key": st.session_state.groq_api_key,
                    "tavily_api_key": st.session_state.tavily_api_key,
                }
                try:
                    result = legal_assistant_crew.kickoff(inputs=inputs_dict)
                except Exception as e:
                    st.error(f"⚠️ Error running the Legal Assistant: {e}")
                    st.stop()

            st.success("✅ Legal Assistant completed the workflow!")

            st.subheader("📄 Final Legal Complaint")
            if isinstance(result, str):
                st.markdown(result)
            else:
                st.json(result)
else:
    st.warning("Enter valid Groq and Tavily API keys in the sidebar to access the assistant.")
