import urllib
import urllib2
import re
import sys
from bs4 import BeautifulSoup

existing_wikis = []
prohibited = ['Type','Latin_language','Wikipedia','Help','File','Latin','History','en','Help']

def find_parent(topic):

    global existing_wikis    
    global prohibited 
    output = ""
    next_page = ""

    article = urllib.quote(topic)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this

    resource = opener.open("http://en.wikipedia.org/wiki/" + article)
    data = resource.read()
    resource.close()
    
    soup = BeautifulSoup(data)
    divTag = soup.find_all("div",{"class":"mw-content-ltr"})
    for tag in divTag:
        for element in tag.find_all("p"):
            output += str(element)    

    #print "\n===\n" + output + "\n===\n"
    pattern = r'/wiki/[A-Z,a-z,1-9,\),\(,_,\-,\:]+'
   
    #print existing_wikis

    for match in re.finditer(pattern,output):
        next_page = match.group().split('/')[2]
        if next_page is None:
            print "[-] No Wikipedia Entry for " + topic 
            sys.exit(1)
        #print "[-] Found link " + next_page        
        #print match.group()         

        if next_page is None:
            print "[-] No Wikipedia Entry for " + topic
            sys.exit(1)

        if next_page in prohibited: 
            #print "[-] Prohibited link found"
            continue

        a = re.compile("^(Help|Wikipedia)\:.+")
        if a.match(next_page):
            continue 

        if next_page == "Philosophy":
            print "[P] Philosophy was reached"
            print existing_wikis
            sys.exit(1)

        if next_page not in existing_wikis:
            #print next_page
            #print "[-] breaking"
            break
    
    existing_wikis.append(next_page)

    #print "[-] returning " + next_page
    return find_parent(next_page)

def main(input):
    print "[-] Searching term " + input + " for parents..."
    find_parent(input)

main(sys.argv[1])    
