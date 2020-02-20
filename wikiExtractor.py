from bs4 import BeautifulSoup
import requests
import os
import hashlib

NOT_FOUND = "Wikipedia does not have an article with this exact name."


def extractWikiContent(meshJSON):
    for mesh in meshJSON:
        meshDir = os.listdir("wiki_content")
        meshHashUID = hashlib.md5(mesh["uid"].encode())
        meshHashRes = meshHashUID.hexdigest()
        if meshHashRes not in meshDir:
            term = mesh["term"]
            response = requests.get("https://en.wikipedia.org/wiki/" + term)
            soup = BeautifulSoup(response.content, 'html.parser')
            allB = soup.find_all('b')
            textInB = []
            if len(allB) > 0:
                for b in allB:
                    textInB.append(b.text)
            if NOT_FOUND in textInB:
                continue
            else:
                for script in soup('script'):
                    script.decompose()
                for style in soup('style'):
                    style.decompose()
                for link in soup('link'):
                    link.decompose()
                for meta in soup('meta'):
                    meta.decompose()

                print(soup.get_text(" ", strip=True))
