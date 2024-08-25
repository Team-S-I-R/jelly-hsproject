FROM python:latest AS base

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y  --no-install-recommends \
    build-essential \
    ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

# COPY .env /app/.env
COPY . .

EXPOSE 5000

ENTRYPOINT [ "flask" ]

CMD [ "run", "--host", "0.0.0.0" ]