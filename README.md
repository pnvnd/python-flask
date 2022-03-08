# Flask Web Application Setup

1. Install `virtualenv`, if not already done
1. Create a virtual environment for the application, if needed
1. Activate virtual environment
1. Upgrade `pip` in virtual environment
1. Install dependencies listed in `requirements.txt`


| Step | Windows (PowerShell)                  | Linux / MacOS (bash)                   |
|------|---------------------------------------|----------------------------------------|
| 1    | `pip install virtualenv`                                                       |
| 2    | `python -m venv venv`                 | `python3 -m venv venv`                 |
| 3    | `.\venv\Scripts\Activate.ps1`         | `source venv/bin/activate`             |
| 4    | `python -m pip install --upgrade pip` | `python3 -m pip install --upgrade pip` |
| 5    | `pip install -r requirements.txt`                                              |


# Running the Application
To send data to New Relic APM, uncomment the the following lines in `webserver.py`:
```python
import newrelic.agent
newrelic.agent.initialize()
```

| Windows (PowerShell)                           | Linux / MacOS (bash)                           |
|------------------------------------------------|------------------------------------------------|
| `$Env:NEW_RELIC_APP_NAME = "Local Python App"` | `export NEW_RELIC_APP_NAME="Local Python App"` |
| `$Env:NEW_RELIC_LICENSE_KEY = "XXXX...NRAL"`   | `export NEW_RELIC_LICENSE_KEY="XXXX...NRAL"`   |
| `python datacrunch-consulting\webserver.py`    | `python3 datacrunch-consulting/webserver.py`   |


# Endpoints to Test

| API                             | Endpoint                                 | Notes                 |
|---------------------------------|------------------------------------------|-----------------------|
| Ping                            | http://127.0.0.1:5000/ping               | JSON: pong            |
| Convert Celcius to Fahrenheit   | http://127.0.0.1:5000/convertC/123       |                       |
| Convert Fahrenheit to Celcius   | http://127.0.0.1:5000/convertF/--143     | Generate Server Error |
| Calculate n-th Prime Number     | http://127.0.0.1:5000/api/prime/12345    | Put load on CPU / RAM |
| Calculate n-th Fibonacci number | http://127.0.0.1:5000/api/fib/42         | JSON result           |
| Validate with Luhn algorithm    | http://127.0.0.1:5000/api/luhn/951847623 | Masked in logs        |
| Get COVID data for Ontario      | http://127.0.0.1:5000/covid              |                       |
| Get status for services         | http://127.0.0.1:5000/statuspage         | AJAX request          |

# OpenTelemetry
1. To send telemetry data to New Relic, set the following environment variables
```
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net:4317
OTEL_EXPORTER_OTLP_HEADERS=api-key=XXXX...NRAL
OTEL_RESOURCE_ATTRIBUTES=service.name=python-flask.otel,service.instance.id=localhost-pc
```

2. Download the following packages to your virtual environment
```
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-instrumentation-flask
pip install opentelemetry-exporter-otlp-proto-grpc
pip install opentelemetry-distro
```

3. No changes to the code is needed, just run the app as usual but with `opentelemetry-instrument` at the front
```
opentelemetry-instrument python .\datacrunch-consulting\webserver.py
```

# Docker Image
1. Build the Docker image with `docker build -t python-flask:latest .`
2. Run the app with your `INGEST - LICENSE` key and give your application a name:
```
docker run -d -e NEW_RELIC_LICENSE_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXNRAL" -e NEW_RELIC_APP_NAME="python-flask.docker" -p 5000:5000 python-flask:latest`
```
3. Access the application with the same endpoints above at `http://127.0.0.1:5000`
