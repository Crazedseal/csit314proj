from googleapiclient.discovery import build
import pprint

def get_credientials():
    """Opens the resource.txt file; parses the lines and returns a dictionary containing the api key and cse id."""
    with open('resource.txt') as file:
        for line in file.readlines():
            split_text = line.strip().split("=")
            if (split_text[0] == "googleapikey"):
                 api_key = split_text[1]
            elif (split_text[0] == "googlecseid"):
                cse_id = split_text[1]

    credResult = { "api": api_key, "cse": cse_id }
    return credResult


def google_search(search_term, api_key, cse_id, **kwargs):
    """Constructs and conducts a google search returning the resulting JSON response."""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

if __name__ == "__main__":
    # Run script
    creds = get_credientials()
    results = google_search('hello world', creds["api"], creds["cse"])
    
    print(results)
