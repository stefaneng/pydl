# Put licence?

import os
import argparse

from bs4 import BeautifulSoup
from urllib2 import urlopen, URLError, HTTPError

# Check out shutil
# shutil.copyfileobj(source, destination)

def get_links(url, ext):
    """
    Takes in a string for the url and a string for the target extention
    """
    try:
        # Reads the url
        html = urlopen(url)
        soup = BeautifulSoup(html)
        # Returns the found links matching extention
        return soup.find_all('a') 

    except HTTPError, e:
        print "HTTP Error: ", e.code, url
    except URLError, e:
        print "URL Error: ", e.code, url

def save_link(url, fileName=None):
    try:
        link = urlopen(url)
        # Test file name
        # Name it with link.info()['Content-Disposition'] ??
        f = open("test.pdf", "wb")
        f.write(link.read())
        f.close()
        #with open(os.path.basename(link), "wb") as f:
        #    f.write(link.read())

    except HTTPError, e:
        print "HTTP Error: ", e.code, url
    except URLError, e:
        print "URL Error: ", e.code, url

def main():
    # Command line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url to download from')
    parser.add_argument('ext', help='extention of file to download')
    parser.add_argument('-v', '--verbose', help='display what is going on',
                        action='store_true')
    args = parser.parse_args()
    if args.verbose:
        print get_links(args.url, args.ext)
    else:
        get_links(args.url, args.ext)
    
    # This is just a test pdf
    save_link("http://www.elsevierdirect.com/downloads/SyngressFreeE-booklets/Certification/1597491535.pdf")


if __name__ == '__main__':
    main()
