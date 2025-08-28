import streamlit as st
import os
from dotenv import load_dotenv
from crew import legal_assistant_crew
from ipc_vectordb_builder import build_ipc_vectordb

# Load environment variables (for local development fallback)
load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️", layout="wide")

# ------------------------------
# IPC Vector DB rebuild if missing
# ------------------------------
VECTOR_DB_PATH = "./chroma_vectordb"
if not os.path.exists(VECTOR_DB_PATH):
    with st.spinner("⚡ Building IPC Vector DB..."):
        build_ipc_vectordb()
        st.success("✅ IPC Vector DB built successfully!")

# ------------------------------
# Session state for API key validation
# ------------------------------
if "api_keys_valid" not in st.session_state:
    st.session_state.api_keys_valid = False

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

# Text inputs in sidebar tied to session state
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "tavily_api_key" not in st.session_state:
    st.session_state.tavily_api_key = ""

groq_api_key_input = st.sidebar.text_input(
    "Enter your Groq API Key",
    type="password",
    key="groq_api_key",
    on_change=validate_keys,
    help="Your Groq API key should start with 'gsk_'"
)

tavily_api_key_input = st.sidebar.text_input(
    "Enter your Tavily API Key",
    type="password",
    key="tavily_api_key",
    on_change=validate_keys,
    help="Your Tavily API key should start with 'tvly'"
)

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

    # Form input
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

    # Run workflow if submitted
    if submitted:
        if not user_input.strip():
            st.warning("⚠️ Please enter your incident details to analyze.")
        else:
            with st.spinner("🔎 Analyzing your case and preparing legal output..."):
                # Prepare all user details
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

                # Kickoff the crew with all inputs
                result = legal_assistant_crew.kickoff(inputs=inputs_dict)

            st.success("✅ Legal Assistant completed the workflow!")

            # Display the final output
            st.subheader("📄 Final Legal Complaint")
            if isinstance(result, str):
                st.markdown(result)
            else:
                st.json(result)

else:
    st.warning("Enter valid Groq and Tavily API keys in the sidebar to access the assistant.")
