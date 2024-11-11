# Usa un'immagine base con Python 3.10
FROM python:3.10

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file requirements.txt per installare le dipendenze
COPY requirements.txt .

# Installa le dipendenze elencate in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutti i file di progetto nella directory di lavoro
COPY . .

# Comando di default per eseguire il file main.py
CMD ["python", "main.py"]
