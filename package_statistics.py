import io
import time
import argparse
import requests
from bs4 import BeautifulSoup
import re
import gzip
import heapq

# NOTE: this script requires Python 3.14 to be able to use heapify_max and heappop_max

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
            print(f'Using contents file: {href}\n')
            response = requests.get(url + href)

            packages = {}
            if response.status_code == 200:
                
                # get content directly into string to avoid having to write to memory and read
                with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                    output = f.read().decode('utf-8')

                    line_output = output.splitlines()
                    for line in line_output:
                        thispkg = line.rsplit(maxsplit=1)[-1]
                        
                        clean_packages = thispkg.split(',') # if there are multiple packages for one file
                        print(clean_packages)

                        for pkg in clean_packages:
                            if pkg in packages:
                                packages[pkg] += 1
                            else:
                                packages[pkg] = 1
                    
                    package_heap = [(value, key) for key, value in packages.items()]
                    heapq.heapify_max(package_heap)

                    for i in range(10):
                        value, key = heapq.heappop_max(package_heap)
                        print(f'{i+1}. {key}    {value} files')
            
            print(f'--------------------------------')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('architecture', help="Architecture to query (ex: amd64, arm64)") 
    args = parser.parse_args()

    query(architecture=args.architecture)
