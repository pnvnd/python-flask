FROM python:slim-buster

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-b :5000", "webserver:flaskapp"]
