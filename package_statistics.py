import time
import argparse
import requests
from bs4 import BeautifulSoup
import re

url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def query(architecture):

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        directorylist = soup.find_all('a')
        
        i = 1
        for link in directorylist: 
            href = link.get('href')
            # if href and href.startswith('Contents-') and href.endswith('.gz') and architecture in href:
            if re.search(rf'Contents-.*{re.escape(architecture)}.*.gz', href):
                print(f'{i}. {href}')
                i += 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('architecture', help="Architecture to query (ex: amd64, arm64)") 
    args = parser.parse_args()

    # start_time = time.perf_counter()
    query(architecture=args.architecture)
    # end_time = time.perf_counter()

    # elapsed_time = end_time - start_time
    # print(f"Query exec time: {elapsed_time:.4f} seconds")
