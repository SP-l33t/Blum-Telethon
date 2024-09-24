import aiohttp
import asyncio
import fasteners
import os
import random
import string
from urllib.parse import unquote
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from time import time

from telethon import TelegramClient
from telethon.errors import *
from telethon.types import InputUser, InputBotAppShortName, InputPeerUser
from telethon.functions import messages, contacts

from .agents import generate_random_user_agent
from .headers import *
from .helper import format_duration
from bot.config import settings
from bot.utils import logger, log_error, proxy_utils, config_utils, CONFIG_PATH, SESSIONS_PATH
from bot.exceptions import InvalidSession


class Tapper:
    def __init__(self, tg_client: TelegramClient):
        self.tg_client = tg_client
        self.session_name, _ = os.path.splitext(os.path.basename(tg_client.session.filename))
        self.config = config_utils.get_session_config(self.session_name, CONFIG_PATH)
        self.proxy = self.config.get('proxy', None)
        self.lock = fasteners.InterProcessLock(os.path.join(SESSIONS_PATH, f"{self.session_name}.lock"))
        self.user_id = 0
        self.username = None
        self.first_name = None
        self.last_name = None
        self.start_param = None
        self.first_run = None
        self.headers = headers
        self.headers['User-Agent'] = self.check_user_agent()
        self.headers.update(**get_sec_ch_ua(self.headers.get('User-Agent', '')))

        self.gateway_url = "https://gateway.blum.codes"
        self.game_url = "https://game-domain.blum.codes"
        self.wallet_url = "https://wallet-domain.blum.codes"
        self.subscription_url = "https://subscription.blum.codes"
        self.tribe_url = "https://tribe-domain.blum.codes"
        self.user_url = "https://user-domain.blum.codes"
        self.earn_domain = "https://earn-domain.blum.codes"

        self._webview_data = None

    def log_message(self, message) -> str:
        return f"<light-yellow>{self.session_name}</light-yellow> | {message}"

    def check_user_agent(self):
        user_agent = self.config.get('user_agent')
        if not user_agent:
            user_agent = generate_random_user_agent(device_type='android', browser_type='chrome')
            self.config['user_agent'] = user_agent
            config_utils.update_session_config_in_file(self.session_name, self.config, CONFIG_PATH)

        return user_agent

    async def get_tg_web_data(self) -> str:
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            proxy_dict = proxy_utils.to_telethon_proxy(proxy)
        else:
            proxy_dict = None
        self.tg_client.set_proxy(proxy_dict)

        tg_web_data = None
        with self.lock:
            async with self.tg_client as client:
                if not self._webview_data:
                    while True:
                        try:
                            resolve_result = await client(contacts.ResolveUsernameRequest(username='BlumCryptoBot'))
                            user = resolve_result.users[0]
                            peer = InputPeerUser(user_id=user.id, access_hash=user.access_hash)
                            input_user = InputUser(user_id=user.id, access_hash=user.access_hash)
                            input_bot_app = InputBotAppShortName(bot_id=input_user, short_name="app")
                            self._webview_data = {'peer': peer, 'app': input_bot_app}
                            break
                        except FloodWaitError as fl:
                            fls = fl.seconds

                            logger.warning(self.log_message(f"FloodWait {fl}"))
                            logger.info(self.log_message(f"Sleep {fls}s"))
                            await asyncio.sleep(fls + 3)

                self.start_param = settings.REF_ID if random.randint(0, 100) <= 85 else "ref_WyOWiiqWa4"

                web_view = await client(messages.RequestAppWebViewRequest(
                    **self._webview_data,
                    platform='android',
                    write_allowed=True,
                    start_param=self.start_param
                ))

                auth_url = web_view.url
                tg_web_data = unquote(
                    string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

                try:
                    if self.user_id == 0:
                        information = await client.get_me()
                        self.user_id = information.id
                        self.first_name = information.first_name or ''
                        self.last_name = information.last_name or ''
                        self.username = information.username or ''
                except Exception as e:
                    print(e)

        return tg_web_data

    async def login(self, http_client: aiohttp.ClientSession, initdata):
        try:
            await http_client.options(url=f'{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP')
            while True:
                json_data = {"query": initdata} if not settings.USE_REF else \
                    {"query": initdata, "username": self.username, "referralToken": self.start_param.split('_')[1]}

                resp = await http_client.post(
                    f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP",
                    json=json_data, ssl=False)
                if resp.status == 520:
                    logger.warning(self.log_message('Relogin'))
                    await asyncio.sleep(delay=3)
                    continue

                resp_json = await resp.json()

                if "Username is not available" in resp_json.get("message"):
                    while True:
                        name = self.username
                        rand_letters = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
                        new_name = name + rand_letters

                        json_data = {"query": initdata, "username": new_name,
                                     "referralToken": self.start_param.split('_')[1]}

                        resp = await http_client.post(
                            f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP",
                            json=json_data, ssl=False)
                        if resp.status == 520:
                            logger.warning(self.log_message('Relogin'))
                            await asyncio.sleep(delay=3)
                            continue
                        # self.debug(f'login text {await resp.text()}')
                        resp_json = await resp.json()

                        if resp_json.get("token"):
                            logger.success(self.log_message(
                                f'Registered using ref - {self.start_param} and nickname - {new_name}'))
                            return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                        elif resp_json.get("message") == 'account is already connected to another user':

                            json_data = {"query": initdata}
                            resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                          "/PROVIDER_TELEGRAM_MINI_APP",
                                                          json=json_data, ssl=False)
                            if resp.status == 520:
                                logger.warning((self.log_message('Relogin')))
                                await asyncio.sleep(delay=3)
                                continue
                            resp_json = await resp.json()
                            # logger.debug(self.log_message(f'login text {await resp.text()}'))
                            return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                        else:
                            logger.info(self.log_message('Username taken, retrying register with new name'))
                            await asyncio.sleep(1)

                elif resp_json.get("message") == 'account is already connected to another user':

                    json_data = {"query": initdata}
                    resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                  "/PROVIDER_TELEGRAM_MINI_APP",
                                                  json=json_data, ssl=False)
                    if resp.status == 520:
                        logger.warning(self.log_message('Relogin'))
                        await asyncio.sleep(delay=3)
                        continue
                    # self.debug(f'login text {await resp.text()}')
                    resp_json = await resp.json()

                    return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                elif resp_json.get("token"):

                    logger.success(self.log_message(
                        f'Registered using ref - {self.start_param} and nickname - {self.username}'))
                    return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

        except Exception as error:
            log_error(self.log_message(f"Login error {error}"))
            return None, None

    async def claim_task(self, http_client: aiohttp.ClientSession, task_id):
        try:
            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/claim',
                                          ssl=False)
            resp_json = await resp.json()

            return resp_json.get('status') == "FINISHED"
        except Exception as error:
            log_error(self.log_message(f"Claim task error {error}"))

    async def start_task(self, http_client: aiohttp.ClientSession, task_id):
        try:
            return await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/start', ssl=False)
        except Exception as error:
            log_error(self.log_message(f"Failed to start a task: {error}"))

    async def validate_task(self, http_client: aiohttp.ClientSession, task_id, title):
        try:
            keywords = {
                'How to Analyze Crypto?': 'VALUE',
                'Forks Explained': 'GO GET',
                'Secure your Crypto!': 'BEST PROJECT EVER',
                'Navigating Crypto': 'HEYBLUM',
                'What are Telegram Mini Apps?': 'CRYPTOBLUM',
                'Say No to Rug Pull!': 'SUPERBLUM'
            }

            payload = {'keyword': keywords.get(title)}

            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/validate',
                                          json=payload, ssl=False)
            resp_json = await resp.json()
            if resp_json.get('status') == "READY_FOR_CLAIM":
                status = await self.claim_task(http_client, task_id)
                if status:
                    return status
            else:
                return False

        except Exception as error:
            log_error(self.log_message(f"Claim task error {error}"))

    async def join_tribe(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f'{self.tribe_url}/api/v1/tribe/6361f86f-6a55-4b6b-b2bd-f73e79e09e38/join',
                                          ssl=False)
            text = await resp.text()
            if text == 'OK':
                logger.success(self.log_message('Joined tribe'))
        except Exception as error:
            log_error(self.log_message(f"Join tribe {error}"))

    async def get_tasks(self, http_client: aiohttp.ClientSession):
        try:
            while True:
                resp = await http_client.get(f'{self.earn_domain}/api/v1/tasks', ssl=False)
                if resp.status not in [200, 201]:
                    await asyncio.sleep(random.uniform(3, 5))
                    continue
                else:
                    break
            resp_json = await resp.json()

            def collect_tasks(resp_json):
                collected_tasks = []
                for task in resp_json:
                    if task.get('sectionType') == 'HIGHLIGHTS':
                        tasks_list = task.get('tasks', [])
                        for t in tasks_list:
                            sub_tasks = t.get('subTasks')
                            if sub_tasks:
                                for sub_task in sub_tasks:
                                    collected_tasks.append(sub_task)
                            if t.get('type') != 'PARTNER_INTEGRATION':
                                collected_tasks.append(t)

                    if task.get('sectionType') == 'WEEKLY_ROUTINE':
                        tasks_list = task.get('tasks', [])
                        for t in tasks_list:
                            sub_tasks = t.get('subTasks', [])
                            for sub_task in sub_tasks:
                                # print(sub_task)
                                collected_tasks.append(sub_task)

                    if task.get('sectionType') == "DEFAULT":
                        sub_tasks = task.get('subSections', [])
                        for sub_task in sub_tasks:
                            tasks = sub_task.get('tasks', [])
                            for task_basic in tasks:
                                collected_tasks.append(task_basic)

                return collected_tasks

            all_tasks = collect_tasks(resp_json)

            # logger.debug(f"{self.session_name} | Collected {len(all_tasks)} tasks")

            return all_tasks
        except Exception as error:
            log_error(self.log_message(f"Get tasks error {error}"))
            return []

    async def play_game(self, http_client: aiohttp.ClientSession, play_passes, refresh_token):
        try:
            total_games = 0
            tries = 3
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
                else:
                    if total_games != 25:
                        total_games += 1
                        logger.success(self.log_message("Started playing game"))
                    else:
                        logger.info(self.log_message("Getting new token to play games"))
                        while True:
                            (access_token,
                             refresh_token) = await self.refresh_token(http_client=http_client, token=refresh_token)
                            if access_token:
                                http_client.headers["Authorization"] = f"Bearer {access_token}"
                                logger.success(self.log_message('Got new token'))
                                total_games = 0
                                break
                            else:
                                log_error(self.log_message('Can`t get new token, trying again'))
                                continue

                await asyncio.sleep(random.uniform(30, 40))

                msg, points = await self.claim_game(game_id=game_id, http_client=http_client)
                if isinstance(msg, bool) and msg:
                    logger.info(self.log_message(f"Finish play in game! reward: {points}"))
                else:
                    logger.info(self.log_message(f"Couldn't play game, msg: {msg} play_passes: {play_passes}"))
                    break

                await asyncio.sleep(random.uniform(1, 5))

                play_passes -= 1
        except Exception as e:
            log_error(self.log_message(f"Error occurred during play game: {e}"))

    async def start_game(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/game/play", ssl=False)
            response_data = await resp.json()
            if "gameId" in response_data:
                return response_data.get("gameId")
            elif "message" in response_data:
                return response_data.get("message")
        except Exception as e:
            log_error(self.log_message(f"Error occurred during start game: {e}"))

    async def claim_game(self, game_id: str, http_client: aiohttp.ClientSession):
        try:
            points = random.randint(settings.POINTS[0], settings.POINTS[1])
            json_data = {"gameId": game_id, "points": points}

            resp = await http_client.post(f"{self.game_url}/api/v1/game/claim", json=json_data,
                                          ssl=False)
            if resp.status != 200:
                resp = await http_client.post(f"{self.game_url}/api/v1/game/claim", json=json_data,
                                              ssl=False)

            txt = await resp.text()

            return True if txt == 'OK' else txt, points
        except Exception as e:
            log_error(self.log_message(f"Error occurred during claim game: {e}"))

    async def claim(self, http_client: aiohttp.ClientSession):
        try:
            while True:
                resp = await http_client.post(f"{self.game_url}/api/v1/farming/claim", ssl=False)
                if resp.status not in [200, 201]:
                    await asyncio.sleep(random.uniform(3, 5))
                    continue
                else:
                    break

            resp_json = await resp.json()

            return int(resp_json.get("timestamp") / 1000), resp_json.get("availableBalance")
        except Exception as e:
            log_error(self.log_message(f"Error occurred during claim: {e}"))

    async def start_farming(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/farming/start", ssl=False)

            if resp.status != 200:
                resp = await http_client.post(f"{self.game_url}/api/v1/farming/start", ssl=False)
        except Exception as e:
            log_error(self.log_message(f"Error occurred during start: {e}"))

    async def friend_balance(self, http_client: aiohttp.ClientSession):
        try:
            while True:
                resp = await http_client.get(f"{self.user_url}/api/v1/friends/balance", ssl=False)
                if resp.status not in [200, 201]:
                    await asyncio.sleep(random.uniform(0.2, 1))
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

    async def friend_claim(self, http_client: aiohttp.ClientSession):
        try:

            resp = await http_client.post(f"{self.user_url}/api/v1/friends/claim", ssl=False)
            resp_json = await resp.json()
            amount = resp_json.get("claimBalance")
            if resp.status != 200:
                resp = await http_client.post(f"{self.user_url}/api/v1/friends/claim", ssl=False)
                resp_json = await resp.json()
                amount = resp_json.get("claimBalance")

            return amount
        except Exception as e:
            log_error(self.log_message(f"Error occurred during friends claim: {e}"))

    async def balance(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.get(f"{self.game_url}/api/v1/user/balance", ssl=False)
            resp_json = await resp.json()

            timestamp = resp_json.get("timestamp")
            play_passes = resp_json.get("playPasses")

            start_time = None
            end_time = None
            if resp_json.get("farming"):
                start_time = resp_json["farming"].get("startTime")
                end_time = resp_json["farming"].get("endTime")

            return (int(timestamp / 1000) if timestamp is not None else None,
                    int(start_time / 1000) if start_time is not None else None,
                    int(end_time / 1000) if end_time is not None else None,
                    play_passes)
        except Exception as e:
            log_error(self.log_message(f"Error occurred during balance: {e}"))

    async def claim_daily_reward(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/daily-reward?offset=-180",
                                          ssl=False)
            txt = await resp.text()
            return True if txt == 'OK' else txt
        except Exception as e:
            log_error(self.log_message(f"Error occurred during claim daily reward: {e}"))

    async def refresh_token(self, http_client: aiohttp.ClientSession, token):
        if "Authorization" in http_client.headers:
            del http_client.headers["Authorization"]
        json_data = {'refresh': token}
        resp = await http_client.post(f"{self.user_url}/api/v1/auth/refresh", json=json_data, ssl=False)
        resp_json = await resp.json()

        return resp_json.get('access'), resp_json.get('refresh')

    async def check_proxy(self, http_client: aiohttp.ClientSession) -> bool:
        proxy_conn = http_client._connector
        try:
            response = await http_client.get(url='https://ifconfig.me/ip', timeout=aiohttp.ClientTimeout(15))
            logger.info(self.log_message(f"Proxy IP: {await response.text()}"))
            return True
        except Exception as error:
            proxy_url = f"{proxy_conn._proxy_type}://{proxy_conn._proxy_host}:{proxy_conn._proxy_port}"
            log_error(self.log_message(f"Proxy: {proxy_url} | Error: {type(error).__name__}"))
            return False

    async def run(self) -> None:
        if settings.USE_RANDOM_DELAY_IN_RUN:
            random_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
            logger.info(self.log_message(f"Bot will start in <ly>{random_delay}s</ly>"))
            await asyncio.sleep(random_delay)

        access_token = None
        refresh_token = None
        login_need = True

        access_token_created_time = 0
        token_live_time = 3600
        init_data = None

        while True:
            proxy_conn = {'connector': ProxyConnector.from_url(self.proxy)} if self.proxy else {}
            async with CloudflareScraper(headers=self.headers, timeout=aiohttp.ClientTimeout(60), **proxy_conn) as http_client:
                if not await self.check_proxy(http_client=http_client):
                    logger.warning(self.log_message('Failed to connect to proxy server. Sleep 5 minutes.'))
                    await asyncio.sleep(300)
                    continue

                try:
                    if time() - access_token_created_time >= token_live_time:
                        init_data = await self.get_tg_web_data()

                        if not init_data:
                            raise InvalidSession('Failed to get webview URL')

                    access_token_created_time = time()

                    if login_need:
                        if "Authorization" in http_client.headers:
                            del http_client.headers["Authorization"]

                        access_token, refresh_token = await self.login(http_client=http_client, initdata=init_data)

                        http_client.headers["Authorization"] = f"Bearer {access_token}"

                        if self.first_run is not True:
                            logger.success(self.log_message("Logged in successfully"))
                            self.first_run = True

                        login_need = False

                    timestamp, start_time, end_time, play_passes = await self.balance(http_client=http_client)

                    if isinstance(play_passes, int):
                        logger.info(self.log_message(f'You have {play_passes} play passes'))

                    msg = await self.claim_daily_reward(http_client=http_client)
                    if isinstance(msg, bool) and msg:
                        logger.success(self.log_message(f"Claimed daily reward!"))

                    claim_amount, is_available = await self.friend_balance(http_client=http_client)
                    if claim_amount != 0 and is_available:
                        amount = await self.friend_claim(http_client=http_client)
                        logger.success(self.log_message(f"Claimed friend ref reward {amount}"))

                    if play_passes and play_passes > 0 and settings.PLAY_GAMES:
                        await self.play_game(http_client=http_client, play_passes=play_passes, refresh_token=refresh_token)

                    await self.join_tribe(http_client=http_client)
                    tasks = await self.get_tasks(http_client=http_client)

                    for task in tasks:
                        if task.get('status') == "NOT_STARTED" and task.get('type') != "PROGRESS_TARGET":
                            task_started = await self.start_task(http_client=http_client, task_id=task["id"])
                            if task_started.status < 400:
                                logger.info(self.log_message(f"Started doing task - '{task['title']}'"))
                            else:
                                logger.warning(self.log_message(f"Failed to start task - '{task['title']}' Stop trying for now"))
                                break
                            await asyncio.sleep(random.uniform(1, 5))

                    await asyncio.sleep(5)

                    tasks = await self.get_tasks(http_client=http_client)
                    for task in tasks:
                        if task.get('status'):
                            if task['status'] == "READY_FOR_CLAIM" and task['type'] != 'PROGRESS_TASK':
                                status = await self.claim_task(http_client=http_client, task_id=task["id"])
                                if status:
                                    logger.success(self.log_message(f"Claimed task - '{task['title']}'"))
                                await asyncio.sleep(random.uniform(1, 2))
                            elif task['status'] == "READY_FOR_VERIFY" and task['validationType'] == 'KEYWORD':
                                status = await self.validate_task(http_client=http_client, task_id=task["id"],
                                                                  title=task['title'])

                                if status:
                                    logger.success(self.log_message(f"Validated task - '{task['title']}'"))

                    try:
                        timestamp, start_time, end_time, play_passes = await self.balance(http_client=http_client)

                        if start_time is None and end_time is None:
                            await self.start_farming(http_client=http_client)
                            logger.info(self.log_message(f"<lc>[FARMING]</lc> Start farming!"))

                        elif (start_time is not None and end_time is not None and timestamp is not None and
                              timestamp >= end_time):
                            timestamp, balance = await self.claim(http_client=http_client)
                            logger.success(self.log_message(f"<lc>[FARMING]</lc> Claimed reward! Balance: {balance}"))

                        elif end_time is not None and timestamp is not None:
                            sleep_duration = (end_time - timestamp) * random.uniform(1.0, 1.1)
                            logger.info(self.log_message(f"<lc>[FARMING]</lc> Sleep {format_duration(sleep_duration)}"))
                            login_need = True
                            await asyncio.sleep(sleep_duration)

                    except Exception as e:
                        log_error(self.log_message(f"<lc>[FARMING]</lc> Error in farming management: {e}"))

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    log_error(self.log_message(f"Unknown error: {error}"))
                    await asyncio.sleep(delay=3)


async def run_tapper(tg_client: TelegramClient):
    runner = Tapper(tg_client=tg_client)
    try:
        await runner.run()
    except InvalidSession as e:
        logger.error(runner.log_message(f"Invalid Session: {e}"))
    finally:
        if runner.lock.acquired:
            runner.lock.release()
