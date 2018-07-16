# -*- coding: utf-8 -*-
import scrapy
import json
import vtuberlive.settings
from vtuberlive.items import VtuberliveItem 
from pprint import pprint
from urllib.request import urlopen

class LivelistSpider(scrapy.Spider):
    name = 'livelist'
    youtube_key = '--yourkey--'
    allowed_domains = ['virtual-youtuber.userlocal.jp']
    start_urls = ['http://virtual-youtuber.userlocal.jp/lives']

    def parse(self, response):
        for sel in response.css("div.card-live"):
            live = VtuberliveItem()
            live['title'] = sel.css("::attr(data-title)").extract_first()
            live['videoId'] = sel.css("::attr(data-id)").extract_first()
            live['videoUrl'] = sel.css("::attr(data-link)").extract_first()
            live['channel'] = sel.css("::attr(data-channel-link)").extract_first()
            live['channelName'] = sel.css("::attr(data-name)").extract_first()
            # create youtube API request
            url = "https://www.googleapis.com/youtube/v3/videos?" + \
                    "id=" + live['videoId'] + \
                    "&key=" + self.youtube_key + \
                    "&fields=items(id,snippet,statistics,contentDetails,liveStreamingDetails)&part=snippet,statistics,contentDetails,liveStreamingDetails"
            res = urlopen(url)
            data = json.loads(res.read().decode('utf8'))
            live['viewCount'] = data['items'][0]['statistics']['viewCount']
            if 'liveStreamingDetails' in data['items'][0]:
                if 'concurrentViewers' in data['items'][0]['liveStreamingDetails']:
                    live['concurrentViewCount'] = data['items'][0]['liveStreamingDetails']['concurrentViewers']
                else:
                    live['concurrentViewCount'] = 0
                live['actualStartTime'] = data['items'][0]['liveStreamingDetails']['actualStartTime']
            live['title'] =data['items'][0]['snippet']['title'] 
            yield live

