# ⚖️ AI Legal Assistant

A **Streamlit-based AI Legal Assistant** that helps users **analyze legal issues, identify relevant IPC sections, search precedent cases, and draft formal legal complaints**. Powered by **Crew AI**, **chromadb**, **LangChain embeddings**, and **Tavily API**, it provides a conversational, structured, and actionable legal workflow.

---

🎥 **Demo Preview:**  
🚀 [AI Legal Assistant(Linkedin Post with Demo Preview Video](https://www.linkedin.com/feed/update/urn:li:activity:7366895333919903745/)  

This demo showcases the multi-agent workflow, IPC section search, legal precedent retrieval, and automated legal drafting.

---

## 🌟 Features

- **Case Intake:** Understands user's legal issue and converts it into a structured JSON format.  
- **IPC Section Retrieval:** Finds top relevant Indian Penal Code (IPC) sections using **chromadb vector search**.  
- **Legal Precedent Search:** Retrieves relevant Indian legal precedents via **Tavily API**.  
- **Legal Document Drafting:** Drafts formal legal complaints, FIRs, or notices based on user inputs.  
- Multi-agent orchestration using **Crew AI**.  
- Semantic search using **LangChain + HuggingFace embeddings**.  
- Interactive web interface powered by **Streamlit**.  
- Handles **user input**, structured analysis, and document generation.  

---

## ⚠️ Notes

- **Groq API key** and **Tavily API key** must be valid (`gsk_` and `tvly_` prefixes).  
- chromadb required for IPC section search.  
- Internet connection is required for Tavily API search.  
- Legal advice is for **informational purposes only** and not a substitute for professional legal counsel.  

---

## 🛠️ Installation & Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Biswo2004/Agentic_AI.git
   cd Agentic_AI/AI_Legal_Assistant

---
2. **🛠️ Create & Activate a Virtual Environment**

   To ensure all dependencies are installed in an isolated environment, follow these steps:
   ```bash
   - windows:
   python -m venv venv
   - macos/linux: 
   source venv/bin/activate

---
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

---
4. **Set Up Environment Variables**
   Create a .env file in the project root and add:
    ```bash
    GROQ_API_KEY=your_groq_api_key
    TAVILY_API_KEY=your_tavily_api_key

---
**🚀 Running the Streamlit App:** `streamlit run app.py` 
- Enter Groq API Key (gsk_...) and Tavily API Key (tvly_...) in the sidebar
- Fill in the incident and user details form
- Explore IPC section suggestions, legal precedents, and generate a legal complaint

---
**🎛️ Optional Settings:**
- Validate API keys in sidebar
- Toggle between Light/Dark theme
- Clear session state if needed

---
**🧩 Code Overview:**
- Agents:
    - Case Intake Agent
    - IPC Section Agent
    - Legal Precedent Agent
    - Legal Drafter Agent
- Tasks:
    - Case Intake Task
    - IPC Section Task
    - Legal Precedent Task
    - Legal Drafter Task
- Tools:
    - IPC Sections Search Tool (chromadb-based vector search)
    - Legal Precedent Search Tool (Tavily API)
- Tech Stacks:
    - Crew AI – multi-agent orchestration
    - Streamlit – interactive web UI
    - chromadb – vector search engine
    - LangChain + HuggingFace – embeddings & semantic understanding
    - Tavily API – trusted Indian legal precedents
    - Python – backend processing
    - JSON – data storage
 
      
---
**📄 Example Usage:**
1. Enter your personal details and describe the incident.
2. The assistant automatically:
   - Classifies your legal issue
   - Suggests relevant IPC sections
   - Retrieves precedent cases
   - Drafts a legal complaint document ready for submission
  
---
**📝 Credits:**
Developed by Biswojit Bal · Powered by Crew AI, Streamlit, FAISS, LangChain, HuggingFace, Tavily API





