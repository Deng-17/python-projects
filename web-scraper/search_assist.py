#! python3
"""Opens up to 5 web links on a subject/topic."""
import sys
import webbrowser

# import urllib.parse

import bs4
import requests

if len(sys.argv) == 1:
    print("Provide a subject or topic with which you need assistance.")
else:
    print("Googling...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(
        "http://google.com/search?q=" + " ".join(sys.argv[1:]),
        headers=headers,
        timeout=10,
    )
    res.raise_for_status()

    # Retrieve top search result links.
    soup = bs4.BeautifulSoup(res.text, features="lxml")

    # Open a browser tab for each result.
    linkElems = soup.select("a[href^='/url?q=']")
    numOpen = min(5, len(linkElems))
    for i in range(numOpen):
        href = linkElems[i].get("href")
        url = href.split("/url?q=")[1].split("&")[0]
        print(f"Opening: {url}")
        webbrowser.open(url)
