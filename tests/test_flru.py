import pytest
from selene import config
from selene.browser import open_url
from app.flru import FlruSearchPage
from app.utils import Utils


class TestsFlru(object):
    @pytest.mark.run_Flru
    @pytest.mark.parametrize('keyword', ['Selenium', ])
    def test_send_new_jobs_to_slack(self, wd, keyword):
        config.base_url = 'https://www.fl.ru/projects/'

        open_url("")
        FlruSearchPage.search_job(keyword)
        jobs_result = FlruSearchPage.get_jobs_from_page()
        Utils.send_results_to_slack('jobs', jobs_result)
        Utils.write_csv(jobs_result)
        Utils.write_xlsx(jobs_result)


if __name__ == '__main__':
    pytest.main()
