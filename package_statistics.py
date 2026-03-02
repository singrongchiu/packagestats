import io
import time
import argparse
import requests
from bs4 import BeautifulSoup
import re
import gzip
import heapq

url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def query(architecture):
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        directorylist = soup.find_all('a') # find all links in the page
        
        my_links = []

        # regex pattern (no micro packages)
        pattern = re.compile(rf'Contents-(?!udeb).*{re.escape(architecture)}.*\.gz') 
        my_links = [href for link in directorylist if (href := link.get('href')) 
                    and pattern.search(href)]
        
        for href in my_links:
            print(f'Using contents file: {href}')
            response = requests.get(url + href)

            packages = {}
            if response.status_code == 200:
                
                # get content directly into string to avoid having to write to disk and read
                with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                    output = f.read().decode('utf-8')

                    # TODO: test speed between splitting after decoding all
                    # vs decoding line by line
                    line_output = output.splitlines()
                    for line in line_output:
                        # print(line)
                        thispkg = line.rsplit(maxsplit=1)[-1]
                        # print(thispkg)
                        if thispkg in packages:
                            packages[thispkg] += 1
                        else:
                            packages[thispkg] = 1
                    
                    package_heap = [(value, key) for key, value in packages.items()]
                    heapq.heapify(package_heap)

                    for i in range(10):
                        value, key = heapq.heappop(package_heap)
                        print(f'{i+1}. {key} {value} occurrences')
            
            print(f'--------------------------------')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('architecture', help="Architecture to query (ex: amd64, arm64)") 
    args = parser.parse_args()

    # start_time = time.perf_counter()
    query(architecture=args.architecture)
    # end_time = time.perf_counter()

    # elapsed_time = end_time - start_time
    # print(f"Query exec time: {elapsed_time:.4f} sec")
