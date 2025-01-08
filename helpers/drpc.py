import threading
import time
import asyncio
from pypresence import Presence, exceptions
import traceback
import requests
from helpers import logUtils as log

rpc = rpcStatus = ""
st = time.time()
def rcpConn():
    global rpc, rpcStatus; rpc = None
    log.chat("    Discord Is Not Running!")
    while not rpc:
        try:
            loop = asyncio.new_event_loop() #현재 스레드에 이벤트 루프를 생성하고 설정합니다.
            asyncio.set_event_loop(loop)
            rpc = Presence(1262205787036455022) #디스코드 애플리케이션의 클라이언트 ID
            rpc.connect()
            rpc.clear()
            #loop.run_forever() #이벤트 루프를 실행합니다.
            log.chat("    Connected To Discord!"); rpcStatus = "Discord Is Running"
            return rpc
        except exceptions.DiscordNotFound: rpcStatus = "Discord Is Not Running"
        except exceptions.DiscordError: rpcStatus = "Discord Is Not Running"
        except Exception as e: rpcStatus = e
        time.sleep(1)
def rpcUpdate(details = None, large_image = None, large_text = None):
    rpc.update(
        start=st,
        state="https://status.redstar.moe",
        details=details,
        large_image=large_image,
        large_text=large_text,
        small_image="https://b.redstar.moe/favicon.ico",
        small_text="https://b.redstar.moe/favicon.ico",
        buttons=[
            {"label": "Status", "url": f"https://status.redstar.moe"},
            {"label": "osu-media-server", "url": f"https://b.redstar.moe/status"}
        ]
    )
def DiscordRichPresence():
    rcpConn()
    while rpc:
        try:
            details = f"ns.aodd.xyz:53"
            rpcUpdate(details=details)
        except exceptions.InvalidID: rcpConn()
        except exceptions.ServerError: rpcUpdate(details="Error!")
        except Exception as e: rpcUpdate(details=e)
        time.sleep(1)

def drpcStart():
    DRP = threading.Thread(target=DiscordRichPresence)
    DRP.start()