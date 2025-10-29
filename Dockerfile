FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#Streamlit default port
EXPOSE 8501

# Entrypoint: serve Streamlit
CMD ["streamlit", "run", "app_ui.py", "--server.port", "8501", "--server.address", "0.0.0.0"]