# Flask Web Application Setup

1. Install `virtualenv`, if not already done
2. Create a virtual environment for the application, if needed
3. Activate virtual environment
4. Upgrade `pip` in virtual environment
5. Install dependencies listed in `requirements.txt`


| Step | Windows (PowerShell)                  | Linux / MacOS (bash)                   |
|------|---------------------------------------|----------------------------------------|
| 1    | `pip install virtualenv`              | `pip3 install virtualenv`              |
| 2    | `python -m venv venv`                 | `python3 -m venv venv`                 |
| 3    | `.\venv\Scripts\Activate.ps1`         | `source venv/bin/activate`             |
| 4    | `python -m pip install --upgrade pip` | `python3 -m pip install --upgrade pip` |
| 5    | `pip install -r requirements.txt`     | `pip install -r requirements.txt`      |


## Endpoints to Test

| API                             | Endpoint                                 | Notes                 |
|---------------------------------|------------------------------------------|-----------------------|
| Ping                            | http://127.0.0.1:5000/ping               | JSON: pong            |
| Convert Celcius to Fahrenheit   | http://127.0.0.1:5000/convertC/123       |                       |
| Convert Fahrenheit to Celcius   | http://127.0.0.1:5000/convertF/--143     | Generate Server Error |
| Validate with Luhn algorithm    | http://127.0.0.1:5000/api/luhn/951847623 | Masked in logs        |
| Calculate n-th Prime Number     | http://127.0.0.1:5000/api/prime/12345    | Put load on CPU / RAM |
| Calculate n-th Fibonacci number | http://127.0.0.1:5000/api/fib/42         | JSON result           |
| Calculate n-th Fibonacci number | http://127.0.0.1:5000/extfib/67          | Call external service |
| Get COVID data for Ontario      | http://127.0.0.1:5000/covid              |                       |
| Get status for services         | http://127.0.0.1:5000/statuspage         | AJAX request          |
| Check divisibility of integers  | http://127.0.0.1:5000/divisibility       |                       |


## OpenTelemetry
1. To send telemetry data to New Relic, set the following environment variables

   ### Windows (PowerShell)
   ```PowerShell
   $Env:OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net:4317"
   $Env:OTEL_EXPORTER_OTLP_HEADERS=api-key="XXXX...NRAL"
   $Env:OTEL_RESOURCE_ATTRIBUTES=service.name="python-flask.otel,service.instance.id=localhost-pc"
   ```

   ### Linux / macOS
   ```Bash
   export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net:4317"
   export OTEL_EXPORTER_OTLP_HEADERS="api-key=XXXX...NRAL"
   export OTEL_RESOURCE_ATTRIBUTES=service.name="python-flask.otel,service.instance.id=vercel"
   ```

2. Download the following packages to your virtual environment
   ```
   pip install opentelemetry-exporter
   pip install opentelemetry-instrumentation-flask
   pip install opentelemetry-instrumentation-jinja2
   pip install opentelemetry-instrumentation-requests
   ```

3. No changes to the code is needed, just run the app as usual but with `opentelemetry-instrument` at the front
   ```
   opentelemetry-instrument python webserver.py
   ```

## Docker Image
1. Build the Docker image with `docker build -t python-flask:latest .`
2. Run the app with your environment variables and give your application a name:
   ```
   docker run -d --name python-flask -e OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net:4318" -e OTEL_EXPORTER_OTLP_HEADERS="api-key=XXXX...NRAL" -e OTEL_RESOURCE_ATTRIBUTES="service.name=python-flask.otel,service.instance.id=docker,tags.environment=production,tags.team=datacrunch" -p 5000:5000 python-flask:latest
   ```
3. Access the application with the same endpoints above at `http://127.0.0.1:5000`
