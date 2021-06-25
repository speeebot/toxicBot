from googleapiclient import discovery
import json

API_KEY = 'AIzaSyD8vfu55pvr4ISTeHb65lRAJLO7zuDMw3w'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

analyze_request = {
  'comment': { 'text': 'friendly greetings from python' },
  'requestedAttributes': {'TOXICITY': {}}
}

response = client.comments().analyze(body=analyze_request).execute()
#print(json.dumps(response, indent=2))

if response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value'] > 0:
    print('yes')
