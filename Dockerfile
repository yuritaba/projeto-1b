# Use a imagem Python oficial como base
FROM python:3.8

# Defina a variável de ambiente para desabilitar a saída em buffer
ENV PYTHONUNBUFFERED 1

# Crie e defina o diretório de trabalho do aplicativo
RUN mkdir /app
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt /app/

# Instale as dependências do projeto
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório atual para o contêiner
COPY . /app/
