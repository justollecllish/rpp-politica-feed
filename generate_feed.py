import requests
import xml.etree.ElementTree as ET

url = "http://www.rpp.com.pe/actualidad-rss_593.xml"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
root = ET.fromstring(response.content)
channel = root.find('channel')

rss = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>RPP - Solo Política</title>
<link>https://rpp.pe/politica</link>
<description>Noticias de política de RPP filtradas</description>
'''

count = 0
for item in channel.findall('item'):
    link = item.findtext('link', '')
    title = item.findtext('title', '')
    pub_date = item.findtext('pubDate', '')
    description = item.findtext('description', '')

    if 'politic' in link.lower() or 'politic' in title.lower():
        rss += f'''<item>
<title>{title}</title>
<link>{link}</link>
<guid>{link}</guid>
<pubDate>{pub_date}</pubDate>
<description>{description}</description>
</item>
'''
        count += 1

rss += '</channel></rss>'

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print(f"Feed generado con {count} artículos de política")
