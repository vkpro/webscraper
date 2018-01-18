import pytest
from selene import config
from selene.browser import open_url
from app.freelancercom import FreelancerSearchPage
from app.utils import Utils

CSV_FILE_NAME = "flcom_results.csv" 
XLSX_FILE_NAME = "flcom_results.xlsx" 

class TestsFreelancercom(object):
    @pytest.mark.run_Freelancercom
    @pytest.mark.jenkins
    @pytest.mark.parametrize('keyword', ['Selenium', ])
    def test_send_new_jobs_to_slack(self, wd, keyword):
        config.base_url = 'https://www.freelancer.com/jobs/regions/'

        open_url("")
        jobs_el = FreelancerSearchPage.search_job(keyword)
        jobs_result = FreelancerSearchPage.get_jobs_from_page(jobs_el)
        Utils.send_results_to_slack('jobs', jobs_result, file_name=CSV_FILE_NAME)
        Utils.write_csv(jobs_result, file_name=CSV_FILE_NAME)
        Utils.write_xlsx(jobs_result, file_name=XLSX_FILE_NAME)


if __name__ == '__main__':
    pytest.main()
