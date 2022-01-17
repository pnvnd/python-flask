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


## Generating Errors
Try the following paths (assuming local):
http://127.0.0.1:5000/projects/convertC/123

Then try to this to get something in New Relic Errors Inbox:
http://127.0.0.1:5000/projects/convertC/--123