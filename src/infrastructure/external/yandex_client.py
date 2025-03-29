from fastapi import HTTPException
from aiohttp import ClientSession

from config import Settings
from src.domain.value_objects import UserData


class YandexClient:

    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_user_data(self, code: str) -> UserData:
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.settings.CLIENT_ID,
            'client_secret': self.settings.CLIENT_SECRET,
        }
        async with ClientSession() as session:
            response = await session.post(
                url=self.settings.TOKEN_URL,
                data=data
            )
            if response.status != 200:
                raise HTTPException(status_code=400, detail='Failed to get access token')
            token_data = await response.json()
            token = token_data['access_token']
            user_info = await self.get_yandex_user(token)
            email = user_info['default_email']

            return UserData(email=email)

    async def get_yandex_user(self, token: str):
        async with ClientSession() as session:
            response = await session.get(
                url=self.settings.USER_INFO_URL,
                headers={"Authorization": f"OAuth {token}"}
            )
            if response.status != 200:
                raise HTTPException(status_code=400, detail='Failed to fetch user info')
            return await response.json()
