import requests
import os
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
import sys

parser = argparse.ArgumentParser(description="Download Videos from NHK World")
parser.add_argument("--url", help="Video url to download")
args = parser.parse_args() # parses sys.argv

url = args.url

if url is None:
    print("Give me an URL please!", file=sys.stderr)
    sys.exit(-1) 

result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(result.content, 'html.parser')

divs = soup.find('div', attrs={'class':'c-episodeInfo__title'})
divs2 = soup.find('div', attrs={'class':'c-episodeInfo__program'})
spans = soup.find('span', attrs={'class':'c-episodeInfo__broadcastDate'})
match = soup.find('div', attrs={'class':'c-floatingVideo__player'})

for div in divs:
    title = div.string

for div in divs2:
    program = div.string
	
for span in spans:
    dt = span.string

date = datetime.strptime(dt, '%B %d, %Y').strftime('%Y-%m-%d')
s = match.attrs['data-src']

plist = 'https://player.ooyala.com/hls/player/all/' + s + '/media/1116.m3u8'	

subprocess.call(['ffmpeg', '-i', f'{plist}', '-codec', 'copy', f'{date}_{program} - {title}.mkv'])


