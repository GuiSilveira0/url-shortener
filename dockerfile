FROM python:3.11-slim

WORKDIR /app

# Variáveis de ambiente para evitar que o Python crie arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências de sistema necessárias
RUN apt-get update \
    && apt-get -y install netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]