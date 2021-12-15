FROM python:3.9

RUN apt-get update && \
    apt-get install -y && \
    python3 -m pip install --upgrade pip && \
    pip3 install daphne

ENV PYTHONUNBUFFERED=1
COPY . /opt/website-builder-api
WORKDIR /opt/website-builder-api

RUN pip3 install -r /opt/website-builder-api/requirements.txt

ENV API_PORT=9999
EXPOSE $API_PORT

ENV ALLOWED_HOSTS="127.0.0.1,localhost,172.17.0.1,178.62.35.144"

# Django Secret Key
ENV SECRET_KEY="django-insecure-!wr_^1ee9_9v-ig$u%e9$h=3*1(3v^ok%)5e8w$aj5u_$7i=87"

# S3 BUCKET CREDENTIALS
ENV BUCKET_ACCESS_KEY_ID="D16XTQLOIP3UKGZZVYLB"
ENV BUCKET_SECRET_KEY="fwezeFlhJS0Mb0NNGoPYyKYe7yOuSCBsZJY8YkJX"
ENV BUCKET_REGION_NAME="eu-central-1"
ENV BUCKET_NAME="page-template-builds"
ENV BUCKET_ENDPOINT_URL="https://s3.eu-central-1.wasabisys.com"

CMD ["daphne", "-b", "0.0.0.0", "-p", "9999", "page_builder.asgi:application"]
