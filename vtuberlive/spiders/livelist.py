# -*- coding: utf-8 -*-
import scrapy
import json
import vtuberlive.settings
from vtuberlive.items import VtuberliveItem 
from pprint import pprint
from urllib.request import urlopen

class LivelistSpider(scrapy.Spider):
    name = 'livelist'
    youtube_key = 'AIzaSyAqhRp7T4VfhuUt_Gngz9HWZRSTu9BGS4Q'
    allowed_domains = ['virtual-youtuber.userlocal.jp']
    start_urls = ['http://virtual-youtuber.userlocal.jp/lives']

    def parse(self, response):
        for sel in response.css("div.card-live"):
            live = VtuberliveItem()
            # parse html
            try:
                live['title'] = sel.css("::attr(data-title)").extract_first()
                live['videoId'] = sel.css("::attr(data-id)").extract_first()
                live['videoUrl'] = sel.css("::attr(data-link)").extract_first()
                live['channel'] = sel.css("::attr(data-channel-link)").extract_first()
                live['channelName'] = sel.css("::attr(data-name)").extract_first()
            except:
                print("parse error:" + sel)
            # create youtube API request
            url = "https://www.googleapis.com/youtube/v3/videos?" + \
                    "id=" + live['videoId'] + \
                    "&key=" + self.youtube_key + \
                    "&fields=items(id,snippet,statistics,contentDetails,liveStreamingDetails)&part=snippet,statistics,contentDetails,liveStreamingDetails"
            try:
                res = urlopen(url)
            except Exception as err:
                print("youtube fetch error:" + url + ":" + err)

            # parse json response
            try:
                data = json.loads(res.read().decode('utf8'))
            except: 
                print("youtube parse error:" + url)
            if len(data['items']) == 1:
                live['title'] =data['items'][0]['snippet']['title'] 
                live['viewCount'] = data['items'][0]['statistics']['viewCount']
                if 'liveStreamingDetails' in data['items'][0]:
                    if 'concurrentViewers' in data['items'][0]['liveStreamingDetails']:
                        live['concurrentViewCount'] = data['items'][0]['liveStreamingDetails']['concurrentViewers']
                    else:
                        live['concurrentViewCount'] = 0
                    live['actualStartTime'] = data['items'][0]['liveStreamingDetails']['actualStartTime']
            else:
                print("invalid json response:url(" + url)

            yield live

