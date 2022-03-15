from bs4 import BeautifulSoup
import dask, requests, time
import pandas as pd

base_url = 'https://www.lider.cl/supermercado/category/Despensa/?No={}&isNavRequest=Yes&Nrpp=40&page={}'

def scrape(id):
    page = id+1; start = 40*page
    bs = BeautifulSoup(requests.get(base_url.format(start,page)).text,'lxml')
    prods = [prod.text for prod in bs.find_all('span',attrs={'class':'product-description js-ellipsis'})]
    prods = [prod.text for prod in prods]
    brands = [b.text for b in bs.find_all('span',attrs={'class':'product-name'})]

    sdf = pd.DataFrame({'product': prods, 'brand': brands})
    return sdf

data = [dask.delayed(scrape)(id) for id in range(10)]
df = dask.delayed(pd.concat)(data)
df = df.compute()

import aiohttp
import asyncio
import requests
import time

from key import key

start_time = time.time()

channel_id = 'UC-QDfvrRIDB6F0bIO4I4HkQ'

url = f'https://www.googleapis.com/youtube/v3/channels?id={channel_id}&key={key}&part=contentDetails'
r = requests.get(url)
results = r.json()['items']

playlist_id = results[0]['contentDetails']['relatedPlaylists']['uploads']

url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&key={key}&part=contentDetails&maxResults=50'

video_ids = []
while True:
    r = requests.get(url)
    results = r.json()
    if 'nextPageToken' in results:
        nextPageToken = results['nextPageToken']
    else:
        nextPageToken = None

    if 'items' in results:
        for item in results['items']:
            videoId = item['contentDetails']['videoId']
            video_ids.append(videoId)

    if nextPageToken:
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&pageToken={nextPageToken}&key={key}&part=contentDetails&maxResults=50'
    else:
        break



'''
view_counts = []
for video_id in video_ids:
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=statistics'
    r = requests.get(url)
    results = r.json()['items']
    viewCount = results[0]['statistics']['viewCount']
    view_counts.append(int(viewCount))
print('Number of videos:', len(view_counts))
print('Average number of views:', sum(view_counts) / len(view_counts))
'''

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video_id in video_ids:
            task = asyncio.ensure_future(get_video_data(session, video_id))
            tasks.append(task)

        view_counts = await asyncio.gather(*tasks)

    print('Number of videos:', len(view_counts))
    print('Average number of views:', sum(view_counts) / len(view_counts))

async def get_video_data(session, video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={key}&part=statistics'

    async with session.get(url) as response:
        result_data = await response.json()
        results = result_data['items']
        viewCount = results[0]['statistics']['viewCount']
        return int(viewCount)

asyncio.run(main())

print("--- %s seconds ---" % (time.time() - start_time))
