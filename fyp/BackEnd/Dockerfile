FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt \
	&& python -m spacy download en_core_web_sm \
	&& python -m spacy download en_core_web_lg

COPY src/ .

EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]