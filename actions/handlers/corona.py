import requests, re, os, datetime
from typing.io import TextIO

case_regex = re.compile('<div class=".+">Số ca nhiễm <br> <span class="font24">(\d+)</span></div>')
line_regex = re.compile('^(\d\d/\d\d/\d\d\d\d) \+(\d+) =(\d+)$')


def handle(send_cb: callable, input_m: str) -> bool:
    if not input_m in ['corona hnay', 'corona hqua']:
        return False
    if input_m == 'corona hnay':
        send_cb('hnay co %d ca' % (get_today_new_case()))
        write_today_data()
    elif input_m == 'corona hqua':
        send_cb('hqua co them %d ca, tong so la %d' % (get_yesterday_new(), get_yesterday_total()))
    return True


def get_total_cases() -> int:
    r = requests.get('https://ncov.moh.gov.vn/', verify=False)
    return int(case_regex.findall(r.text)[0])


def get_yesterday_data() -> list:
    data = parse_data()
    t = datetime.date.today() - datetime.timedelta(days=1)
    t = t.strftime('%d/%m/%Y')
    return data[t]


def get_yesterday_new() -> int:
    return get_yesterday_data()[0]


def get_yesterday_total() -> int:
    return get_yesterday_data()[1]


def parse_data() -> dict:
    file = open_data('r')
    ret = {}
    for line in file.readlines():
        date, new, total = line_regex.findall(line)[0]
        ret[date] = [int(new), int(total)]
    close_data(file)
    return ret


def get_today_new_case() -> int:
    return get_total_cases() - get_yesterday_total()


def write_today_data() -> None:
    t = datetime.date.today().strftime('%d/%m/%Y')
    n = get_today_new_case()
    s = get_yesterday_total() + n
    file = open_data('r+')
    data = parse_data()
    data[t] = [n, s]
    for date, data in data.items():
        file.writelines('%s +%d =%d\n' % (date, data[0], data[1]))
    close_data(file)


def open_data(mode: str) -> TextIO:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return open(dir_path + '/corona/cases.data', mode)


def close_data(file: TextIO):
    file.close()
