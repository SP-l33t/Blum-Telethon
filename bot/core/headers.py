import re


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://telegram.blum.codes',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': 'Android',
    'X-Requested-With': 'org.telegram.messenger',
}


def get_sec_ch_ua(user_agent):
    pattern = r'(Chrome|Chromium)\/(\d+)\.(\d+)\.(\d+)\.(\d+)'

    match = re.search(pattern, user_agent)

    if match:
        browser = match.group(1)
        version = match.group(2)

        if browser == 'Chrome':
            sec_ch_ua = f'"Chromium";v="{version}", "Not;A=Brand";v="24", "Google Chrome";v="{version}"'
        else:
            sec_ch_ua = f'"Chromium";v="{version}", "Not;A=Brand";v="24"'

        return {'Sec-Ch-Ua': sec_ch_ua}
    else:
        return {}
