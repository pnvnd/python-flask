import requests
import json

API_Key = "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"

endpoint = "https://api.newrelic.com/graphql"
headers = {"API-Key": f"{API_Key}", "Content-Type": "application/json"}

environment_query = """query GetSpans {
  actor {
    entity(guid: "MXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") {
      ... on ApmApplicationEntity {
        guid
        name
        applicationInstances {
          environmentAttributes {
            attribute
            value
          }
        }
      }
    }
  }
}"""

apm_query = """query GetSpans {
  actor {
    account(id: 3293157) {
      nrql(query: "SELECT timestamp, duration, request.uri from Transaction WHERE appName = 'FlaskApp - Heroku (APM)' SINCE 5 minutes AGO LIMIT MAX") {
        results
      }
    }
  }
}
"""

r = requests.post(endpoint, json={"query": apm_query}, headers=headers)

if r.status_code == 200:
    print(json.dumps(r.json(), indent=2))
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")