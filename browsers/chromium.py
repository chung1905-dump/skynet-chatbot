from selenium import webdriver
from os import path


def get_browser(system: str, root_dir: str, headless: bool = True) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.binary_location = '/usr/bin/chromium'
    executable_path = path.abspath(root_dir + '/browsers/chrome/' + system + '/chromedriver')
    return webdriver.Chrome(executable_path=executable_path, options=options)
