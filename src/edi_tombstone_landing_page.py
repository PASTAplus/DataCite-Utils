#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: edi_tombstone_landing_page.py

:Synopsis:
    Finds all deprecated DOIs (i.e. those that do not conform with
    the "10.6073/PASTA" format) and resets their landing page to the 
    tombstone landing page on the EDI web site.

:Author:
    Duane Costa

:Created:
    5/24/18
"""
import requests, sys
import logging
from doi_list import get_doi_list

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', 
                    filename='edi_tombstone_landing_page.log',
                    level=logging.INFO)

logger = logging.getLogger('inactivate')

if (len(sys.argv) < 3):
    raise Exception('Please provide username and password')

username, password = sys.argv[1:]

doi_list = get_doi_list(username, password)

datacite_doi_endpoint = 'https://mds.datacite.org/doi/'
tombstone_landing_page = \
    'https://environmentaldatainitiative.org/data-package-not-available'
count = 0

for doi in doi_list:
    if not "10.6073/PASTA" in doi:
        count = count + 1
        landing_page_url = tombstone_landing_page + "?doi=" + doi
        logger.info("Setting tombstone landing page for " + doi + 
                    " to " + landing_page_url)
        request_body = \
                "doi=" + doi + "\n" + "url=" + landing_page_url + "\n"

        try:
            response = \
                requests.post(datacite_doi_endpoint, 
                    auth = (username, password), 
                    data = request_body.encode('utf-8'), 
                    headers = {'Content-Type':'text/plain;charset=UTF-8'})

            logger.info("    POST status code: " + str(response.status_code))
            logger.info("    POST response body: " + response.text)
        except Exception as e:
            msg = str(e) + '\n'
            logger.error('Unknown error: {e}'.format(e=msg))

logger.info("Total DOIs processed: " + str(count))
