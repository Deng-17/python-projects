#! python3
"""Opens up to 5 web links on a subject/topic using Google search."""

import sys
import webbrowser
import requests
import bs4

if len(sys.argv) == 1:
    print("Provide a subject or topic with which you need assistance.")
    sys.exit()

print("Googling...")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(
    "https://www.google.com/search?q=" + " ".join(sys.argv[1:]),
    headers=headers,
    timeout=10,
)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "lxml")

# New reliable selector
link_elems = soup.select("a[href^='/url?q=']")

num_open = min(5, len(link_elems))

for i in range(num_open):
    href = link_elems[i].get("href")
    url = href.split("/url?q=")[1].split("&")[0]
    print(f"Opening: {url}")
    webbrowser.open(url)
