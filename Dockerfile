# This example uses .NET 6.0.  For other versions, see https://hub.docker.com/_/microsoft-dotnet-sdk/
FROM python:slim-buster

# Copy repository to base image and publish your application
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-b :5000", "webserver:flaskapp"]
