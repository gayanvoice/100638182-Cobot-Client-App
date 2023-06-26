import asyncio

from cloud import cobot
from cloud.cobot import Cobot

if __name__ == '__main__':
    cobot_model_id = "dtmi:com:example:Cobot;1"
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = "0ne00A685D0"
    registration_id = "Cobot"
    symmetric_key = "GQXiRV7rtQVOFCKZuSnHfj85arpbeQqAyhbov8zk7vNbaG/4mcXa06ETfH+C1Mr/IGPOCDawrqmfCR6lG0IyKA=="

    cobot = Cobot(cobot_model_id, provisioning_host, id_scope, registration_id, symmetric_key)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(cobot.connect_azure_iot())
    loop.close()
