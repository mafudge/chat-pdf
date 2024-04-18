FROM python:3.11-bookworm

WORKDIR /app 

RUN apt-get update && apt-get install -y curl  

ENV PIP_CACHE_DIR "$CI_PROJECT_DIR/.cache/pip"

COPY ./requirements.txt /app/requirements.txt 

RUN pip install -r requirements.txt 

COPY . /app/

EXPOSE 8501


CMD [ "/usr/local/bin/python", "-m", "streamlit", "run", "app.py" ]