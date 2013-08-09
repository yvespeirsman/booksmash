import xml.etree.ElementTree as ET

class Book():

    def __init__(self,xml):
        root = ET.fromstring(xml)

        self.title = root.find("Product_Detail").find("Title").text
        self.author = root.find("Product_Detail").find("Product_Contributors").find("Product_Contributor").find("Display_Name").text
        self.cover = root.find("Product_Detail").find("CoverImageURL_Medium").text
        self.isbn = root.find("Product_Detail").find("ISBN").text
        self.desc = root.find("Product_Detail").find("Product_Group_SEO_Copy").text
