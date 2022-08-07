import json
from http import HTTPStatus
from typing import Optional, Union

import httpx

from core import config
from core.logger import logger
from service.api_client.base import AbstractAPIService
from service.api_client.models import (
    BillStat,
    MonthStat,
    UserActiveConsultations,
    UserData,
    UserExpiredConsultations,
    UserMonthStat,
    WeekStat,
)


class SiteAPIService(AbstractAPIService):
    """
    TODO: development after Frontend API creation
    """

    def __init__(self):
        self.site_url: str = config.SITE_API_URL
        self.bot_token: str = config.SITE_API_BOT_TOKEN

    async def get_bill(self) -> BillStat:
        ...

    async def get_week_stat(self) -> list[WeekStat]:
        return await self.__get_list_with_data(WeekStat, f"{self.site_url}/tgbot/stat/weekly")

    async def get_month_stat(self) -> list[MonthStat]:
        return await self.__get_list_with_data(MonthStat, f"{self.site_url}/tgbot/stat/monthly")

    async def get_user_active_consultations(self, telegram_id: int) -> Optional[UserActiveConsultations]:
        url = f"{self.site_url}/tgbot/stat/active/user/{telegram_id}"
        active_consultations = await self.__get_json_data(url=url)
        try:
            return UserActiveConsultations(**active_consultations)
        except TypeError as error:
            logger.error("Failed convert json to dataclass: %s", error)
            return None

    async def get_user_expired_consultations(self, telegram_id: int) -> Optional[UserExpiredConsultations]:
        url = f"{self.site_url}/tgbot/stat/overdue/user/{telegram_id}"
        exp_consultations = await self.__get_json_data(url=url)
        try:
            return UserExpiredConsultations(**exp_consultations)
        except TypeError as error:
            logger.error("Failed convert json to dataclass: %s", error)
            return None

    async def get_user_month_stat(self, telegram_id: int) -> Optional[UserMonthStat]:
        url = f"{self.site_url}/tgbot/stat/monthly/user/{telegram_id}"
        user_month_stat = await self.__get_json_data(url=url)
        try:
            return UserMonthStat(**user_month_stat)
        except TypeError as error:
            logger.error("Failed convert json to dataclass: %s", error)
            return None

    async def authenticate_user(self, telegram_id: int) -> Optional[UserData]:
        url = f"{self.site_url}/tgbot/user/{telegram_id}"
        user = await self.__get_json_data(url=url)
        try:
            return UserData(**user)
        except TypeError as error:
            logger.error("Failed convert json to dataclass: %s", error)
            return None

    async def set_user_timezone(self, telegram_id: int, user_time_zone: str) -> HTTPStatus:
        url = f"{self.site_url}/tgbot/user"
        headers = {"Authorization": self.bot_token}
        data = {"telegram_id": telegram_id, "time_zone": user_time_zone}
        async with httpx.AsyncClient() as client:
            response = await client.put(url=url, headers=headers, json=data)
            return response.status_code

    async def __get_json_data(self, url: str) -> Optional[dict]:
        headers = {"Authorization": self.bot_token}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=url, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as error:
                logger.error("Failed get data from server: %s", error)
            except json.JSONDecodeError as error:
                logger.error(
                    "Got a JSONDecodeError in responce decode - %s, url - %s, error - %s", response.text, url, error
                )
            return None

    async def __get_list_with_data(self, current_class: Union[WeekStat, MonthStat], url: str) -> Optional[list]:
        data = await self.__get_json_data(url=url)
        try:
            return [current_class.from_dict(stats) for stats in data]
        except TypeError as error:
            logger.error("Failed convert json to dataclass: %s, error: %s", current_class, error)
            return None
