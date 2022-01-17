# Flask Web Application Setup
| Windows (PowerShell)                  | Linux / MacOS (bash)                   | Notes                                  |
|---------------------------------------|----------------------------------------|----------------------------------------|
| `pip install virtualenv`              |                                        | Install `virtualenv`                   |
| `python -m venv venv`                 | `python3 -m venv venv`                 | Create virtual environment (if needed) |
| `.\venv\Scripts\Activate.ps1`         | `source venv/bin/activate`             | Activate virtual environment           |
| `python -m pip install --upgrade pip` | `python3 -m pip install --upgrade pip` | Upgrade `pip` in virtual environment   |
| `pip install -r requirements.txt`     |                                        | Install dependencies                   |


# Running the Application
To send data to New Relic APM, uncomment the the following lines in `webserver.py`:
```python
import newrelic.agent
newrelic.agent.initialize()
```

| Windows (PowerShell)                                  | Linux / MacOS (bash)                                  |
|-------------------------------------------------------|-------------------------------------------------------|
| `$Env:NEW_RELIC_APP_NAME = "Local Python App"`        | `export NEW_RELIC_APP_NAME="Local Python App"`        |
| `$Env:NEW_RELIC_LICENSE_KEY = "XXXXXXXXXXXXXXXXNRAL"` | `export NEW_RELIC_LICENSE_KEY="XXXXXXXXXXXXXXXXNRAL"` |
| `python datacrunch-consulting\webserver.py`           | `python3 datacrunch-consulting/webserver.py`          |


## Generating Errors
Try the following paths (assuming local):
http://127.0.0.1:5000/projects/convertC/123

Then try to this to get something in New Relic Errors Inbox:
http://127.0.0.1:5000/projects/convertC/--123