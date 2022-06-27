from http import HTTPStatus

import httpx

from service.api_client.base import AbstractAPIService
from service.api_client.models import BillStat, MonthStat, MyMonthStat, MyWeekStat, UserData, WeekStat


class ShemasAPIService(AbstractAPIService):
    async def get_bill(self) -> BillStat:
        url = f"{self.site_url}tgbot/bill"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
            return BillStat(response["telegram_id"])

    async def get_week_stat(self) -> WeekStat:
        url = f"{self.site_url}tgbot/stat/weekly"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
            return WeekStat(response["week_stat"])

    async def get_month_stat(self) -> MonthStat:
        url = f"{self.site_url}tgbot/stat/monthly"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
            return MonthStat(response["month_stat"])

    async def get_my_week_stat(self, telegram_id: int) -> MyWeekStat:
        url = f"{self.site_url}/tgbot/stat/weekly/user/{telegram_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
            return MyWeekStat(response["week_stat"])

    async def get_my_month_stat(self, telegram_id: int) -> MyMonthStat:
        url = f"{self.site_url}/tgbot/stat/monthly/user/{telegram_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
            return MyWeekStat(response["month_stat"])

    async def authenticate_user(self, telegram_id: int) -> UserData | None:  # если неавторизированный пользователь:
        url = f"{self.site_url}tgbot/auth"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={"telegram_id": telegram_id})
            response = response.json()
            return UserData(response["username"], response["user_time_zone"], response["user_id_in_trello"])

    async def set_user_timezone(self, telegram_id: int, user_timezone: str) -> HTTPStatus:
        url = f"{self.site_url}tgbot/user"
        async with httpx.AsyncClient() as client:
            response = await client.put(url, data={"telegram_id": telegram_id, "user_timezine": user_timezone})
            return response.status_code == HTTPStatus.OK
