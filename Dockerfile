# app/Dockerfile

FROM python:3.9-slim
EXPOSE 8501
COPY . /app
WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN apt-get update && apt-get install -y git

RUN pip install -r requirements.txt


ENTRYPOINT ["streamlit", "run", "sos.py", "--server.port=8080","--server.address=0.0.0.0"]


