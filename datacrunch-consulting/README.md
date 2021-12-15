# Flask Web Application Setup
1. `pip install virtualenv`
1. Activate virtual environment by running
    - `.\venv\Scripts\Activate.ps1` (PowerShell)
    - `source venv/bin/activate` (Linux / macOS)
1. `python -m pip install --upgrade pip`
1. `pip install -r requirements.txt`


# Running the Application
To send data to New Relic APM, uncomment the the following lines in `webserver.py`:
```python
import newrelic.agent
newrelic.agent.initialize()
```

## Windows (PowerShell)
```PowerShell
$Env:NEW_RELIC_APP_NAME = "new value test"
$Env:NEW_RELIC_LICENSE_KEY = "XXXXXXXXXXXXXXXXNRAL"
python datacrunch-consulting\webserver.py
```

## Linux / macOS
```bash
export NEW_RELIC_APP_NAME="Local Python App"
export NEW_RELIC_LICENSE_KEY="XXXXXXXXXXXXXXXXNRAL"
python3 datacrunch-consulting/webserver.py
```