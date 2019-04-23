FROM python:2.7

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app/

ARG BACKEND_HOSTNAME=localhost
ARG BACKEND_PORT=5001

RUN /bin/sed -i -e "s/{{BACKEND_HOSTNAME}}/$BACKEND_HOSTNAME/g" /app/js/app.js
RUN /bin/sed -i -e "s/{{BACKEND_PORT}}/$BACKEND_PORT/g" /app/js/app.js

CMD python celsiusPro.py
