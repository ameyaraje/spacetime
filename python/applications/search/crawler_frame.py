import logging
from datamodel.search.datamodel import ProducedLink, OneUnProcessedGroup, robot_manager
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import urlparse
from bs4 import BeautifulSoup
from urlparse import urljoin
#from sets import Set

import re, os
from time import time

try:
    # For python 2
    from urlparse import urlparse, parse_qs
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs


logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"
url_count = 0 if not os.path.exists("successful_urls.txt") else (len(open("successful_urls.txt").readlines()) - 1)
if url_count < 0:
    url_count = 0
MAX_LINKS_TO_DOWNLOAD = 20

mainDict = {}

@Producer(ProducedLink)
@GetterSetter(OneUnProcessedGroup)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        # Set app_id <student_id1>_<student_id2>...
        self.app_id = "54729960"
        # Set user agent string to IR W17 UnderGrad <student_id1>, <student_id2> ...
        # If Graduate studetn, change the UnderGrad part to Grad.
        self.UserAgentString = "IR W17 Grad 54729960"
		
        self.frame = frame
        assert(self.UserAgentString != None)
        assert(self.app_id != "")
        if url_count >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def initialize(self):
        self.count = 0
        l = ProducedLink("http://www.ics.uci.edu", self.UserAgentString)
        print l.full_url
        self.frame.add(l)

    def update(self):
        for g in self.frame.get(OneUnProcessedGroup):
            print "Got a Group"
            outputLinks = process_url_group(g, self.UserAgentString)
            for l in outputLinks:
                if is_valid(l) and robot_manager.Allowed(l, self.UserAgentString):
                    lObj = ProducedLink(l, self.UserAgentString)
                    self.frame.add(lObj)
        if url_count >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def shutdown(self):
        print "downloaded ", url_count, " in ", time() - self.starttime, " seconds."
        pass

def save_count(urls):
    global url_count
    url_count += len(urls)
    with open("successful_urls.txt", "a") as surls:
        surls.write("\n".join(urls) + "\n")

def process_url_group(group, useragentstr):
    rawDatas, successfull_urls = group.download(useragentstr, is_valid)
    save_count(successfull_urls)
    return extract_next_links(rawDatas)
    
#######################################################################################
'''
STUB FUNCTIONS TO BE FILLED OUT BY THE STUDENT.
'''
def extract_next_links(rawDatas):
    outputLinks = list()
    '''
    rawDatas is a list of tuples -> [(url1, raw_content1), (url2, raw_content2), ....]
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.

    Suggested library: lxml
    '''

    count = 0
    '''
    for url, content in rawDatas:
        print "FIRST URL IS : " , url
        soup = BeautifulSoup(url)
        links = soup.find_all('a')
        for tag in links:
            link = tag.get('href', None)
            print "Link is:  ", link
            if link is not None:
                print "Extracted link: ", link
        count = count + 1
    '''

    for url, content in rawDatas:
        count = count + 1
        soup = BeautifulSoup(content, "lxml")
        links = soup.find_all('a')
        for tag in links:
            link = tag.get('href', None)
            count = count+1
            print "Link retrieved is", link
            if len(link) < 2:
                continue
            if not link.startswith('http'):
                print "BEFORE:", link
                link = urljoin(url, link)
                print "AFTER append" , link
            if is_valid(link):
                print "Valid link" , link
            #outputLinks.append(link)
    print "Count : ", count

    return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be downloaded or not.
    Robot rules and duplication rules are checked separately.

    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse.urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False

    '''
    TODO: Extract params and add them to a dictionary for every path
    Once this count reaches 50, do a % match and ignore successive URLs
    '''

    '''
       1. Parse the queryParams as a set
       2. Create a dictionary for subdomain -> path
       3. Create a sub-dictionary for path -> queryParams
    '''

    subdomain = parsed.hostname.split('.')[0]
    path = parsed.path
    queryParams = urlparse.parse_qs(urlparse.urlsplit(url).query)

    freqCount = {}
    querySet = set()

    for query, value in queryParams.items():
        querySet.add(query)

    freqCount[querySet] = 1

    fullPath = subdomain + '.' + path

    if mainDict.get(fullPath):
        currParam = mainDict[fullPath]
        for param in currParam:
            if param[queryParams]:
                if param[queryParams] < 50:
                    param[queryParams] = param[queryParams] + 1
                else:
                    param[queryParams] = 1
            else:
                return False
    mainDict[fullPath] = {freqCount}

    #pathDict[path, querySet]


    # if dict.get(parsed.path):
    #     if dict.get(parsed.path < 50):
    #         dict[parsed.path] = dict.get(parsed.path)+1
    #     else:
    #         return False
    # else:
    #     dict[parsed.params] = 1

    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
