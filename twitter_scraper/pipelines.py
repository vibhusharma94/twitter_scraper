# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import json

from .settings import PROJECT_ROOT

class TwitterScraperPipeline(object):

    def __init__(self): 
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet('twitter')
        # Sheet header, first row
        self.row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['follower_count', 'profile_name', 'handle' ]
        for col_num in range(len(columns)):
            self.ws.write(self.row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        self.font_style = xlwt.XFStyle()

    def process_item(self, item, spider):
        row = list(dict(item).values())
        self.row_num += 1
        for col_num in range(len(row)):
            self.ws.write(self.row_num, col_num, row[col_num], self.font_style)
        self.wb.save(PROJECT_ROOT + '/items.xls')
        return item

        

        
