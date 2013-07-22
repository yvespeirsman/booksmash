import xml.etree.ElementTree as ET
import os
import time


def getAuthors():
    tree = ET.parse('data/hc_authors.xml')
    root = tree.getroot()

    authors = {}

    for el in root.iter('Contributor_List'):
        for author in el.iter('Contributor_Persona_ID'):
            print author.text
            authors[author.text] = 1

    authorList = authors.keys()
    authorList.sort()

    for author in authorList[:100]:
        print '--', author
        uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=catalog&format=XML&authorglobalid="+str(author)+"&apikey=6wbqgghpzmxhmtf5dmykv2bj" 
   
        os.system('curl "' + uri + '" > data/products/' + str(author) + '.xml')
       

