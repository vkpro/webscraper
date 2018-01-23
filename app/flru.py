import collections
from selene.api import *
import logging
from time import sleep

logger = logging.getLogger(__name__)


class FlruLocators(object):
    SEARCH_FIELD = '#pf_keywords'
    SUBMIT = 'button.b-button.b-button_flat.b-button_flat_green'
    JOB_LIST = '.b-post.b-post_padbot_15.b-post_margbot_20.b-post_bordbot_eee.b-post_relative'
    NEXT_BTN = '#PrevLink'
    JOB_TITLE = '[id^="prj_name"]'
    JOB_DESCRIPTION = ".b-post__body.b-post__body_padtop_15.b-post__body_overflow_hidden.b-layuot_width_full"
    JOB_PRICE = ".b-post__price.b-post__price_padleft_10.b-post__price_padbot_5"
    JOB_BIDS = "a.b-post__txt_float_right.b-page__desktop.b-post__link_margtop_7"


class FlruSearchPage(object):

    @staticmethod
    def search_job(keyword):
        s(FlruLocators.SEARCH_FIELD).set_value(keyword)
        sleep(1)
        s(FlruLocators.SUBMIT).click()

    @staticmethod
    def get_jobs_from_page(keyword):
        jobs_info = []
        job_list = ss(FlruLocators.JOB_LIST)
        if not job_list:
            return None
        for job in job_list:

            def get_text(element):
                # TODO: Try to use Selene instead this
                if element:
                    return element[0].text
                else:
                    return 'N/A'

            job_info = collections.OrderedDict()

            title = job.ss(FlruLocators.JOB_TITLE)
            job_info['title'] = get_text(title)
            logging.debug('Title: {}'.format(title))

            description = job.ss(FlruLocators.JOB_DESCRIPTION)
            job_info['description'] = get_text(description)
            logging.debug('Description: {}'.format(description))

            price = job.ss(FlruLocators.JOB_PRICE)
            job_info['price'] = get_text(price)

            bids = job.ss(FlruLocators.JOB_BIDS)
            job_info['bids'] = get_text(bids)

            job_info['link'] = job.s(FlruLocators.JOB_TITLE).get_attribute('href')

            job_info['keyword'] = keyword

            jobs_info.append(job_info)

        return jobs_info

    @staticmethod
    def get_jobs_from_pages(job_list):
        jobs_info = []
        while True:
            jobs = FlruSearchPage.get_jobs_from_page()
            if jobs:
                jobs_info.extend(jobs)
            else:
                break
            s(FlruLocators.NEXT_BTN).click()
        return jobs_info
