FROM python:3.8

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app.py /src/app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
