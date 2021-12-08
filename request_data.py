import asyncio

import requests


async def getUserData():
    users = requests.get('http://127.0.0.1:8083/rest/user/get')
    print(users.json())




async def main():
    asyncio.create_task(getUserData())

asyncio.run(main())