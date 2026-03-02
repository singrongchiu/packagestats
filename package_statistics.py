import io
import time
import argparse
import requests
from bs4 import BeautifulSoup
import re
import gzip

url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def query(architecture):
    packages = []

    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        directorylist = soup.find_all('a')
        
        for link in directorylist: 
            href = link.get('href')

            # if href and href.startswith('Contents-') and href.endswith('.gz') and architecture in href:
            if re.search(rf'Contents-(?!udeb).*{re.escape(architecture)}.*.gz', href):
                response = requests.get(url + href)

                if response.status_code == 200:
                    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                        output = f.read().decode('utf-8')
                        print(output)


    # print(f'{i}. {href}')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('architecture', help="Architecture to query (ex: amd64, arm64)") 
    args = parser.parse_args()

    # start_time = time.perf_counter()
    query(architecture=args.architecture)
    # end_time = time.perf_counter()

    # elapsed_time = end_time - start_time
    # print(f"Query exec time: {elapsed_time:.4f} sec")
