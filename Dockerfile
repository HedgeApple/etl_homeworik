FROM python:3.12.3
COPY /src /src
COPY ./requirements.txt ./src
WORKDIR /src

ENV PYTHONPATH "${PYTHONPATH}:/src"
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip

CMD ["python", "pipeline.py"]



