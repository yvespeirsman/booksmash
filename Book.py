import xml.etree.ElementTree as ET
import HTMLParser

parser = HTMLParser.HTMLParser()

class Book():

    def __init__(self,xml):
        root = ET.fromstring(xml)

        self.title = root.find("Product_Detail").find("Title").text
        self.author = root.find("Product_Detail").find("Product_Contributors").find("Product_Contributor").find("Display_Name").text
        self.cover = root.find("Product_Detail").find("CoverImageURL_Medium").text
        self.isbn = root.find("Product_Detail").find("ISBN").text
        self.desc = root.find("Product_Detail").find("Product_Group_SEO_Copy").text
        self.summary = None
        self.category = None
        self.reviews = {}

        if self.title is not None:
            self.title = parser.unescape(self.title)
        if self.author is not None:
            self.author = parser.unescape(self.author)
        if self.desc is not None:
            self.desc = parser.unescape(self.desc)

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
