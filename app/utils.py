import argparse
import csv
import os
import logging

from openpyxl import Workbook, load_workbook
from slacker import Slacker

XLSX_FILEPATH = "./results.xlsx"
CSV_FILEPATH = "./results.csv"
logger = logging.getLogger(__name__)


class Utils(object):
    @staticmethod
    def send_msg_to_slack(_channel=None, _msg=''):
        slack_token = os.getenv("SLACK_TOKEN")
        if not slack_token:
            return "SLACK_TOKEN not defined"

        slack = Slacker(slack_token)
        slack.chat.post_message(_channel, str(_msg))
        logger.info("Sent message to slack channel '{}':\n '{}' ".format(_channel, _msg))

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
        # TODO: Get rid of hardcode
        with open(filepath, 'a+', newline='', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(header)
            for row in data:
                filewriter.writerow([value for value in row.values()])

    @staticmethod
    def write_xlsx(data, sheet_title='NewSheet', filepath=XLSX_FILEPATH,
                   header=('title', 'description', 'price', 'bids', 'days', 'link')):
        # TODO: Do not create new sheet everytime 
        # TODO: Get rid of hardcode
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
    def send_results_to_slack(channel, results):
        # Send slack notification if new result
        # TODO: Use ordereddict
        for result in results:
            if not Utils.is_string_in_csv(next(iter(result.values()))):
                result = '\n'.join([' : '.join((k, str(result[k]))) for k in sorted(result, key=result.get, reverse=True)])
                Utils.send_msg_to_slack(_channel=channel, _msg=result)
