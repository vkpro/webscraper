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
    # TODO: Clean up log system
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        logging.info("Setup logging from config {}".format(path))
    else:
        logging.basicConfig(level=default_level)
        logging.warning("logging config not found {}. Setup defaults".format(path))


class WdListener(AbstractEventListener):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def before_navigate_to(self, url, driver):
        self.logger.info("Open {}".format(url))

    def before_find(self, by, value, driver):
        self.logger.debug("Finding '{}' by '{}'".format(value, by))

    def after_find(self, by, value, driver):
        self.logger.debug("Found '{}' by '{}'".format(value, by))

    def before_click(self, element, driver):
        self.logger.debug('Clicking  by element')

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

    if browser_type == "firefox":
        wd = webdriver.Firefox()
    elif browser_type == "chrome":
        wd = webdriver.Chrome()
    elif browser_type == "chrome-nogui":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-web-security')
        wd = webdriver.Chrome(chrome_options=options)
    elif browser_type == "rfirefox":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "firefox"})
    elif browser_type == "rchrome":
        wd = webdriver.Remote(remote_wd, desired_capabilities={"browserName": "chrome"})
    elif browser_type == "selenoid_chrome":
        capabilities = {
            "browserName": "chrome",
            "version": "63.0",
            "enableVNC": True,
            "enableVideo": True,
            "screenResolution": "1280x1024x24"
        }
        wd = webdriver.Remote(
            command_executor=remote_wd,
            desired_capabilities=capabilities)
    elif browser_type == "selenoid_firefox":
        capabilities = {
            "browserName": "firefox",
            "version": "57.0",
            "enableVNC": True,
            "enableVideo": True
        }
        wd = webdriver.Remote(
            command_executor=remote_wd,
            desired_capabilities=capabilities)
    else:
        raise ValueError("Unrecognized browser %s" % browser_type)

    if not wd:
        raise RuntimeError("wd is not defined")

    wd = EventFiringWebDriver(wd, WdListener())
    logger.info("Browser {} started".format(browser_type))
    wd.set_window_size(1280, 1024)
    logger.info("Set window size 1280x1024")

    def fin():
        browser.quit()

    request.addfinalizer(fin)
    browser.set_driver(wd)

setup_logging()
logger = logging.getLogger(__name__)
