FROM nginx/unit:1.26.1-python3.9
RUN apt-get update && apt-get install openssh-server -y && service ssh start
COPY requirements.txt /generateid/requirements.txt
RUN pip install -r /generateid/requirements.txt
COPY config.json /docker-entrypoint.d/config.json
COPY . /generateid