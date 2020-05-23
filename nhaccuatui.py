from browsers import firefox, phantomjs, chromium
from utils import system
from os import path
import time
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

# Config
web_engine = 'chromium'

if web_engine == 'firefox':
    browser = firefox.get_browser(system=system.get_system(), root_dir=path.abspath('.'), headless=False)
elif web_engine == 'chromium':
    browser = chromium.get_browser(system=system.get_system(), root_dir=path.abspath('.'), headless=False)
    browser.set_window_size(1120, 550)
elif web_engine == 'phantomjs':
    browser = phantomjs.get_browser(system=system.get_system(), root_dir=path.abspath('.'))
    browser.set_window_size(1120, 550)
else:
    # Default: headless firefox
    browser = firefox.get_browser(system=system.get_system(), root_dir=path.abspath('.'))


def download_song(btn: WebElement, retry: int = 0) -> bool:
    try:
        ActionChains(browser).move_to_element(btn).perform()
        btn.click()
        time.sleep(1)
        dl_bs = browser.find_element_by_id('downloadBasic')
        while True:
            time.sleep(1)
            try:
                browser.switch_to.frame(browser.find_element_by_id('ifAdsTVC'))
                browser.find_element_by_css_selector('div.vast-skip-button.enabled').click()
            except NoSuchElementException:
                pass
            time.sleep(1)
            browser.switch_to.default_content()
            class_str: str = dl_bs.get_attribute('class')
            class_lst = class_str.split(' ')
            if 'disabled' not in class_lst:
                dl_bs.click()
                time.sleep(3)
                break
    except ElementNotInteractableException:
        print('retry: ' + str(retry + 1))
        if retry < 3:
            return download_song(btn, retry + 1)
        return False
    return True


def download_playlist(url: str, success: int = 0, fail: int = 0) -> tuple:
    browser.get(url)
    download_buttons = browser.find_elements_by_css_selector('a.button_download')
    for dl_btn in download_buttons:
        result = download_song(dl_btn)
        if result:
            success += 1
            print('downloaded ' + str(success))
        else:
            fail += 1
            print('failed ' + str(fail))
    return success, fail


playlists = [
    'https://www.nhaccuatui.com/playlist/loi-bac-dan-truoc-luc-di-xa-va.PS6hXzS3miDR.html',
    'https://www.nhaccuatui.com/playlist/nhung-bai-hat-cach-mang-di-cung-nam-thang-va.Nxoz1L8RF3gV.html',
    'https://www.nhaccuatui.com/playlist/tuyen-tap-song-ca-nhac-do-va.qNjcFxjHdOLE.html',
    'https://www.nhaccuatui.com/playlist/loi-ca-dang-bac-thu-hien-nsnd.W8345jDXRPNS.html',
    'https://www.nhaccuatui.com/playlist/bai-ca-dat-nuoc-va.MioiLw0vlHMF.html',
    'https://www.nhaccuatui.com/playlist/bai-ca-nam-tan-thu-hien-nsnd.EmhWViuDCZBS.html',
    'https://www.nhaccuatui.com/playlist/cac-ca-khuc-ca-ngoi-bac-va.wu7Ki5LPyqtu.html',
]

s, f = 0, 0
for playlist in playlists:
    s, f = download_playlist(playlist, s, f)
