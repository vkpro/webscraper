import collections
from selene.api import *
from selene.browser import open_url
from selenium.webdriver.common.by import By
import logging
from time import sleep

logger = logging.getLogger(__name__)


class UpworkLocators(object):
    JOB_LIST = '#jobs-list'
    JOB = '.job-tile'
    JOB_TITLE = '.job-title-link'
    JOB_DESCRIPTION = ".description"
    JOB_PRICE = ".js-budget"
    JOB_POSTED = '.js-posted'


class UpworkSearchPage(object):

    @staticmethod
    def get_jobs_from_page(keyword):

        jobs_info = []
        jobs_list = s(UpworkLocators.JOB_LIST).ss(UpworkLocators.JOB)
        for job in jobs_list:

            def get_text(element):
                # TODO: Try to use Selene instead this
                if element:
                    return element[0].text
                else:
                    return 'N/A'

            job_info = collections.OrderedDict()

            title = job.s(UpworkLocators.JOB_TITLE)
            job_info['title'] = title.text

            description = job.s(UpworkLocators.JOB_DESCRIPTION)
            job_info['description'] = description.text

            price = job.ss(UpworkLocators.JOB_PRICE)
            job_info['price'] = get_text(price)

            job_info['link'] = job.s(UpworkLocators.JOB_TITLE).get_attribute('href')

            posted = job.s(UpworkLocators.JOB_POSTED)
            job_info['posted'] = posted.text

            job_info['keyword'] = keyword

            jobs_info.append(job_info)

        return jobs_info
