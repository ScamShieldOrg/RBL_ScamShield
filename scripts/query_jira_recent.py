
import sys, os
sys.path.append('c:/Users/USER/RBL_ScamShield/scripts')
from jira_sync import JiraClient, load_env

env = load_env('c:/Users/USER/RBL_ScamShield/.env')
client = JiraClient(env.get('JIRA_URL'), env.get('JIRA_EMAIL'), env.get('JIRA_API_TOKEN'))

res = client.request('/rest/api/3/search/jql', method='POST', data={
    'jql': 'project = SCRUM ORDER BY key DESC',
    'maxResults': 40,
    'fields': ['summary', 'status', 'assignee', 'issuetype', 'created']
})
for i in res.get('issues', []):
    key = i.get('key')
    f = i.get('fields', {})
    status = f.get('status', {}).get('name')
    assignee = f.get('assignee', {})
    assignee_name = assignee.get('displayName') if assignee else 'Unassigned'
    summary = f.get('summary')
    print(f'{key} | {status} | {assignee_name} | {summary}')
