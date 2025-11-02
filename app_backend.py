from fastapi import FastAPI


api = FastAPI(title= "APIs for RAG-FAISS-Streamlit app project", version="v1")


@api.get(path="/api/health")
def health_check():
    return {"message" : "HEALTHY", "status" : 200}