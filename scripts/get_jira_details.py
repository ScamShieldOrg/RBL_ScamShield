import sys, os, json
sys.path.append('c:/Users/USER/RBL_ScamShield/scripts')
from jira_sync import JiraClient, load_env

env = load_env('c:/Users/USER/RBL_ScamShield/.env')
client = JiraClient(env.get('JIRA_URL'), env.get('JIRA_EMAIL'), env.get('JIRA_API_TOKEN'))

for key in ['SCRUM-128', 'SCRUM-132', 'SCRUM-135']:
    issue = client.request(f'/rest/api/3/issue/{key}')
    print('**************************************************')
    print(f'TICKET: {key}')
    print(f"SUMMARY: {issue.get('fields', {}).get('summary')}")
    print(f"STATUS: {issue.get('fields', {}).get('status', {}).get('name')}")
    print(f"ASSIGNEE: {issue.get('fields', {}).get('assignee', {}).get('displayName')}")
    desc = issue.get('fields', {}).get('description')
    print('RAW DESC:', json.dumps(desc, ensure_ascii=False, indent=2))
