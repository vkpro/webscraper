import pytest
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

from selene import browser


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)

    def after_find(self, by, value, driver):
        print(by, value, "found")

    def on_exception(self, exception, driver):
        print(exception)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser type")
    parser.addoption("--remote_wd", action="store", default="http://127.0.0.1:4444/wd/hub", help="remote server URL")


@pytest.fixture(scope="module")
def browser_type(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="module")
def remote_wd(request):
    return request.config.getoption("--remote_wd")


@pytest.fixture(scope="module")
def wd(request, browser_type, remote_wd):
    if browser_type == "firefox":
        wd = webdriver.Firefox()
    elif browser_type == "chrome":
        # wd = webdriver.Chrome()
        wd = EventFiringWebDriver(webdriver.Chrome(), MyListener())
    elif browser_type == "phantomjs":
        wd = webdriver.PhantomJS()
    elif browser_type == "rfirefox":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "firefox"})
    elif browser_type == "rphantomjs":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "phantomjs"})
    elif browser_type == "rchrome":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "chrome"})
    else:
        raise ValueError("Unrecognized browser %s" % browser_type)
    wd.maximize_window()

    def fin():
        browser.quit()

    request.addfinalizer(fin)
    browser.set_driver(wd)
