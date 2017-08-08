import requests, sys

def get_doi_list(username, password):
    datacite_url = 'https://mds.datacite.org/doi'
    response = requests.get(datacite_url, auth=(username, password))
    
    doi_list = []
    if (response.status_code == 200):
        # Get rid of newlines
        doi_list = response.text.splitlines()
    else:
        raise Exception('Failed to get list of DOIs from DataCite API')
    return doi_list   


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        raise Exception('Please provide username and password')
    username = sys.argv[1]
    password = sys.argv[2]
    DOIs = get_doi_list(username, password)
    for doi in DOIs:
        print(doi)
    