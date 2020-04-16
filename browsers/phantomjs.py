from selenium import webdriver
from os import path


def get_browser(system: str, root_dir: str) -> webdriver.Firefox:
    executable_path = path.abspath(root_dir + '/browsers/phantomjs/' + system + '/bin/phantomjs')
    return webdriver.PhantomJS(executable_path=executable_path)
