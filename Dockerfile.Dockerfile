FROM python:3.10-slim

# Instala o FFmpeg, essencial para processar áudio
RUN apt-get update && apt-get install -y ffmpeg

# Copia os arquivos do seu bot para o servidor
WORKDIR /app
COPY . /app

# Instala as bibliotecas do Python
RUN pip install -r requirements.txt

# Comando para iniciar o bot
CMD ["python", "bot.py"]