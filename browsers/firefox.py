from selenium import webdriver
from os import path


def get_browser(system: str, root_dir: str, headless: bool = True) -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    options.headless = headless
    executable_path = path.abspath(root_dir + '/browsers/firefox/' + system + '/geckodriver')
    return webdriver.Firefox(executable_path=executable_path, options=options)
