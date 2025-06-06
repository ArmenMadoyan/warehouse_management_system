FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR .

COPY requirements.txt .
COPY front.py .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


EXPOSE 8501

CMD ["bash", "-c", "streamlit run front.py --server.port=8501 --server.address=0.0.0.0"]
