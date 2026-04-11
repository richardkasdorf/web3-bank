FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalando dependências de sistema essenciais para compilar pacotes de criptografia
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Atualiza o pip para evitar problemas com versões antigas
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
