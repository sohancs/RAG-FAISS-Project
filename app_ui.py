
import streamlit as st
from rag_pipeline import load_pdfs_from_folder, split_txt, create_vector_store, ask_query
import os
import time
import shutil
from dotenv import load_dotenv


load_dotenv(dotenv_path="app.env")

DATA_DIR = os.getenv("DATA_DIR", "data")
DB_DIR = os.getenv("DB_DIR", "db")
MAX_QUERIES = int(os.getenv("MAX_QUERIES", 5))

#Refresh UI
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

#Store user queries counter
if "user_queries_count" not in st.session_state:
    st.session_state.user_queries_count = 1

def refresh_ui() :
    st.session_state.reset_flag = not  st.session_state.reset_flag
    st.rerun()

st.set_page_config(page_title="📚 RAG Chatbot", layout="wide")
st.title("🚀 Intelligent Chatbot 🤖")

st.sidebar.header("📂 Manage Uploads")
st.markdown(
    """
    <style>
        /* Sidebar width */
        [data-testid="stSidebar"] {
            min-width: 500px;
            max-width: 500px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

os.makedirs(name=DATA_DIR, exist_ok=True)

#Disappear messages after given interval
def disapper_msg(msg:str, msg_type = 'success', duration=3) :
    placeholder = st.sidebar.empty()

    if(msg_type == 'success'):
        placeholder.success(msg)
    elif(msg_type == 'warning'):
        placeholder.warning(msg)
    elif(msg_type == 'info'):
        placeholder.info(msg)
    
    #clear msg after given interval
    start_time = time.time()

    while time.time() - start_time < duration :
        time.sleep(0.1)

    placeholder.empty()


# Show existing files
existing_files = os.listdir(DATA_DIR)
if existing_files:
    st.sidebar.markdown("**Existing uploaded files**")
    for file in existing_files:
        st.sidebar.markdown(f"- {file}")
else:
    disapper_msg("No file uploaded yet!", "info", 3)
    


# Step 1: File uploader
uploaded_files = st.sidebar.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True, key=str(st.session_state.reset_flag))

# Step 2: When user uploads files - save or show duplicate warning
new_file=[]
if uploaded_files:
    for file in uploaded_files:
        new_file_name = os.path.join(DATA_DIR,file.name)

        if os.path.exists(new_file_name):
            disapper_msg(f"⚠️ {file.name} is alreay exists in {DATA_DIR} folder.", "warning", 3)
        else:   
            with open(f"data/{file.name}", "wb") as f:
                f.write(file.getbuffer())
                
            new_file.append(file.name)
    
    if new_file:
         disapper_msg(f"✅ Uploaded {', '.join(new_file)}", "success", 3)
         refresh_ui()


# Step 3: Build FAISS index on button click

if st.sidebar.button("🔄 Rebuild FAISS Index"):
    try:
        with st.spinner("Indexing documents..."):
            text = load_pdfs_from_folder(DATA_DIR)
            chunks = split_txt(text)
            create_vector_store(chunks)
        disapper_msg("📂 Documents indexed successfully!", "success", 3)
    except FileNotFoundError as ex:
        st.error(str(ex))

# Reset FAISS Index, Uploaded files and Clear Chat History
if existing_files:
    if st.sidebar.button("🗑️ Reset All") :
        if os.path.exists(DB_DIR):
            for fileNm in os.listdir(DB_DIR):
                path = os.path.join(DB_DIR, fileNm)
                if os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            disapper_msg("📂 FAISS index reset successfully!", "success", 2)
        
        if os.path.exists(DATA_DIR):
            for fileNm in os.listdir(DATA_DIR):
                path = os.path.join(DATA_DIR, fileNm)
                if os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            disapper_msg("📂 Uploaded Files reset successfully!", "success", 2)
        refresh_ui()

if st.sidebar.button("🗑️ Clear Chat History") :
    st.session_state["chat_history"].clear()
    disapper_msg("🕘 Cleared Chat history successfully!", "success", 3)
    refresh_ui()


#initialize chat_history to save chat histories
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Step 4: Chat input
user_query = st.text_input("**Ask a question about the uploaded documents and press enter button:**")

if user_query:
    try:
        if st.session_state.user_queries_count > MAX_QUERIES:
            st.warning(f"⚠️ You've reached to your {MAX_QUERIES} free queries limit.")
        else:
            with st.spinner("Generating answer..."):
                response = ask_query(user_query)
                st.write("**Answer:**", response)
                st.session_state.user_queries_count += 1

                #save history
                st.session_state["chat_history"].append({
                    "question" : user_query,
                    "answer" : response
                })

    except FileNotFoundError as ex:
        st.error(str(ex))
    
    st.divider()


# display chat history
if st.session_state["chat_history"]:
    st.markdown("### 🕘 Chat History")
    for index, item in enumerate(st.session_state["chat_history"][::-1], 1) :
        st.markdown(f"**Que{index}** : {item['question']}")
        st.markdown(f"**Ans{index}** : {item['answer']}")
        st.divider()

    


