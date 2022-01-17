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

| API                             | Endpoint                                             | Notes                 |
|---------------------------------|------------------------------------------------------|-----------------------|
| Convert Celcius to Fahrenheit   | http://localhost:5000/projects/convertC/123          |                       |
| Convert Fahrenheit to Celcius   | http://localhost:5000/projects/convertF/--143        | Generate Server Error |
| Calculate n-th Prime Number     | http://localhost:5000/projects/prime/12345           | Put load on CPU / RAM |
| Calculate n-th Fibonacci number | http://localhost:5000/projects/fib/42                | JSON result           |
| Validate with Luhn algorithm    | http://localhost:5000/projects/luhn/5454545454545454 | Masked in logs        |
| Get COVID data for Ontario      | http://localhost:5000/projects/covid                 |                       |
