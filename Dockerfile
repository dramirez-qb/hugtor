FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app /etc/tor/torrc.d/; apk add --no-cache iproute2-ss tor 
WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt && \
    chmod 755 -R /app/*; ln -sf /app/torrc /etc/tor/torrc

ENV LOGLEVEL=WARNING \
    APP_THREADS=4 \
    APP_ENV=prod\
    APP_PORT=5055\
    APP_HIDDEN_SERVICE_PORT=80\
    APP_ENV=prod

EXPOSE 5055

USER tor

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "gunicorn", "src" ]
