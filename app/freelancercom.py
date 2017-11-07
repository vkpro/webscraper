from selene.api import *
from selene.browser import open_url
from selenium.webdriver.common.by import By


class FreelancercomLocators(object):
    NEXT_BTN = (By.XPATH, '(//*[@data-link="next_page"])[1]')
    JOB_LIST = (By.CSS_SELECTOR, ".JobSearchCard-item-inner")
    JOB_TITLE = ".JobSearchCard-primary-heading-link"
    JOB_DESCRIPTION = ".JobSearchCard-primary-description"
    JOB_PRICE = ".JobSearchCard-secondary-price"
    JOB_BIDS = ".JobSearchCard-secondary-entry"
    JOB_LINK = '.JobSearchCard-primary-heading>a'
    JOB_DAYS = '.JobSearchCard-primary-heading-Days'


class FreelancerSearchPage(object):
    @staticmethod
    def search_job(keyword):
        s('#keyword-input').set_value(keyword).press_enter()
        jobs_el = ss(FreelancercomLocators.JOB_LIST)
        return jobs_el

    @staticmethod
    def get_jobs_from_page(jobs_el):
        jobs_info = []
        for job in jobs_el:
            title = job.s(FreelancercomLocators.JOB_TITLE).text
            description = job.s(FreelancercomLocators.JOB_DESCRIPTION).text
            price = job.ss(FreelancercomLocators.JOB_PRICE)
            if price:
                price = price[0].text
            else:
                price = None
            bids = job.s(FreelancercomLocators.JOB_BIDS).text
            link = job.s(FreelancercomLocators.JOB_LINK).get_attribute('href')
            days = job.s(FreelancercomLocators.JOB_DAYS).text

            jobs_info.append({'title': title,
                              'description': description,
                              'price': price,
                              'bids': bids,
                              'link': link,
                              'days': days})
        return jobs_info

    @staticmethod
    def get_jobs_from_pages(keyword):
        jobs_info = []
        page_num = 1
        while True:
            open_url("{_page_num}?keyword={_keyword}".format(_page_num=page_num, _keyword=keyword))
            jobs_el = ss(FreelancercomLocators.JOB_LIST)
            jobs = FreelancerSearchPage.get_jobs_from_page(jobs_el)
            if jobs:
                jobs_info.extend(jobs)
                page_num += 1
            else:
                break
        return jobs_info
