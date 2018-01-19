import pytest
from selene import config
from selene.browser import open_url
from app.flru import FlruSearchPage
from app.utils import Utils

CSV_FILE_NAME = "flru_results.csv" 
XLSX_FILE_NAME = "flru_results.xlsx"


class TestsFlru(object):
    @pytest.mark.run_Flru
    @pytest.mark.parametrize('keyword', ['Selenium', 'Парсинг'])
    def test_send_new_jobs_to_slack(self, wd, keyword):
        config.base_url = 'https://www.fl.ru/projects/'

        open_url("")
        FlruSearchPage.search_job(keyword)
        jobs_result = FlruSearchPage.get_jobs_from_page(keyword)
        Utils.send_results_to_slack('jobs', jobs_result, file_name=CSV_FILE_NAME)
        Utils.write_csv(jobs_result, file_name=CSV_FILE_NAME)
        Utils.write_xlsx(jobs_result, file_name=XLSX_FILE_NAME)


if __name__ == '__main__':
    pytest.main()
