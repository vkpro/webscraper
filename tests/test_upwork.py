import pytest
from selene.browser import open_url
from app.utils import Utils
from selene.api import *
from app.upwork import *
from selene import config


class TestsUpwork(object):
    @pytest.mark.jenkins
    @pytest.mark.parametrize('keyword', ['Selenium', 'Scraping'])
    def test_send_new_jobs_to_slack(self, wd, keyword):
        config.base_url = 'https://www.upwork.com/o/jobs/browse/'

        open_url('?q={_keyword}'.format(_keyword=keyword))

        jobs_results = []
        jobs_list = s(UpworkLocators.JOB_LIST).ss(UpworkLocators.JOB)
        for job in jobs_list:
            title = job.s(UpworkLocators.JOB_TITLE).text
            description = job.s(UpworkLocators.JOB_DESCRIPTION).text
            price = job.ss(UpworkLocators.JOB_PRICE)
            if price:
                price = price[0].text
            else:
                price = None
            link = job.s(UpworkLocators.JOB_TITLE).get_attribute('href')
            posted = job.s(UpworkLocators.JOB_POSTED).text

            jobs_results.append({'title': title,
                                 'description': description,
                                 'price': price,
                                 'link': link,
                                 'posted': posted})

        Utils.notify_slack_upwork(jobs_results)
        Utils.write_csv(jobs_results)


if __name__ == '__main__':
    pytest.main()
