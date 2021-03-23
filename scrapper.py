#!/usr/bin/python

from bs4 import BeautifulSoup
import requests, os

def get_chapter_links(url):
    r =  requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    return [a["href"] for a in soup.find_all("a", href=True) if url in a["href"]]

def get_page_links(url):
    r =  requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    return [img["data-src"] for img in soup.find_all("img", {"data-src": True})]

def download_image(url, path):
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)

def main(base_url, base_dir):

    chapter_links = get_chapter_links(base_url)

    for i, chap_link in enumerate(reversed(chapter_links)):

        print(f"Downloading {chap_link}")
        page_links = get_page_links(chap_link)
        chapter_path = os.path.join(base_dir, str(i+1))
        os.mkdir(chapter_path)

        for j, p_link in enumerate(page_links):

            image_path = os.path.join(chapter_path, str(j+1)+".png")
            download_image(p_link.strip(), image_path)

if __name__ == "__main__":
    main("https://www.scan-fr.cc/manga/ascension/", "/home/vzl3ntin/Documents/Scans/ascension")
    main("https://www.scan-fr.cc/manga/jujutsu-kaisen/", "/home/vzl3ntin/Documents/Scans/jujutsu-kaisen")
