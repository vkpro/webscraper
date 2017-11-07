import argparse
import csv
import os

from openpyxl import Workbook, load_workbook
from slacker import Slacker
from conf.config import *


class Utils(object):
    @staticmethod
    def send_msg_to_slack(channel=None, _string='', slack_token=''):
        slack = Slacker(slack_token)
        slack.chat.post_message(channel, _string)

    @staticmethod
    def is_string_in_csv(_string, filepath=CSV_FILEPATH):
        if not os.path.isfile(filepath):
            open(filepath, 'a').close()
        with open(filepath, mode='r', encoding="utf8") as f:
            reader = csv.reader(f)
            for row in reader:
                if _string in row:
                    return True

    @staticmethod
    def create_parser():
        _parser = argparse.ArgumentParser(
            description='The script saves jobs info from freelancer.com to csv and xlsx-file.')
        _parser.add_argument('-k', '--keyword', help='keyword for searching', default='KEYWORD')
        _parser.add_argument('-p', '--pages', help='number of pages for scraping', default=1)
        return _parser

    @staticmethod
    def write_csv(data, filepath=CSV_FILEPATH, header=('title', 'description', 'price', 'bids', 'days', 'link')):
        with open(filepath, 'a+', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(header)
            for row in data:
                filewriter.writerow([value for value in row.values()])

    @staticmethod
    def write_xlsx(data, sheet_title='NewSheet', filepath=XLSX_FILEPATH,
                   header=('title', 'description', 'price', 'bids', 'days', 'link')):
        try:
            wb = load_workbook(filepath)
        except FileNotFoundError:
            wb = Workbook()
        ws = wb.create_sheet(sheet_title)
        ws.append(header)
        if data:
            for item_info in data:
                ws.append([value for value in item_info.values()])
        wb.save(filepath)

    @staticmethod
    def notify_slack(results, _slack_token=SLACK_TOKEN):
        # Send slack notification if new result
        for result in results:
            if not Utils.is_string_in_csv(result['title']):
                msg = "Title: {} \nDescription: {} \nBids: {} \nPrice: {} \nDays: {} \nLink: {}" \
                    .format(result['title'], result['description'], result['bids'], result['price'], result['days'],
                            result['link'])
                Utils.send_msg_to_slack(channel="#flcom_web-scraping", _string=msg, slack_token=_slack_token)

    # TODO: Replace this method with ordered dict here
    @staticmethod
    def notify_slack_upwork(results, _slack_token=SLACK_TOKEN):
        # Send slack notification if new result
        for result in results:
            if not Utils.is_string_in_csv(result['title']):
                msg = "Title: {} \nDescription: {} \nPrice: {} \nLink: {} \n Posted: {}" \
                    .format(result['title'], result['description'], result['price'], result['link'], result['posted'])
                Utils.send_msg_to_slack(channel="#flcom_web-scraping", _string=msg, slack_token=_slack_token)
