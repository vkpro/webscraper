import pytest
from selene import config
from selene.browser import open_url
from app.freelancercom import FreelancerSearchPage
from app.utils import Utils


class TestsFreelancercom(object):
    @pytest.mark.jenkins
    @pytest.mark.parametrize('keyword', ['Selenium', 'Scraping'])
    def test_send_new_jobs_to_slack(self, wd, keyword):
        config.base_url = 'https://www.freelancer.com/jobs/regions/'

        open_url("")
        jobs_el = FreelancerSearchPage.search_job(keyword)
        jobs_result = FreelancerSearchPage.get_jobs_from_page(jobs_el)
        Utils.notify_slack(jobs_result)
        Utils.write_csv(jobs_result)


if __name__ == '__main__':
    pytest.main()
