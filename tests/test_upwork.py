import collections
import pytest
from selene.browser import open_url
from app.utils import Utils
from selene.api import *
from app.upwork import *
from selene import config

CSV_FILE_NAME = "upwork_results.csv" 
XLSX_FILE_NAME = "upwork_results.xlsx"


class TestsUpwork(object):
    @pytest.mark.run_upwork
    @pytest.mark.parametrize('keyword', ['Selenium', 'Scraping' ])
    def test_send_new_jobs_to_slack(self, wd, keyword):
        config.base_url = 'https://www.upwork.com/o/jobs/browse/'
        open_url('?q={_keyword}'.format(_keyword=keyword))

        jobs_result = UpworkSearchPage.get_jobs_from_page(keyword)
        Utils.send_results_to_slack(channel='job-upwork', results=jobs_result, file_name=CSV_FILE_NAME)
        Utils.write_csv(jobs_result, file_name=CSV_FILE_NAME)

if __name__ == '__main__':
    pytest.main()
