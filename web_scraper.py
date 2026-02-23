
import sys
from bs4 import BeautifulSoup
import requests

if len(sys.argv) != 2:
    print("You did not enter URL.")
    print("Please run the program like this:")
    print("python web_scraper.py https://example.com")
    sys.exit()

url = sys.argv[1]

htmlWebPage = requests.get(url)

htmlPlainTxt = htmlWebPage.text
htmlStrutured = BeautifulSoup(htmlPlainTxt, "html.parser")

print ("let us print the web pages results as follows Page Titles, Page Body and Links")
print("Page title -")
if htmlStrutured.title is not None:
    title_text = htmlStrutured.title.text
    title_text = title_text.strip()
    print(title_text)
else:
    print("No title is present in this web page")
print ("\n")

print("Page body - ")

allscriptstag = htmlStrutured.find_all("script")
for scripttags in allscriptstag:
    scripttags.extract()

allstylesTag = htmlStrutured.find_all("style")
for styleTags in allstylesTag:
    styleTags.extract()

finalTxt = htmlStrutured.get_text()

allLines = finalTxt.split("\n")

for line in allLines:
    line = line.strip()
    print(line)
print("\n")

print("All links - ")

allLinks = htmlStrutured.find_all("a")

for link in allLinks:
    address = link.get("href")
    print(address)