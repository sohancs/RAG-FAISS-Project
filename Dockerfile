FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#Streamlit default port
EXPOSE 8000 8501

# Entrypoint: serve Streamlit
CMD ["streamlit", "run", "app_ui.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

# Entrypoint: start uvicorn server for fast apis & serve Streamlit in same container
#CMD ["bash", "-c", "uvicorn app_backend:api --host 0.0.0.0 --port 8000 & streamlit run app_ui.py --server.port=8501 --server.address=0.0.0.0"]
