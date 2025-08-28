# ⚖️ AI Legal Assistant

A **Streamlit-based AI Legal Assistant** that helps users **analyze legal issues, identify relevant IPC sections, search precedent cases, and draft formal legal complaints**. Powered by **Crew AI**, **FAISS**, **LangChain embeddings**, and **Tavily API**, it provides a conversational, structured, and actionable legal workflow.

---

🎥 **Demo Preview:**  
🚀 [AI Legal Assistant – GitHub Repo](https://github.com/Biswo2004/Agentic_AI/tree/main/AI_Legal_Assistant)  

This demo showcases the multi-agent workflow, IPC section search, legal precedent retrieval, and automated legal drafting.

---

## 🌟 Features

- **Case Intake:** Understands user's legal issue and converts it into a structured JSON format.  
- **IPC Section Retrieval:** Finds top relevant Indian Penal Code (IPC) sections using **FAISS vector search**.  
- **Legal Precedent Search:** Retrieves relevant Indian legal precedents via **Tavily API**.  
- **Legal Document Drafting:** Drafts formal legal complaints, FIRs, or notices based on user inputs.  
- Multi-agent orchestration using **Crew AI**.  
- Semantic search using **LangChain + HuggingFace embeddings**.  
- Interactive web interface powered by **Streamlit**.  
- Handles **user input**, structured analysis, and document generation.  

---

## ⚠️ Notes

- **Groq API key** and **Tavily API key** must be valid (`gsk_` and `tvly_` prefixes).  
- FAISS index and metadata are required for IPC section search.  
- Internet connection is required for Tavily API search.  
- Legal advice is for **informational purposes only** and not a substitute for professional legal counsel.  

---

## 🛠️ Installation & Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Biswo2004/Agentic_AI.git
   cd Agentic_AI/AI_Legal_Assistant
