# Author: Stefan Eng
# License: GPLv3

#import os
import argparse
import re

from os.path import basename
from bs4 import BeautifulSoup
from urllib2 import urlopen, URLError, HTTPError

def get_links(url, ext, verbose=False):
    """
    Takes in a string for the url and a string for the target extention.
    """
    try:
        # Reads the url
        html = urlopen(url)
        # Gets the html in a better format
        soup = BeautifulSoup(html)
        # Returns the found links matching extention
        all_links = soup.find_all('a')
        regex = re.compile('.*\.' + ext)
        new_links = [x for x in all_links 
                     if regex.search(x.get('href'))]
        # Print all information if user wants it
        if verbose:
            print 'Matching extention: ' + ext
            print '---------------------------'
            for i in new_links:
                print i.get('href')

        return new_links

    except HTTPError, e:
        print "HTTP Error: ", e.code, url
    except URLError, e:
        print "URL Error: ", e.code, url

def save_link(url, filename=None):
    '''
    Saves a link from a url to a filename
    Default value is the original filename from the website
    '''
    try:
        # Opens the url for reading
        link = urlopen(url)
        if filename:
            name = filename
        else:
            name = basename(url)
        with open(name, 'w+') as f:
            print 'Downloading......' + basename(url)
            f.write(link.read())
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
    parser.add_argument('-q', '--quiet', 
                        help='silences prompts and saves as original filename',
                        action='store_true')
    args = parser.parse_args()
    links = get_links(args.url, args.ext)

    # User wants more output
    if args.verbose:
        for x in links:
            print basename(x.get('href'))

    for i in links:
        # Use does not want to be prompted, saves files with default name
        if args.quiet:
            save_link(i.get('href'))
        else:
            print "Do you want to save: " + basename(i.get('href')) + " ?"
            var = raw_input("[y/n]: ")
            if var == 'y':
                var = raw_input("Rename to: ")
                save_link(i.get('href'),var)

if __name__ == '__main__':
    main()
