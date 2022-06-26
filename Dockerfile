FROM python:3.10-slim

VOLUME [ "/logs" ]

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

RUN useradd --user-group --system --no-log-init app
USER app

CMD ["python", "main.py"]
