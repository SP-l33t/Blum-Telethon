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
        version = match.group(2)

        return {'Sec-Ch-Ua': f'"Android WebView";v="{version}", "Chromium";v="{version}", "Not?A_Brand";v="24"'}
    else:
        return {}
