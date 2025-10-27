## 🧠 **RAG Chatbot with FAISS and Streamlit**

A **Retrieval-Augmented Generation (RAG)** chatbot that lets you upload PDFs, index them using **FAISS**, and ask questions about their content — all through a clean **Streamlit UI**.

---

### 🚀 **Key Features**

* 📂 Upload multiple PDFs from sidebar
* ⚡ Automatically extract, chunk & index text
* 🧭 Prevent duplicate uploads
* 💬 Ask natural-language questions
* 📑 Get answers with source (file & page)
* 🕘 Session-based chat history

---

### 🏗 **Tech Stack**

**Python**, **Streamlit**, **LangChain**, **FAISS**, **OpenAI**, **PyPDF2**

---

### ⚙️ **Setup & Run**

1️⃣ Create a virtual environment & install dependencies

```bash
pip install -r requirements.txt
```

2️⃣ Set your OpenAI API key in **app.env**

```bash
OPENAI_API_KEY=your_api_key   
```

3️⃣ Run the app

```bash
streamlit run app.py
```

Then open **[http://localhost:8501](http://localhost:8501)** in your browser 🚀

---

### 💡 **How It Works**

1. Upload one or more PDFs from the sidebar
2. Click **“Rebuild FAISS Index”** to process and store embeddings
3. Ask questions → get LLM-generated answers with document sources
4. Reset All button - delete indexes and uploaded files
5. Clear Chat History - cleanup chat history

---

### 📁 **Structure**

```
rag-faiss-streamlit/
├── app.py              # Streamlit UI
├── rag_pipeline.py     # RAG logic (PDF → chunks → FAISS)
├── data/               # Uploaded PDFs
└── db/                 # FAISS index storage
└── app.env             #config file
```

