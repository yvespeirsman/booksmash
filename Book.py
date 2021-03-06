import xml.etree.ElementTree as ET
import HTMLParser
import re

parser = HTMLParser.HTMLParser()

class Book():

    def __init__(self,xml):
        root = ET.fromstring(xml)

        self.title = root.find("Product_Detail").find("Title").text
        authors = []
        contributors = root.find("Product_Detail").find("Product_Contributors").findall("Product_Contributor")
        for contributor in contributors:
            name = contributor.find('Display_Name')
            authors.append(name.text)
        self.author = ", ".join(authors)
        self.cover = root.find("Product_Detail").find("CoverImageURL_Medium").text
        self.isbn = root.find("Product_Detail").find("ISBN").text
        self.desc1 = root.find("Product_Detail").find("Product_Group_SEO_Copy").text
        self.desc1 = re.sub('\n+','\n', self.desc1)
        if self.desc1 is not None:
            self.desc1 = parser.unescape(self.desc1)
        self.desc = self.desc1.split("\n")
        while self.desc[0] == '':
            self.desc = self.desc[1:]

        self.summary = None
        self.category = None
        self.reviews = {}

        if self.title is not None:
            self.title = parser.unescape(self.title)
        if self.author is not None:
            self.author = parser.unescape(self.author)

        for el in root.iter("Product_Content"):
            t = el.find('Content_Type_ID').text
            if t == "605":
                self.summary = el.find('Content_Area1').text
                self.summary = parser.unescape(self.summary)

            elif t == "618":
                review = el.find('Content_Area1').text
                reviewer = el.find('Content_Area3').text
                self.reviews[parser.unescape(reviewer)] = parser.unescape(review)

        for el in root.iter("Product_Categories"):
            for el2 in el.iter("Product_Category"):
                t = el2.find("Category_Type_Desc")
                if t is not None:
                    cattype = t.text
                    if cattype == "MKTSUBJECT":
                        self.category = el2.find("Category_Desc").text
