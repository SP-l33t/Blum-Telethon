import subprocess
import json
from bot.utils import logger


async def create_payload_local(game_id: str, clover, freeze, dogs=0):
    command = ['node', './index.js', game_id, str(clover), str(freeze), str(dogs)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, cwd="./bot/utils/payload/")
        output = json.loads(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        logger.warning(f"Unknown error during local payload generation: {e.stderr}")
        output = None
    except FileNotFoundError:
        logger.warning("'Node.js' not found. Local payload generation is unavailable.")
        output = None
    return output
