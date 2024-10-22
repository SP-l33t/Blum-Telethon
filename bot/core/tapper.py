import aiohttp
import asyncio
import json
import string
from urllib.parse import unquote, parse_qs
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from random import randint, uniform, choices
from time import time

from bot.utils.universal_telegram_client import UniversalTelegramClient

from .headers import *
from .helper import format_duration
from bot.config import settings
from bot.utils import logger, log_error, config_utils, CONFIG_PATH, first_run
from bot.exceptions import InvalidSession


class Tapper:
    def __init__(self, tg_client: UniversalTelegramClient):
        self.tg_client = tg_client
        self.session_name = tg_client.session_name

        session_config = config_utils.get_session_config(self.session_name, CONFIG_PATH)

        if not all(key in session_config for key in ('api', 'user_agent')):
            logger.critical(self.log_message('CHECK accounts_config.json as it might be corrupted'))
            exit(-1)

        self.headers = headers
        user_agent = session_config.get('user_agent')
        self.headers['user-agent'] = user_agent
        self.headers.update(**get_sec_ch_ua(user_agent))

        self.proxy = session_config.get('proxy')
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            self.tg_client.set_proxy(proxy)

        self.user_data = None
        self.start_param = None
        self.blum_data = None

        self.gateway_url = "https://gateway.blum.codes"
        self.game_url = "https://game-domain.blum.codes"
        self.wallet_url = "https://wallet-domain.blum.codes"
        self.subscription_url = "https://subscription.blum.codes"
        self.tribe_url = "https://tribe-domain.blum.codes"
        self.user_url = "https://user-domain.blum.codes"
        self.earn_domain = "https://earn-domain.blum.codes"

        self._webview_data = None

    def log_message(self, message) -> str:
        return f"<ly>{self.session_name}</ly> | {message}"

    async def get_tg_web_data(self) -> str:
        webview_url = await self.tg_client.get_app_webview_url('BlumCryptoBot', "app", "ref_WyOWiiqWa4")

        tg_web_data = unquote(string=webview_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        self.user_data = json.loads(parse_qs(tg_web_data).get('user', [''])[0])
        self.start_param = parse_qs(tg_web_data).get('start_param', [''])[0]

        return tg_web_data

    async def check_proxy(self, http_client: CloudflareScraper) -> bool:
        proxy_conn = http_client.connector
        if proxy_conn and not hasattr(proxy_conn, '_proxy_host'):
            logger.info(self.log_message(f"Running Proxy-less"))
            return True
        try:
            response = await http_client.get(url='https://ifconfig.me/ip', timeout=aiohttp.ClientTimeout(15))
            logger.info(self.log_message(f"Proxy IP: {await response.text()}"))
            return True
        except Exception as error:
            proxy_url = f"{proxy_conn._proxy_type}://{proxy_conn._proxy_host}:{proxy_conn._proxy_port}"
            log_error(self.log_message(f"Proxy: {proxy_url} | Error: {type(error).__name__}"))
            return False

    async def login(self, http_client: CloudflareScraper, initdata):
        try:
            await http_client.options(url=f'{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP')
            while True:
                json_data = {"query": initdata} if not self.start_param else \
                    {"query": initdata, "username": self.user_data.get('username'),
                     "referralToken": self.start_param.split('_')[1]}

                resp = await http_client.post(
                    f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
                if resp.status == 520:
                    logger.warning(self.log_message('Relogin'))
                    await asyncio.sleep(delay=3)
                    continue

                resp_json = await resp.json()

                if resp_json.get('token', {}).get('access'):
                    logger.info(self.log_message(f"Logged in successfully as {self.user_data.get('username')}"))
                    return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                elif "username is not available" in resp_json.get("message", "").lower():
                    while True:
                        name = self.user_data.get('username')
                        rand_letters = ''.join(choices(string.ascii_lowercase, k=randint(3, 8)))
                        new_name = name + rand_letters

                        json_data = {"query": initdata, "username": new_name,
                                     "referralToken": self.start_param.split('_')[1]}

                        resp = await http_client.post(
                            f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP",
                            json=json_data)
                        if resp.status == 520:
                            logger.warning(self.log_message('Relogin'))
                            await asyncio.sleep(delay=3)
                            continue
                        resp_json = await resp.json()

                        if resp_json.get("token"):
                            logger.success(self.log_message(
                                f'Registered using ref - {self.start_param} and nickname - {new_name}'))
                            return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                        elif resp_json.get("message") == 'account is already connected to another user':

                            json_data = {"query": initdata}
                            resp = await http_client.post(
                                f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
                            if resp.status == 520:
                                logger.warning((self.log_message('Relogin')))
                                await asyncio.sleep(delay=3)
                                continue
                            resp_json = await resp.json()
                            if not resp_json.get("token", {}).get("access") \
                                    or not resp_json.get("token", {}).get("refresh"):
                                continue
                            return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                        else:
                            logger.info(self.log_message('Username taken, retrying register with new name'))
                            await asyncio.sleep(1)

                elif 'account is already connected to another user' in resp_json.get("message", "").lower():

                    json_data = {"query": initdata}
                    resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                  "/PROVIDER_TELEGRAM_MINI_APP",
                                                  json=json_data)
                    if resp.status == 520:
                        logger.warning(self.log_message('Relogin'))
                        await asyncio.sleep(delay=3)
                        continue
                    resp_json = await resp.json()

                    return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                elif resp_json.get("token"):

                    logger.success(self.log_message(
                        f"Registered using ref - {self.start_param} and nickname - {self.user_data.get('username')}"))
                    return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

        except Exception as error:
            log_error(self.log_message(f"Login error {error}"))
            return None, None

    async def claim_task(self, http_client: CloudflareScraper, task_id):
        try:
            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/claim')
            resp_json = await resp.json()

            return resp_json.get('status') == "FINISHED"
        except Exception as error:
            log_error(self.log_message(f"Claim task error {error}"))

    async def start_task(self, http_client: CloudflareScraper, task_id):
        try:
            return await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/start')
        except Exception as error:
            log_error(self.log_message(f"Failed to start a task: {error}"))

    async def validate_task(self, http_client: CloudflareScraper, task_id):
        try:
            tasks = self.blum_data.get('tasks')

            keyword = [item["answer"] for item in tasks if item['id'] == task_id]

            payload = {'keyword': keyword[0]}

            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/validate', json=payload)
            resp.raise_for_status()
            resp_json = await resp.json()
            is_finished = False
            if resp_json.get('status') == "READY_FOR_CLAIM":
                is_finished = await self.claim_task(http_client, task_id)

            return is_finished

        except Exception as error:
            log_error(self.log_message(f"Claim task error {error}"))

    async def join_tribe(self, http_client: CloudflareScraper):
        if settings.JOIN_TRIBE:
            try:
                resp = await http_client.post(f'{self.tribe_url}/api/v1/tribe/{settings.JOIN_TRIBE}/join')
                text = await resp.text()
                if text == 'OK':
                    logger.success(self.log_message('Joined tribe'))
            except Exception as error:
                log_error(self.log_message(f"Join tribe {error}"))

    async def get_tasks(self, http_client: CloudflareScraper):
        try:
            while True:
                resp = await http_client.get(f'{self.earn_domain}/api/v1/tasks')
                if resp.status not in [200, 201]:
                    await asyncio.sleep(uniform(3, 5))
                    continue
                else:
                    break
            resp_json = await resp.json()

            collected_tasks = []

            for task_group in resp_json:
                if task_group.get('sectionType') == 'HIGHLIGHTS':
                    tasks_list = task_group.get('tasks', [])
                    for task in tasks_list:
                        sub_tasks = task.get('subTasks')
                        if sub_tasks:
                            for sub_task in sub_tasks:
                                collected_tasks.append(sub_task)
                        if task.get('type') != 'PARTNER_INTEGRATION':
                            collected_tasks.append(task)
                        if task.get('type') == 'PARTNER_INTEGRATION' and task.get('reward'):
                            collected_tasks.append(task)

                if task_group.get('sectionType') == 'WEEKLY_ROUTINE':
                    tasks_list = task_group.get('tasks', [])
                    for task in tasks_list:
                        sub_tasks = task.get('subTasks', [])
                        for sub_task in sub_tasks:
                            collected_tasks.append(sub_task)

                if task_group.get('sectionType') == "DEFAULT":
                    sub_tasks = task_group.get('subSections', [])
                    for sub_task in sub_tasks:
                        tasks = sub_task.get('tasks', [])
                        for task_basic in tasks:
                            collected_tasks.append(task_basic)

            return collected_tasks
        except Exception as error:
            log_error(self.log_message(f"Get tasks error {error}"))
            return []

    async def play_game(self, http_client: CloudflareScraper, play_passes):
        try:
            total_games = 0
            tries = 3
            max_games = randint(5, 20)
            data_elig = await self.elig_dogs(http_client=http_client)

            while play_passes:
                game_id = await self.start_game(http_client=http_client)

                if not game_id or game_id == "cannot start game":
                    logger.info(self.log_message(
                        f"Couldn't start play in game! play_passes: {play_passes}, trying again"))
                    tries -= 1
                    if tries == 0:
                        logger.warning(self.log_message('No more trying, gonna skip games'))
                        break
                    continue

                if total_games >= max_games:
                    logger.info(self.log_message(f"Played {total_games}. Enough for now"))
                    return

                total_games += 1
                logger.success(self.log_message("Started playing game"))

                await asyncio.sleep(uniform(30, 40))

                if data_elig:
                    dogs = randint(25, 30) * 5
                    msg, points = await self.claim_game(game_id=game_id, http_client=http_client, dogs=dogs)
                else:
                    msg, points = await self.claim_game(game_id=game_id, http_client=http_client, dogs=0)

                if isinstance(msg, bool) and msg:
                    logger.info(self.log_message(f"Finish play in game! reward: {points}"))
                else:
                    logger.info(self.log_message(f"Couldn't play game, msg: {msg} play_passes: {play_passes}"))
                    break

                await asyncio.sleep(uniform(2, 5))

                play_passes -= 1

        except Exception as e:
            log_error(self.log_message(f"Error occurred during play game: {e}"))

    async def start_game(self, http_client: CloudflareScraper):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v2/game/play")
            response_data = await resp.json()
            if "gameId" in response_data:
                return response_data.get("gameId")
            elif "message" in response_data:
                return response_data.get("message")
        except Exception as e:
            log_error(self.log_message(f"Error occurred during start game: {e}"))

    async def elig_dogs(self, http_client: CloudflareScraper):
        try:
            resp = await http_client.get(f'{self.game_url}/api/v2/game/eligibility/dogs_drop')
            if resp is not None:
                data = await resp.json()
                eligible = data.get('eligible', False)
                return eligible

        except Exception as e:
            log_error(self.log_message(f"Failed elif dogs, error: {e}"))
        return None

    async def get_data_payload(self):
        url = 'https://raw.githubusercontent.com/zuydd/database/main/blum.json'
        async with aiohttp.request(url=url, method="GET") as response:
            self.blum_data = json.loads(await response.text())

    async def create_payload(self, http_client: CloudflareScraper, game_id, points, dogs):
        payload_servers = self.blum_data.get('payloadServer', [])
        available_servers = [item for item in payload_servers if item['status'] == 1]
        for server in available_servers:
            resp = await http_client.post(f"https://{server['id']}.vercel.app/api/blum",
                                          json={'game_id': game_id, 'points': points, 'dogs': dogs})
            if resp.status in range(200, 300):
                data = await resp.json()
                if data.get("payload"):
                    return data.get("payload")
            logger.warning(self.log_message(f"Failed to create payload from server {server['id']}"))
        return None

    async def claim_game(self, game_id: str, dogs, http_client: CloudflareScraper):
        try:
            points = randint(settings.POINTS[0], settings.POINTS[1])

            data = await self.create_payload(http_client=http_client, game_id=game_id, points=points, dogs=dogs)

            if not data:
                return None

            resp = await http_client.post(f"{self.game_url}/api/v2/game/claim", json={'payload': data})
            if resp.status != 200:
                resp = await http_client.post(f"{self.game_url}/api/v2/game/claim", json={'payload': data})

            txt = await resp.text()

            return True if txt == 'OK' else txt, points
        except Exception as e:
            log_error(self.log_message(f"Error occurred during claim game: {e}"))

    async def claim(self, http_client: CloudflareScraper):
        try:
            while True:
                resp = await http_client.post(f"{self.game_url}/api/v1/farming/claim")
                if resp.status not in [200, 201]:
                    await asyncio.sleep(uniform(3, 5))
                    continue
                else:
                    break

            resp_json = await resp.json()

            return int(resp_json.get("timestamp") / 1000), resp_json.get("availableBalance")
        except Exception as e:
            log_error(self.log_message(f"Error occurred during claim: {e}"))

    async def start_farming(self, http_client: CloudflareScraper):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/farming/start")

            if resp.status != 200:
                resp = await http_client.post(f"{self.game_url}/api/v1/farming/start")
        except Exception as e:
            log_error(self.log_message(f"Error occurred during start: {e}"))

    async def friend_balance(self, http_client: CloudflareScraper):
        try:
            while True:
                resp = await http_client.get(f"{self.user_url}/api/v1/friends/balance")
                if resp.status not in [200, 201]:
                    await asyncio.sleep(uniform(0.2, 1))
                    continue
                else:
                    break

            resp_json = await resp.json()
            claim_amount = resp_json.get("amountForClaim")
            is_available = resp_json.get("canClaim")

            return claim_amount, is_available

        except Exception as e:
            log_error(self.log_message(f"Error occurred during friend balance: {e}"))
            return None, None

    async def friend_claim(self, http_client: CloudflareScraper):
        try:

            resp = await http_client.post(f"{self.user_url}/api/v1/friends/claim")
            resp_json = await resp.json()
            amount = resp_json.get("claimBalance")
            if resp.status != 200:
                resp = await http_client.post(f"{self.user_url}/api/v1/friends/claim")
                resp_json = await resp.json()
                amount = resp_json.get("claimBalance")

            return amount
        except Exception as e:
            log_error(self.log_message(f"Error occurred during friends claim: {e}"))

    async def balance(self, http_client: CloudflareScraper):
        try:
            resp = await http_client.get(f"{self.game_url}/api/v1/user/balance")
            resp_json = await resp.json()

            timestamp = resp_json.get("timestamp")
            play_passes = resp_json.get("playPasses")
            balance = int(float(resp_json.get('availableBalance')))

            start_time = None
            end_time = None
            if resp_json.get("farming"):
                start_time = resp_json["farming"].get("startTime")
                end_time = resp_json["farming"].get("endTime")

            await asyncio.sleep(uniform(1, 2))

            return (int(timestamp / 1000) if timestamp is not None else None,
                    int(start_time / 1000) if start_time is not None else None,
                    int(end_time / 1000) if end_time is not None else None,
                    play_passes, balance)
        except Exception as e:
            log_error(self.log_message(f"Error occurred during balance: {e}"))

    async def claim_daily_reward(self, http_client: CloudflareScraper):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/daily-reward?offset=-180")
            txt = await resp.text()
            await asyncio.sleep(uniform(1, 2))
            return True if txt == 'OK' else txt
        except Exception as e:
            log_error(self.log_message(f"Error occurred during claim daily reward: {e}"))

    async def refresh_token(self, http_client: CloudflareScraper, token):
        if "Authorization" in http_client.headers:
            del http_client.headers["Authorization"]
        json_data = {'refresh': token}
        resp = await http_client.post(f"{self.user_url}/api/v1/auth/refresh", json=json_data)
        resp_json = await resp.json()

        return resp_json.get('access'), resp_json.get('refresh')

    async def run(self) -> None:
        if settings.USE_RANDOM_DELAY_IN_RUN:
            random_delay = uniform(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
            logger.info(self.log_message(f"Bot will start in <ly>{int(random_delay)}s</ly>"))
            await asyncio.sleep(random_delay)

        access_token = None
        refresh_token = None
        login_need = True

        access_token_created_time = 0
        init_data = None

        proxy_conn = {'connector': ProxyConnector.from_url(self.proxy)} if self.proxy else {}
        async with CloudflareScraper(headers=self.headers, timeout=aiohttp.ClientTimeout(60), **proxy_conn) as http_client:
            while True:
                if not await self.check_proxy(http_client=http_client):
                    logger.warning(self.log_message('Failed to connect to proxy server. Sleep 5 minutes.'))
                    await asyncio.sleep(300)
                    continue

                token_live_time = randint(3500, 3600)
                try:
                    if time() - access_token_created_time >= token_live_time or not init_data:
                        init_data = await self.get_tg_web_data()

                        if not init_data:
                            logger.warning(self.log_message('Failed to get webview URL. Retrying in 5 minutes'))
                            await asyncio.sleep(300)
                            continue

                    access_token_created_time = time()

                    await self.get_data_payload()

                    if login_need:
                        if "Authorization" in http_client.headers:
                            del http_client.headers["Authorization"]

                        access_token, refresh_token = await self.login(http_client=http_client, initdata=init_data)

                        http_client.headers["Authorization"] = f"Bearer {access_token}"

                        logger.success(self.log_message("Logged in successfully"))

                        if self.tg_client.is_fist_run:
                            await first_run.append_recurring_session(self.session_name)

                        login_need = False

                    await self.balance(http_client=http_client)

                    msg = await self.claim_daily_reward(http_client=http_client)
                    if msg is True:
                        logger.success(self.log_message(f"Claimed daily reward!"))

                    timestamp, start_time, end_time, play_passes, balance = await self.balance(http_client=http_client)

                    if isinstance(play_passes, int):
                        logger.info(self.log_message(f'Balance: <lg>{balance}</lg> | Play passes: <lg>{play_passes}</lg>'))

                    claim_amount, is_available = await self.friend_balance(http_client=http_client)
                    if claim_amount != 0 and is_available:
                        amount = await self.friend_claim(http_client=http_client)
                        logger.success(self.log_message(f"Claimed friend ref reward {amount}"))

                    if play_passes and play_passes > 0 and settings.PLAY_GAMES:
                        await self.play_game(http_client=http_client, play_passes=play_passes)

                    await self.join_tribe(http_client=http_client)

                    if settings.PERFORM_TASKS:
                        tasks = await self.get_tasks(http_client=http_client)
                        err_count = 0
                        for task in tasks:
                            if task.get('status') == "NOT_STARTED" and task.get('type') != "PROGRESS_TARGET":
                                task_started = await self.start_task(http_client=http_client, task_id=task["id"])
                                if task_started.status in range(200, 300):
                                    logger.info(self.log_message(f"Started doing task - '{task['title']}'"))
                                else:
                                    err_count += 1
                                    if err_count > 3:
                                        logger.warning(self.log_message(
                                            f"Failed to start 3 tasks. Latest - '{task['title']}' Stop trying for now"))
                                        break
                                await asyncio.sleep(uniform(1, 5))

                    await asyncio.sleep(5)

                    tasks = await self.get_tasks(http_client=http_client)
                    for task in tasks:
                        if task.get('status'):
                            if task['status'] == "READY_FOR_CLAIM" and task['type'] != 'PROGRESS_TASK':
                                status = await self.claim_task(http_client=http_client, task_id=task["id"])
                                if status:
                                    logger.success(self.log_message(f"Claimed task - '{task['title']}'"))
                                await asyncio.sleep(uniform(1, 2))
                            elif task['status'] == "READY_FOR_VERIFY" and task['validationType'] == 'KEYWORD':
                                status = await self.validate_task(http_client=http_client, task_id=task["id"])

                                if status:
                                    logger.success(self.log_message(f"Validated task - '{task['title']}'"))

                    try:
                        timestamp, start_time, end_time, play_passes, balance = await self.balance(http_client=http_client)

                        if start_time and end_time and timestamp and timestamp >= end_time:
                            timestamp, balance = await self.claim(http_client=http_client)
                            logger.success(self.log_message(f"<lc>[FARMING]</lc> Claimed reward! Balance: {balance}"))
                            timestamp, start_time, end_time, play_passes, balanc = await self.balance(http_client=http_client)

                        if not start_time and not end_time:
                            await self.start_farming(http_client=http_client)
                            logger.info(self.log_message(f"<lc>[FARMING]</lc> Start farming!"))
                            await asyncio.sleep(uniform(3, 5))
                            timestamp, start_time, end_time, play_passes, balanc = await self.balance(http_client=http_client)

                        if end_time and timestamp and timestamp < end_time:
                            sleep_duration = (end_time - timestamp) * uniform(1.0, 1.1)
                            logger.info(self.log_message(f"<lc>[FARMING]</lc> Sleep {format_duration(sleep_duration)}"))
                            login_need = True
                            await asyncio.sleep(sleep_duration)

                    except Exception as e:
                        log_error(self.log_message(f"<lc>[FARMING]</lc> Error in farming management: {e}"))

                except InvalidSession:
                    raise

                except Exception as error:
                    sleep_duration = uniform(60, 120)
                    log_error(self.log_message(f"Unknown error: {error}. Sleeping for {int(sleep_duration)}"))
                    await asyncio.sleep(sleep_duration)


async def run_tapper(tg_client: UniversalTelegramClient):
    runner = Tapper(tg_client=tg_client)
    try:
        await runner.run()
    except InvalidSession as e:
        logger.error(runner.log_message(f"Invalid Session: {e}"))
