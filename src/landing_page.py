import requests, sys
import logging

from doi_list import get_doi_list

def is_LTER(package_id):
    lter = False
    if ("knb-lter-" in package_id or
        "lter-landsat" in package_id or
        "ecotrends" in package_id):
        lter = True
    return lter

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='landing_page.log',
                    level=logging.INFO)

logger = logging.getLogger('landing_page')

endpoint = 'https://mds.datacite.org/doi/'

if (len(sys.argv) < 3):
    raise Exception('Please provide username and password')

username, password = sys.argv[1:]
doi_list = get_doi_list(username, password)

count = 0
lter_landing_page = "https://portal.lternet.edu/nis/mapbrowse?packageid="
edi_landing_page =  "https://portal.edirepository.org/nis/mapbrowse?packageid="

for doi in doi_list:
    if "10.6073/PASTA" in doi:
        datacite_get_url = endpoint + doi
        response = requests.get(datacite_get_url, auth=(username, password))
        logger.info("DOI: " + doi + "  GET status code: " + str(response.status_code))
        if response.status_code == 200:
            current_landing_page = response.text.strip()
            new_landing_page = ""
            equal_sign_index = current_landing_page.find('=') + 1
            package_id = current_landing_page[equal_sign_index:]
            #logger.info("package_id: " + package_id + "  current_landing_page: " + current_landing_page)
            if is_LTER(package_id) and edi_landing_page in current_landing_page:
                new_landing_page = lter_landing_page + package_id
            elif not is_LTER(package_id) and lter_landing_page in current_landing_page:
                new_landing_page = edi_landing_page + package_id
            
            if new_landing_page != "":
                logger.info("Setting landing page for " + package_id + "from " + current_landing_page + " to " + new_landing_page)
                request_body = "doi=" + doi + "\n" + "url=" + new_landing_page + "\n"
                logger.info("    POST request body:\n" + request_body)
                response = requests.post(endpoint, auth = (username, password), data = request_body.encode('utf-8'), headers = {'Content-Type':'text/plain;charset=UTF-8'})
                logger.info("    POST status code: " + str(response.status_code))
                logger.info("    POST response body: " + response.text)
                count = count + 1
            
logger.info("Total landing page updates: " + str(count))
