from browsers import firefox, phantomjs
from actions import facebook
from utils import system
from os import path
from time import sleep

# Config
fb_user = 'kybiukybiu@gmail.com'
fb_pwd = 'skynet20152020'
fb_cid = 'g.994597937304071'
web_engine = 'firefox-headless'

if web_engine == 'firefox':
    browser = firefox.get_browser(system=system.get_system(), root_dir=path.abspath('.'), headless=False)
elif web_engine == 'phantomjs':
    browser = phantomjs.get_browser(system=system.get_system(), root_dir=path.abspath('.'))
    browser.set_window_size(1120, 550)
else:
    # Default: headless firefox
    browser = firefox.get_browser(system=system.get_system(), root_dir=path.abspath('.'))

facebook.login(browser, fb_user, fb_pwd)
print('logged in')

while True:
    facebook.open_chat(browser, fb_cid)
    messages = facebook.check_message(browser)
    for m in messages:
        facebook.reply_message(browser, m)
    sleep(2.5)

# browser.quit()
