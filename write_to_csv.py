import requests
from bs4 import BeautifulSoup
import time

START_DATE = '2022-12-27'

fetch_more_page = True
path = 'front?day=' + START_DATE
DATA = []
days = 1

while days < 10:
    time.sleep(2)
    print("Path " + path)
    page = requests.get('https://news.ycombinator.com/' + path)
    soup = BeautifulSoup(page.text)
    stories = soup.body.center.table.find_all('tr', {"class": "athing"})
    for story in stories:
        storyId = "https://news.ycombinator.com/item?id=" + story.attrs['id']
        storyUrl = story.find_all('a')[1].attrs['href']
        # the story might be a Ask HN, or tell HN
        if storyUrl.startswith('http'):
            DATA.append([storyId, storyUrl])
    more_link = soup.body.center.table.find_all('a', {"class": "morelink"})
    if len(more_link):
        path = more_link[0].attrs['href']
    else:
        # go back a date
        days+=1
        print(soup.find_all('span', {"class": "hnmore"}))
        path = soup.find_all('span', {"class": "hnmore"})[0].a.attrs['href']

print(DATA)


# import csv
# filename = "hn_records.csv"
# fields=['url','discussed_url']
# with open(filename, 'w') as csvfile:
    
#     csvwriter = csv.writer(csvfile)
    
#     csvwriter.writerow(fields)
    
#     csvwriter.writerows(DATA)