import sys
import requests
from bs4 import BeautifulSoup


if len(sys.argv) != 3:
    print("You did not enter two URLs.")
    print("Please run the program like this:")
    print("python simhash_compare.py https://example1.com https://example2.com")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

print("Now we will compare two web pages using SimHash")
print("\n")

def getCleanText(url):
    htmlWebPage = requests.get(url)
    htmlPlainTxt = htmlWebPage.text
    htmlStrutured = BeautifulSoup(htmlPlainTxt, "html.parser")

    allscriptstag = htmlStrutured.find_all("script")
    for scripttags in allscriptstag:
        scripttags.extract()

    allstylesTag = htmlStrutured.find_all("style")
    for styleTags in allstylesTag:
        styleTags.extract()

    finalTxt = htmlStrutured.get_text()
    return finalTxt

t1 = getCleanText(url1)
t2 = getCleanText(url2)

def calWordFreq(text):
    wordFreq = {}
    words = text.lower().split()
    for word in words:
        word = word.strip()
        if word.isalnum():
            if word in wordFreq:
                wordFreq[word] = wordFreq[word] + 1
            else:
                wordFreq[word] = 1
    return wordFreq

freq1 = calWordFreq(t1)
freq2 = calWordFreq(t2)
P = 53
M = 2**64

def calculateHash(word):
    hashValue = 0
    pow = 1
    for ch in word:
        asciVal = ord(ch)
        hashValue = hashValue + asciVal * pow
        pow = pow * P
    hashValue = hashValue % M
    return hashValue

def calculateSimhash(wordFrequency):
    vector = [0] * 64
    for word in wordFrequency:
        hashValue = calculateHash(word)
        weight = wordFrequency[word]
        for i in range(64):
            bit = (hashValue >> i) & 1
            if bit == 1:
                vector[i] = vector[i] + weight
            else:
                vector[i] = vector[i] - weight
    finalSimhash = 0
    for i in range(64):
        if vector[i] > 0:
            power = 2 ** i
            finalSimhash = finalSimhash + power
    return finalSimhash

simhash1 = calculateSimhash(freq1)
simhash2 = calculateSimhash(freq2)


print("Simhash value for the first web page is -")
print(simhash1)
print("\n")

print("Simhash value of second web page is -")
print(simhash2)
print("\n")

xorval = simhash1 ^ simhash2
differentBits = 0
temp = xorval
while temp > 0:
    if temp % 2 == 1:
        differentBits += 1
    temp = temp // 2
commonbits = 64 - differentBits

print("Number of common bits between both web pages is -")
print(commonbits)