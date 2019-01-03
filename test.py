# -*- coding: utf-8 -*-
import asyncio
url = "http://127.0.0.1:5000/router_map"
from aiohttp import ClientSession
import asyncio
import time
async def do_some_work(x):
    async with ClientSession() as session:
        time_ = time.time()
        async with session.get(url,headers={'sc_school':'31aee39323d5ee00043bcfa06b4479d1'}) as resp:
            # print(f"{x}==={resp}")
            await resp.text()
            print(f"{x}============{time.time() - time_}")
loop = asyncio.get_event_loop()
j=0
h=500
while True:
    tasks = []
    for i in range(h):
        tasks.append(asyncio.ensure_future(do_some_work(i+j*h)))
    loop.run_until_complete(asyncio.wait(tasks))
    j+=1
