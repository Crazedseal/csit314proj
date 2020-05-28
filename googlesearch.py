from googleapiclient.discovery import build
import pprint

my_api_key = ""
my_cse_id = ""

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

results = google_search(
    'hello world', my_api_key, my_cse_id)

pprint.pprint(results)
