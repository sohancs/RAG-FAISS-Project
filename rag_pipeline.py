import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


load_dotenv(dotenv_path="app.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")


def load_pdfs_from_folder(folder_path: str) :
    if not os.path.exists(folder_path) or not os.listdir(folder_path):
        raise FileNotFoundError(f"❌ No PDFs found in given folder - /{folder_path}.")

    text = ""
    for file in os.listdir(folder_path) :
        if file.endswith(".pdf"):
            pdf = PdfReader(os.path.join(folder_path, file))
            for page in pdf.pages :
                text += page.extract_text()

    return text


def split_txt(text: str) :
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
    chunks = text_splitter.split_text(text)
    return chunks


def create_vector_store(chunks) :
    embedding = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embedding)
    vector_store.save_local("db/faiss-index")
    return vector_store

def load_vector_store():
    embedding = OpenAIEmbeddings(model = OPENAI_EMBEDDING_MODEL)

    #Check FAISS index before loading 
    if not os.path.exists("db/faiss-index"):
        raise FileNotFoundError("❌ No FAISS index found. Please upload documents and rebuild the index first.")

    return FAISS.load_local("db/faiss-index", embedding, allow_dangerous_deserialization=True)


def get_qa_chain() :
    llm = ChatOpenAI(model=OPENAI_LLM_MODEL, temperature=0.1)
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k":3})

    prompt_template = """
        You are assistant that answers user questions using the provided context.
        
        Treat the context and question as **case-insensitive** — 
        meaning "PROMPT", "prompt", and "Prompt" are the same thing.
       
         If unsure, summarize what is present.        

        Conext:
        {context}

        Question:
        {question}

        Answer:
    """

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )

    qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt":prompt},
            return_source_documents=True        
        )
    
    return qa_chain


def ask_query(query: str):
    print(f"query - {query}")
    qa_chain = get_qa_chain()
    response = qa_chain.invoke({"query": query})
    answer = response['result']
   
    sources = response['source_documents']
    #print(f"sources - {sources}")

    return answer 






