import sys, os
sys.path.append('c:/Users/USER/RBL_ScamShield/scripts')
from jira_sync import JiraClient, load_env

env = load_env('c:/Users/USER/RBL_ScamShield/.env')
client = JiraClient(env.get('JIRA_URL'), env.get('JIRA_EMAIL'), env.get('JIRA_API_TOKEN'))

res = client.request('/rest/api/3/issue/SCRUM-128/transitions')
transitions = res.get('transitions', [])
print('Available transitions for SCRUM-128:')
for t in transitions:
    print(f"ID: {t.get('id')} | Name: {t.get('name')} | To: {t.get('to', {}).get('name')}")
