import logging
import os
import logging.config

import pytest
import json
from selene import browser
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class WdListener(AbstractEventListener):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def before_navigate_to(self, url, driver):
        self.logger.info("Open {}".format(url))

    def before_find(self, by, value, driver):
        self.logger.info("Finding '{}' by '{}'".format(value, by))

    def after_find(self, by, value, driver):
        self.logger.info("Found '{}' by '{}'".format(value, by))

    def before_click(self, element, driver):
        self.logger.info('Clicking  by element')

    def after_click(self, element, driver):
        self.logger.info('Element clicked')

    def on_exception(self, exception, driver):
        self.logger.error(exception)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser type")
    parser.addoption("--remote_wd", action="store", default="http://127.0.0.1:4444/wd/hub", help="remote server URL")


@pytest.fixture(scope="module")
def browser_type(request):
    """Browser type to run"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="module")
def remote_wd(request):
    """URL of remote wd e.g. http://127.0.0.1:4444/wd/hub"""
    return request.config.getoption("--remote_wd")


@pytest.fixture(scope="module")
def wd(request, browser_type, remote_wd):
    """Webdriver object"""
    setup_logging()
    logger = logging.getLogger(__name__)

    if browser_type == "firefox":
        # wd = webdriver.Firefox()
        wd = EventFiringWebDriver(webdriver.Firefox(), WdListener())
        logger.info("Browser {} started".format(browser_type))
    elif browser_type == "chrome":
        # wd = webdriver.Chrome()
        wd = EventFiringWebDriver(webdriver.Chrome(), WdListener())
        logger.info("Browser {} started".format(browser_type))
    elif browser_type == "phantomjs":
        # wd = webdriver.PhantomJS()
        wd = EventFiringWebDriver(webdriver.PhantomJS(), WdListener())
        logger.info("Browser {} started".format(browser_type))
    elif browser_type == "rfirefox":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "firefox"})
    elif browser_type == "rphantomjs":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "phantomjs"})
    elif browser_type == "rchrome":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "chrome"})
    else:
        raise ValueError("Unrecognized browser %s" % browser_type)

    if browser_type != 'rchrome' and 'chrome':
        wd.maximize_window()

    def fin():
        browser.quit()

    request.addfinalizer(fin)
    browser.set_driver(wd)
