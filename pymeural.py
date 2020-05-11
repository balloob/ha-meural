from functools import partial

from typing import Dict

import aiohttp
import async_timeout

BASE_URL = "https://api.meural.com/v0/"


async def authenticate(
    session: aiohttp.ClientSession, username: str, password: str
) -> str:
    """Authenticate and return a token."""
    with async_timeout.timeout(10):
        resp = await session.request(
            "post",
            BASE_URL + "authenticate",
            data={"username": username, "password": password},
            raise_for_status=True,
        )

    data = await resp.json()
    return data["token"]


class PyMeural:
    def __init__(self, token, session: aiohttp.ClientSession):
        self.token = token
        self.session = session

    async def request(self, method, path, data=None) -> Dict:
        url = f"{BASE_URL}{path}"
        kwargs = {}
        if data:
            if method == "get":
                data["query"] = data
            else:
                data["data"] = data
        with async_timeout.timeout(10):
            resp = await self.session.request(
                method,
                url,
                headers={
                    "Authorization": f"Token {self.token}",
                    "x-meural-api-version": "3",
                },
                raise_for_status=True,
                **kwargs,
            )

        response = await resp.json()
        from pprint import pprint

        pprint(response)
        return response["data"]

    async def get_user(self):
        return await self.request("get", "user")

    async def get_user_items(self):
        return await self.request("get", "user/items")

    async def get_user_galleries(self):
        return await self.request("get", "user/galleries")

    async def get_user_devices(self):
        return await self.request("get", "user/devices")

    async def get_user_feedback(self):
        return await self.request("get", "user/feedback")

    async def device_load_gallery(self, device_id, gallery_id):
        return await self.request("post", f"devices/{device_id}/galleries/{gallery_id}")

    async def get_device(self, device_id):
        return await self.request("get", f"devices/{device_id}")

    async def get_device_galleries(self, device_id):
        return await self.request("get", f"devices/{device_id}/galleries")

    async def update_device(self, device_id):
        return await self.request("put", f"devices/{device_id}")