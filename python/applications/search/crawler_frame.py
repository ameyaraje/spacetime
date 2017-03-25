import logging
from datamodel.search.datamodel import ProducedLink, OneUnProcessedGroup, robot_manager
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter, Getter
#from lxml import html,etree
import re, os
from time import time
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlsplit


mainDict = {}
subdomains = {}
max_outlinks = -1
max_url = ""

try:
    # For python 2
    from urlparse import urlparse, parse_qs
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs


logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"
url_count = (set()
    if not os.path.exists("successful_urls.txt") else
    set([line.strip() for line in open("successful_urls.txt").readlines() if line.strip() != ""]))
MAX_LINKS_TO_DOWNLOAD = 3500

@Producer(ProducedLink)
@GetterSetter(OneUnProcessedGroup)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        # Set app_id <student_id1>_<student_id2>...
        self.app_id = "54729960_79129624_86124503"
        # Set user agent string to IR W17 UnderGrad <student_id1>, <student_id2> ...
        # If Graduate studetn, change the UnderGrad part to Grad.
        self.UserAgentString = "IR W17 Grad 54729960,79129624,86124503"

        self.frame = frame
        assert(self.UserAgentString != None)
        assert(self.app_id != "")
        if len(url_count) >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def initialize(self):
        self.count = 0
        l = ProducedLink("http://www.ics.uci.edu", self.UserAgentString)
        print l.full_url
        self.frame.add(l)

    def update(self):
        for g in self.frame.get_new(OneUnProcessedGroup):
            print "Got a Group"
            outputLinks, urlResps = process_url_group(g, self.UserAgentString)
            for urlResp in urlResps:
                if urlResp.bad_url and self.UserAgentString not in set(urlResp.dataframe_obj.bad_url):
                    urlResp.dataframe_obj.bad_url += [self.UserAgentString]
            for l in outputLinks:
                if is_valid(l) and robot_manager.Allowed(l, self.UserAgentString):
                    lObj = ProducedLink(l, self.UserAgentString)
                    self.frame.add(lObj)
        if len(url_count) >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def shutdown(self):
        print "downloaded ", len(url_count), " in ", time() - self.starttime, " seconds."
        pass

def save_count(urls):
    global url_count
    urls = set(urls).difference(url_count)
    url_count.update(urls)
    if len(urls):
        with open("successful_urls.txt", "a") as surls:
            surls.write(("\n".join(urls) + "\n").encode("utf-8"))

def process_url_group(group, useragentstr):
    rawDatas, successfull_urls = group.download(useragentstr, is_valid)
    save_count(successfull_urls)
    return extract_next_links(rawDatas), rawDatas

#######################################################################################
'''
STUB FUNCTIONS TO BE FILLED OUT BY THE STUDENT.
'''
#counts the number of urls received
count = 0

#counts the number of bad urls
bad_urls = 0

def extract_next_links(rawDatas):
    outputLinks = list()
    '''
    rawDatas is a list of objs -> [raw_content_obj1, raw_content_obj2, ....]
    Each obj is of type UrlResponse  declared at L28-42 datamodel/search/datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded.
    The frontier takes care of that.

    Suggested library: lxml
    '''

    global count
    global bad_urls
    global max_outlinks
    global max_url
    to_parse = ""

    for rawData in rawDatas:
        print "RAWDATA URL", rawData.url
        # print "RAWDATA RED_URL", rawData.final_url
        # print "RAWDATA STATUS CODE", rawData.http_code
        # print "RAWDATA FLAG", rawData.is_redirected
        if rawData.is_redirected == 1:
            to_parse = rawData.final_url
            # print "URL: ", rawData.final_url
        elif rawData.http_code == 200:
            to_parse = rawData.url
        else:
            bad_urls = bad_urls + 1
            continue

        if is_valid(to_parse) is False:
            bad_urls = bad_urls + 1
            print "BAD URLs:", to_parse
            continue

        count = count+1
        soup = BeautifulSoup(rawData.content, "lxml")
        links = soup.find_all('a')

        if len(links) > max_outlinks:
            max_outlinks = len(links)
            max_url = to_parse

        for tag in links:
            link = tag.get('href', None)
            # print "BEFORE:", link
            link = urljoin(to_parse, link)
            # print link
            print "Link to check is : ", link
            if is_valid(link):
                print "Appending Link: ", link
                outputLinks.append(link)
            else:
                rawData.bad_url = True
                bad_urls = bad_urls + 1
                print "BAD URL is:", link

    writeMaxOutlinks(max_url, max_outlinks)
    countSubdomains(outputLinks)
    print "Total URL Count : ", count
    print "Invalid URLs : ", bad_urls

    return outputLinks


def is_valid(url):
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        if ".ics.uci.edu" in parsed.hostname \
                and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                         + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                         + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                         + "|thmx|mso|arff|rtf|jar|csv" \
                                         + "|c|cc|cpp|m|h"\
                                         + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):

            subdomain = parsed.hostname.split('.')[0]
            path = parsed.path
            queryParams = parse_qs(urlsplit(url).query)

            fullPath = subdomain + '.' + path
            querySet = ""
            global mainDict

            for query, value in queryParams.items():
                # print query
                querySet = querySet + query

            print querySet

            if mainDict.get(fullPath):
                currParams = mainDict[fullPath]
                # print "currParams is ", currParams
                exist = False
                for param in currParams:
                    # print param, ": param"
                    if param.get(querySet):
                        exist = True
                        # print param[querySet]
                        if param[querySet] < 10:
                            param[querySet] = param[querySet] + 1
                        else:
                            return False
                if exist is False:
                    mainDict[fullPath].append({querySet: 1})
            else:
                mainDict.setdefault(fullPath, []).append({querySet: 1})

            return True
        else:
            return False

    except TypeError:
        print ("TypeError for ", parsed)


def countSubdomains(links):
    # print "Called analytics" , links
    str = ""
    index = 0
    index2 = 0

    for link in links:
        if ".ics.uci.edu" in link:

            if "www.ics.uci.edu" in link:

                str = "ics.uci.edu"
                if str in subdomains.keys():
                    subdomains[str] = subdomains[str] + 1
                else:
                    subdomains[str] = 1
                    continue
            else:
                index = 7
                if link.startswith("https://"):
                    index = 8

                index2 = link.find(".ics.uci.edu") + 12
                str = link[index:index2]

                if str in subdomains.keys():
                    subdomains[str] = subdomains[str] + 1
                else:
                    subdomains[str] = 1


    file = open("subdomainsCount1.txt", "w")

    for key, value in subdomains.items():
        file.write(('%s , %s\n' % (key, value)).encode("UTF-8"))

    file.close()

def writeMaxOutlinks(maxURL, number):
    # print "Writing to MAX"
    file1 = open("maxOutlinks1", "w")
    file1.write(('%s , %d\n' % (maxURL, number)).encode("UTF-8"))
    file1.close()