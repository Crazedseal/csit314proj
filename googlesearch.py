from googleapiclient.discovery import build
import pprint

my_api_key = ""
my_cse_id = ""

def get_credientials():
    with open('resource.txt') as file:
        for line in file.readlines():
            split_text = line.strip().split("=")
            if (split_text[0] == "googleapikey"):
                 api_key = split_text[1]
                 print("API - " + split_text[1])
            elif (split_text[0] == "googlecseid"):
                cse_id = split_text[1]
                print("CSE - " + split_text[1])

    credResult = { "api": api_key, "cse": cse_id }
    print(credResult)
    return credResult

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

if __name__ == "__main__":
    # Run script
    creds = get_credientials()
    print("API KEY: " + creds["api"])
    print("CSE ID: " + creds["cse"])
    results = google_search('hello world', creds["api"], creds["cse"])

    pprint.pprint(results)
