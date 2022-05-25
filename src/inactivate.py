import requests, sys
import logging
from doi_list import get_doi_list

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='inactivate.log',
                    level=logging.INFO)

logger = logging.getLogger('inactivate')

endpoint = 'https://mds.datacite.org/metadata/'

if (len(sys.argv) < 3):
    raise Exception('Please provide username and password')

username, password = sys.argv[1:]
doi_list = get_doi_list(username, password)
tombstone_landing_page = 'https://edirepository.org/data/tombstone'
count = 0

for doi in doi_list:
    if not "10.6073/PASTA" in doi:
        datacite_url = endpoint + doi
        response = requests.delete(datacite_url, auth=(username, password))
        logger.info("doi: " + doi + "  response: " + 
                    str(response.status_code) + " " + response.text)
        count = count + 1

logger.info("Total inactivations: " + str(count))
