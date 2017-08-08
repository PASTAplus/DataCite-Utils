import requests, sys
import logging

from doi_list import get_doi_list

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='publisher.log',
                    level=logging.INFO)

logger = logging.getLogger('publisher')

endpoint = 'https://mds.datacite.org/metadata/'

if (len(sys.argv) < 3):
    raise Exception('Please provide username and password')

username, password = sys.argv[1:]
doi_list = get_doi_list(username, password)

count = 0
lter_publisher = "<publisher>Long Term Ecological Research Network</publisher>"
edi_publisher =  "<publisher>Environmental Data Initiative</publisher>"

for doi in doi_list:
    if "10.6073/PASTA" in doi:
        datacite_get_url = endpoint + doi
        response = requests.get(datacite_get_url, auth=(username, password))
        logger.info("DOI: " + doi + "  GET status code: " + str(response.status_code))
        if response.status_code == 200:
            metadata_xml = response.text
            if lter_publisher in metadata_xml:
                metadata_xml = metadata_xml.replace(lter_publisher, edi_publisher)
                response = requests.post(endpoint, auth = (username, password), data = metadata_xml.encode('utf-8'), headers = {'Content-Type':'text/plain;charset=UTF-8'})
                logger.info("    POST status code: " + str(response.status_code))
                logger.info("    POST response body: " + response.text)
                count = count + 1

logger.info("Total publisher updates: " + str(count))
