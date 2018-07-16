# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import argparse
import time
from datetime import datetime
from pprint import pprint
from oauth2client import file, client, tools 
from apiclient.discovery import build
from httplib2 import Http

class VtuberlivePipeline(object):
    key_file = 'client_secret.json'
    credential_file = './credential.json'
    worksheet_key = "1q2u90mH5Oz2cqDr5W0ItX0sl6YfML0YvJMKR2Tr3CBI"
    rows = [] #list to be appended to Gsheet

    def open_spider(self, spider):
        
        # Setup the Sheets API
        store = file.Storage(self.credential_file)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', 'https://www.googleapis.com/auth/spreadsheets')
            args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args(args.split())
            creds = tools.run_flow(flow, store, flags)
            raise Exception()

        try:
            print("connnecting gsheet....")
            self.service = build('sheets', 'v4', http=creds.authorize(Http()))
        except Exception as err:
            print("Can not connect to Gsheet:" + err)
            raise err
        
    def close_spider(self, spider):
        # append records
        body = {
                "majorDimension": "ROWS",
                "values": self.rows }
        print("appending " + str(len(self.rows)) + " records..")
        request = self.service.spreadsheets().values().append(
                    spreadsheetId = self.worksheet_key,
                    range = "Sheet1!A:G",
                    valueInputOption = "USER_ENTERED",
                    body = body)
        response = request.execute()
        print(response)

    def process_item(self, item, spider):
        now = datetime.now()
        duration = int((int(datetime.utcnow().timestamp()) - int(datetime.strptime(item['actualStartTime'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%s"))) / 60)
        self.rows.append([
            now.strftime("%Y-%m-%d %H:%M"), 
            item['title'],
            item['videoId'],
            item['videoUrl'],
            item['channelName'],
            item['channel'],
            duration,
            item['viewCount'],
            item['concurrentViewCount']
            ])
        return item
