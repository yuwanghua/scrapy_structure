"""
钩子方法，不需要主动去调函数。scrapy框架会主动运行。————>回调方法————>callback
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
import openpyxl


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()  # 里面有个默认的工作表，用默认的：ws = wb.active,ws.title = 'Top250'
        # sheet_name = wb.create_sheet()
        self.ws = self.wb.active
        self.ws.title = 'Top250'
        self.ws.append(('标题', '评分', '主题', '时长', '简介 '))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.wb.save('电影数据.xlsx')

    # 每拿到一条数据就执行一次
    def process_item(self, item, spider):
        # 可以实现批处理，加个容器
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        duration = item.get('duration', '')
        introduce = item.get('introduce', '')
        self.ws.append((title, rank, subject, duration, introduce))
        # self.ws.append((item['title'], item['rank'], item['subject'])) 方括号哪去的值没有，报异常
        return item  # Terminal是否能看到数据


class DbPipeline:
    def __init__(self):
        self.mydb = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456'
                                    , db='test01', charset='utf8mb4')
        self.cursor = self.mydb.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
            self.mydb.close()

    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        duration = item.get('duration', '')
        introduce = item.get('introduce', '')
        self.data.append((title, rank, subject, duration, introduce))
        if len(self.data) == 100:
            self._write_to_db()
            self.data.clear()
        return item

    def _write_to_db(self):
        self.cursor.execute(
            'insert into tb_top_movie (title, rating, subject, time, introduce) values (%s, %s, %s, %s, $s    )',
            self.data
        )
        self.mydb.commit()
