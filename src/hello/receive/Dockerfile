FROM alpine:latest as base
RUN apk add --no-cache python3

FROM base as builder
COPY . app
WORKDIR app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --trusted-host 172.17.0.1 --extra-index-url http://172.17.0.1:32774

FROM builder as built
RUN rm -r /root/.cache

FROM built
ENTRYPOINT ["python3"]
CMD ["receive.py"]