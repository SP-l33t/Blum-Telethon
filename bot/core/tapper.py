import aiohttp
import asyncio
import os
import random
import string
from urllib.parse import unquote
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy

from telethon import TelegramClient
from telethon.errors import *
from telethon.types import InputUser, InputBotAppShortName, InputPeerUser
from telethon.functions import messages, contacts

from .agents import generate_random_user_agent
from .headers import *
from .helper import format_duration
from bot.config import settings
from bot.utils import logger, proxy_utils, config_utils
from bot.exceptions import InvalidSession


class Tapper:
    def __init__(self, tg_client: TelegramClient):

        self.session_name, _ = os.path.splitext(os.path.basename(tg_client.session.filename))
        self.config = config_utils.get_session_config(self.session_name)
        self.proxy = self.config.get('proxy', None)
        self.tg_client = tg_client
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

    @staticmethod
    async def generate_random_user_agent():
        return generate_random_user_agent(device_type='android', browser_type='chrome')

    def info(self, message):
        from bot.utils import info
        info(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def debug(self, message):
        from bot.utils import debug
        debug(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def warning(self, message):
        from bot.utils import warning
        warning(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def error(self, message):
        from bot.utils import error
        error(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def critical(self, message):
        from bot.utils import critical
        critical(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def success(self, message):
        from bot.utils import success
        success(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def check_user_agent(self):
        user_agent = self.config.get('user_agent')
        if not user_agent:
            user_agent = generate_random_user_agent()
            self.config['user_agent'] = user_agent
            config_utils.update_config_file(self.session_name, self.config)

        return user_agent

    async def get_tg_web_data(self) -> str:
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            proxy_dict = proxy_utils.to_telethon_proxy(proxy)
        else:
            proxy_dict = None

        self.tg_client.set_proxy(proxy_dict)
        try:
            if not self.tg_client.is_connected():
                try:
                    await self.tg_client.start()
                except (UnauthorizedError, AuthKeyUnregisteredError):
                    raise InvalidSession(self.session_name)
                except (UserDeactivatedError, UserDeactivatedBanError, PhoneNumberBannedError):
                    raise InvalidSession(f"{self.session_name}: User is banned")
            self.start_param = settings.REF_ID if random.randint(0, 100) <= 85 else "ref_WyOWiiqWa4"
            while True:
                try:
                    resolve_result = await self.tg_client(contacts.ResolveUsernameRequest(username='BlumCryptoBot'))
                    peer = InputPeerUser(user_id=resolve_result.peer.user_id, access_hash=resolve_result.users[0].access_hash)
                    break
                except FloodWaitError as fl:
                    fls = fl.seconds

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    logger.info(f"{self.session_name} | Sleep {fls}s")
                    await asyncio.sleep(fls + 3)

            input_user = InputUser(user_id=resolve_result.peer.user_id, access_hash=resolve_result.users[0].access_hash)
            input_bot_app = InputBotAppShortName(bot_id=input_user, short_name="app")

            web_view = await self.tg_client(messages.RequestAppWebViewRequest(
                peer=peer,
                app=input_bot_app,
                platform='android',
                write_allowed=True,
                start_param=self.start_param
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

            try:
                if self.user_id == 0:
                    information = await self.tg_client.get_me()
                    self.user_id = information.id
                    self.first_name = information.first_name or ''
                    self.last_name = information.last_name or ''
                    self.username = information.username or ''
            except Exception as e:
                print(e)

            if self.tg_client.is_connected():
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            self.error(f"Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: aiohttp.ClientSession, initdata):
        try:
            await http_client.options(url=f'{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP')
            while True:
                if settings.USE_REF is False:

                    json_data = {"query": initdata}
                    resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                  "/PROVIDER_TELEGRAM_MINI_APP",
                                                  json=json_data, ssl=False)
                    if resp.status == 520:
                        self.warning('Relogin')
                        await asyncio.sleep(delay=3)
                        continue
                    # self.debug(f'login text {await resp.text()}')
                    resp_json = await resp.json()

                    return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                else:

                    json_data = {"query": initdata, "username": self.username,
                                 "referralToken": self.start_param.split('_')[1]}

                    resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                  "/PROVIDER_TELEGRAM_MINI_APP",
                                                  json=json_data, ssl=False)
                    if resp.status == 520:
                        self.warning('Relogin')
                        await asyncio.sleep(delay=3)
                        continue
                    # self.debug(f'login text {await resp.text()}')
                    resp_json = await resp.json()

                    if resp_json.get("message") == "rpc error: code = AlreadyExists desc = Username is not available":
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
                                self.warning('Relogin')
                                await asyncio.sleep(delay=3)
                                continue
                            # self.debug(f'login text {await resp.text()}')
                            resp_json = await resp.json()

                            if resp_json.get("token"):
                                self.success(f'Registered using ref - {self.start_param} and nickname - {new_name}')
                                return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                            elif resp_json.get("message") == 'account is already connected to another user':

                                json_data = {"query": initdata}
                                resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                              "/PROVIDER_TELEGRAM_MINI_APP",
                                                              json=json_data, ssl=False)
                                if resp.status == 520:
                                    self.warning('Relogin')
                                    await asyncio.sleep(delay=3)
                                    continue
                                resp_json = await resp.json()
                                # self.debug(f'login text {await resp.text()}')
                                return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                            else:
                                self.info(f'Username taken, retrying register with new name')
                                await asyncio.sleep(1)

                    elif resp_json.get("message") == 'account is already connected to another user':

                        json_data = {"query": initdata}
                        resp = await http_client.post(f"{self.user_url}/api/v1/auth/provider"
                                                      "/PROVIDER_TELEGRAM_MINI_APP",
                                                      json=json_data, ssl=False)
                        if resp.status == 520:
                            self.warning('Relogin')
                            await asyncio.sleep(delay=3)
                            continue
                        # self.debug(f'login text {await resp.text()}')
                        resp_json = await resp.json()

                        return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

                    elif resp_json.get("token"):

                        self.success(f'Registered using ref - {self.start_param} and nickname - {self.username}')
                        return resp_json.get("token").get("access"), resp_json.get("token").get("refresh")

        except Exception as error:
            self.error(f"Login error {error}")
            return None, None

    async def claim_task(self, http_client: aiohttp.ClientSession, task_id):
        try:
            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/claim',
                                          ssl=False)
            resp_json = await resp.json()

            return resp_json.get('status') == "FINISHED"
        except Exception as error:
            self.error(f"Claim task error {error}")

    async def start_task(self, http_client: aiohttp.ClientSession, task_id):
        try:
            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/start',
                                          ssl=False)

        except Exception as error:
            self.error(f" Start complete error {error}")

    async def validate_task(self, http_client: aiohttp.ClientSession, task_id, title):
        try:
            keywords = {
                'How to Analyze Crypto?': 'VALUE'
            }

            payload = {'keyword': keywords.get(title)}

            resp = await http_client.post(f'{self.earn_domain}/api/v1/tasks/{task_id}/validate',
                                          json=payload, ssl=False)
            resp_json = await resp.json()
            if resp_json.get('status') == "READY_FOR_CLAIM":
                self.success(f'Validated task - {title}')
                status = await self.claim_task(http_client, task_id)
                if status:
                    return status
            else:
                return False

        except Exception as error:
            self.error(f"Claim task error {error}")

    async def join_tribe(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f'{self.tribe_url}/api/v1/tribe/510c4987-ff99-4bd4-9e74-29ba9bce8220/join',
                                          ssl=False)
            text = await resp.text()
            if text == 'OK':
                self.success(f'Joined tribe')
        except Exception as error:
            self.error(f"Join tribe {error}")

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

            # self.debug(f"get_tasks response: {resp_json}")
            tasks = [element for sublist in resp_json for element in sublist.get("subSections")]

            if isinstance(resp_json, list):
                return tasks
            else:
                self.error(f"Unexpected response format in get_tasks: {resp_json}")
                return []
        except Exception as error:
            self.error(f"Get tasks error {error}")

    async def play_game(self, http_client: aiohttp.ClientSession, play_passes, refresh_token):
        try:
            total_games = 0
            tries = 3
            while play_passes:
                game_id = await self.start_game(http_client=http_client)

                if not game_id or game_id == "cannot start game":
                    self.info(f"Couldn't start play in game! play_passes: {play_passes}, trying again")
                    tries -= 1
                    if tries == 0:
                        self.warning('No more trying, gonna skip games')
                        break
                    continue
                else:
                    if total_games != 25:
                        total_games += 1
                        self.success("Started playing game")
                    else:
                        self.info("Getting new token to play games")
                        while True:
                            (access_token,
                             refresh_token) = await self.refresh_token(http_client=http_client, token=refresh_token)
                            if access_token:
                                http_client.headers["Authorization"] = f"Bearer {access_token}"
                                self.success('Got new token')
                                total_games = 0
                                break
                            else:
                                self.error('Can`t get new token, trying again')
                                continue

                await asyncio.sleep(random.uniform(30, 40))

                msg, points = await self.claim_game(game_id=game_id, http_client=http_client)
                if isinstance(msg, bool) and msg:
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Finish play in game!"
                                f" reward: {points}")
                else:
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Couldn't play game,"
                                f" msg: {msg} play_passes: {play_passes}")
                    break

                await asyncio.sleep(random.uniform(1, 5))

                play_passes -= 1
        except Exception as e:
            self.error(f"Error occurred during play game: {e}")

    async def start_game(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/game/play", ssl=False)
            response_data = await resp.json()
            if "gameId" in response_data:
                return response_data.get("gameId")
            elif "message" in response_data:
                return response_data.get("message")
        except Exception as e:
            self.error(f"Error occurred during start game: {e}")

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
            self.error(f"Error occurred during claim game: {e}")

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
            self.error(f"Error occurred during claim: {e}")

    async def start_farming(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/farming/start", ssl=False)

            if resp.status != 200:
                resp = await http_client.post(f"{self.game_url}/api/v1/farming/start", ssl=False)
        except Exception as e:
            self.error(f"Error occurred during start: {e}")

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
            self.error(f"Error occurred during friend balance: {e}")
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
            self.error(f"Error occurred during friends claim: {e}")

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
            self.error(f"Error occurred during balance: {e}")

    async def claim_daily_reward(self, http_client: aiohttp.ClientSession):
        try:
            resp = await http_client.post(f"{self.game_url}/api/v1/daily-reward?offset=-180",
                                          ssl=False)
            txt = await resp.text()
            return True if txt == 'OK' else txt
        except Exception as e:
            self.error(f"Error occurred during claim daily reward: {e}")

    async def refresh_token(self, http_client: aiohttp.ClientSession, token):
        if "Authorization" in http_client.headers:
            del http_client.headers["Authorization"]
        json_data = {'refresh': token}
        resp = await http_client.post(f"{self.user_url}/api/v1/auth/refresh", json=json_data, ssl=False)
        resp_json = await resp.json()

        return resp_json.get('access'), resp_json.get('refresh')

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: str) -> bool:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            self.info(f"Proxy IP: {ip}")
            return True
        except Exception as error:
            self.error(f"Proxy: {proxy} | Error: {error}")
            return False

    async def run(self) -> None:
        access_token = None
        refresh_token = None
        login_need = True

        if self.proxy:
            proxy_conn = ProxyConnector().from_url(self.proxy)
            http_client = CloudflareScraper(headers=self.headers, connector=proxy_conn)
            p_type = proxy_conn._proxy_type
            p_host = proxy_conn._proxy_host
            p_port = proxy_conn._proxy_port
            if not await self.check_proxy(http_client=http_client, proxy=f"{p_type}://{p_host}:{p_port}"):
                return
        else:
            http_client = CloudflareScraper(headers=self.headers)

        # print(init_data)

        while True:
            try:
                if login_need:
                    if "Authorization" in http_client.headers:
                        del http_client.headers["Authorization"]

                    init_data = await self.get_tg_web_data()

                    access_token, refresh_token = await self.login(http_client=http_client, initdata=init_data)

                    http_client.headers["Authorization"] = f"Bearer {access_token}"

                    if self.first_run is not True:
                        self.success("Logged in successfully")
                        self.first_run = True

                    login_need = False

                msg = await self.claim_daily_reward(http_client=http_client)
                if isinstance(msg, bool) and msg:
                    self.success(f"Claimed daily reward!")

                timestamp, start_time, end_time, play_passes = await self.balance(http_client=http_client)
                if isinstance(play_passes, int):
                    self.info(f'You have {play_passes} play passes')

                claim_amount, is_available = await self.friend_balance(http_client=http_client)
                if claim_amount != 0 and is_available:
                    amount = await self.friend_claim(http_client=http_client)
                    self.success(f"Claimed friend ref reward {amount}")

                if play_passes and play_passes > 0 and settings.PLAY_GAMES:
                    await self.play_game(http_client=http_client, play_passes=play_passes, refresh_token=refresh_token)

                # await self.join_tribe(http_client=http_client)
                tasks = await self.get_tasks(http_client=http_client)
                for section in tasks:
                    for task in section['tasks']:
                        if task.get('status') == "NOT_STARTED" and task.get('type') != "PROGRESS_TARGET":
                            await self.start_task(http_client=http_client, task_id=task["id"])
                            await asyncio.sleep(random.uniform(3, 5))

                tasks = await self.get_tasks(http_client=http_client)
                for section in tasks:
                    for task in section['tasks']:
                        if task.get('status'):
                            if task['status'] == "READY_FOR_CLAIM":
                                status = await self.claim_task(http_client=http_client, task_id=task["id"])
                                if status:
                                    self.success(f"Claimed task - '{task['title']}'")
                                await asyncio.sleep(random.uniform(3, 5))
                            elif task['status'] == "READY_FOR_VERIFY" and task['validationType'] == 'KEYWORD':
                                status = await self.validate_task(http_client=http_client, task_id=task["id"],
                                                                  title=task['title'])

                                if status:
                                    self.success(f"Claimed task - '{task['title']}'")

                # await asyncio.sleep(random.uniform(1, 3))

                try:
                    timestamp, start_time, end_time, play_passes = await self.balance(http_client=http_client)

                    if start_time is None and end_time is None:
                        await self.start_farming(http_client=http_client)
                        self.info(f"<lc>[FARMING]</lc> Start farming!")

                    elif (start_time is not None and end_time is not None and timestamp is not None and
                          timestamp >= end_time):
                        timestamp, balance = await self.claim(http_client=http_client)
                        self.success(f"<lc>[FARMING]</lc> Claimed reward! Balance: {balance}")

                    elif end_time is not None and timestamp is not None:
                        sleep_duration = end_time - timestamp
                        self.info(f"<lc>[FARMING]</lc> Sleep {format_duration(sleep_duration)}")
                        login_need = True
                        await asyncio.sleep(sleep_duration)

                except Exception as e:
                    self.error(f"<lc>[FARMING]</lc> Error in farming management: {e}")

            except InvalidSession as error:
                raise error

            except Exception as error:
                self.error(f"Unknown error: {error}")
                await asyncio.sleep(delay=3)


async def run_tapper(tg_client: TelegramClient):
    try:
        await Tapper(tg_client=tg_client).run()
    except InvalidSession:
        session_name, _ = os.path.splitext(os.path.basename(tg_client.session.filename))
        logger.error(f"<light-yellow>{session_name}</light-yellow> | Invalid Session")
