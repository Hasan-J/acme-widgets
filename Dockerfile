FROM python:3.10.5-slim-bullseye

COPY ./main.py /app/main.py
COPY ./test_main.py /app/test_main.py
WORKDIR /app

RUN pip install pytest

ENTRYPOINT ["python", "main.py"]
