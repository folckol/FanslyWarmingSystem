import asyncio
import datetime
import os
import random
import string
import threading
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5
from pprint import pprint

import requests
from sqlalchemy import select, and_
import time

from FanslyModel import FanslyModel
from Utils.logger import logger

from DB import *

def generate_random_number(length: int) -> int:
    return int(''.join([random.choice(string.digits) for _ in range(length)]))

def generate_csrf_token() -> str:
    random_int: int = generate_random_number(length=3)
    current_timestamp: int = int(str(int(time.time())) + str(random_int))
    random_csrf_token = md5(string=f'{current_timestamp}:{current_timestamp},{0}:{0}'.encode()).hexdigest()

    return random_csrf_token

names = [
    "Liam", "Noah", "Oliver", "Ethan", "Aiden", "Lucas", "Jackson", "Elijah", "Benjamin", "James",
    "Mason", "Carter", "Michael", "Alexander", "Sebastian", "Daniel", "William", "Matthew", "Joseph", "Samuel",
    "David", "John", "Logan", "Ryan", "Andrew", "Christopher", "Nicholas", "Robert", "Henry", "Jacob",
    "Isaac", "Anthony", "Dylan", "Luke", "Nathan", "Wyatt", "Owen", "Caleb", "Connor", "Gabriel",
    "Christian", "Isaiah", "Zachary", "Joshua", "Brandon", "Jordan", "Julian", "Adrian", "Tyler", "Angel",
    "Sophia", "Olivia", "Emma", "Ava", "Isabella", "Mia", "Abigail", "Emily", "Amelia", "Elizabeth",
    "Avery", "Sofia", "Ella", "Scarlett", "Grace", "Madison", "Aria", "Victoria", "Natalie", "Lily",
    "Chloe", "Layla", "Brooklyn", "Zoe", "Penelope", "Riley", "Leah", "Hannah", "Lillian", "Addison",
    "Zoey", "Stella", "Nora", "Zara", "Maria", "Claire", "Daisy", "Aubrey", "Elena", "Charlotte"
]

surnames = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson"
]


def generate_password():
    # Генерация отдельных компонентов пароля
    uppercase_letter = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special_symbol = random.choice(string.punctuation)

    # Вычисление количества оставшихся символов
    remaining_length = 8 - len(uppercase_letter) - len(digit) - len(special_symbol)
    remaining_chars = ''.join(
        random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(remaining_length))

    # Сборка пароля и его перемешивание
    password = uppercase_letter + digit + special_symbol + remaining_chars
    password = ''.join(random.sample(password, len(password)))

    return password


def DownloadPhoto(url):

    response = requests.get(url)

    fake_name = str(uuid.uuid4())+".jpg"

    with open(fake_name, "wb") as file:
        file.write(response.content)

    return fake_name

def random_datetime_from_range(start_datetime, end_datetime):
    # Проверяем, что start_datetime раньше end_datetime
    if start_datetime > end_datetime:
        start_datetime, end_datetime = end_datetime, start_datetime

    # Вычисляем разницу в секундах между начальным и конечным временем
    time_difference = (end_datetime - start_datetime).total_seconds()

    # Генерируем случайное количество секунд в пределах разницы
    random_seconds = random.uniform(0, time_difference)

    # Добавляем случайное количество секунд к начальному времени
    random_datetime = start_datetime + datetime.timedelta(seconds=random_seconds)

    return random_datetime

def datetime_from_hour_range(hour1, hour2, timezone=0):
    current_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=timezone)

    # Получение текущей даты
    current_date = current_datetime.date()

    # Создание объектов datetime для указанных часов
    datetime1 = datetime.datetime.combine(current_date, datetime.time(hour=hour1))
    datetime2 = datetime.datetime.combine(current_date, datetime.time(hour=hour2))

    # Если случайно сгенерированное время находится в прошлом, приравниваем его к дате следующего дня
    if datetime1 < current_datetime:
        next_date = current_date + datetime.timedelta(days=1)
        datetime1 = datetime.datetime.combine(next_date, datetime.time(hour=hour1))
        datetime2 = datetime.datetime.combine(next_date, datetime.time(hour=hour2))

    if datetime2 < datetime1:
        next_date = current_date + datetime.timedelta(days=1)
        datetime2 = datetime.datetime.combine(next_date, datetime.time(hour=hour2))

    return datetime1 - datetime.timedelta(hours=timezone), datetime2 - datetime.timedelta(hours=timezone)



class ActiveSystem:

    def __init__(self, now_day, models=None):

        self.now_day = now_day

        if models:
            self.models = models
        else:
            self.models = []

        self.system()


    def system(self):

        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.Distributor())

    async def Distributor(self):

        print("Распределение")

        async with async_session() as session:
            # user = session.query(User).filter_by(id=message.from_user.id).first()

            accounts = await session.execute(select(FanslyAccount).where(FanslyAccount.status == "active"))
            accounts = accounts.scalars().all()

            tasks = []

            for account in accounts:

                acc = {'auth_token': account.auth_token,
                       'ct0': account.ct0,
                       'proxy': account.proxy,
                       'user_agent': account.user_agent,
                       'authorization_token': account.authorization_token,
                       'id': account.id}

                if account.warming_days == 0:

                    design_tasks = []
                    if random.randint(0,100) < 30:
                        design_tasks.append("Ava")
                    elif random.randint(0,100) < 5:
                        design_tasks.append("Banner")
                    elif random.randint(0,100) < 50:
                        design_tasks.append("Name")

                    timepoint = random_datetime_from_range(datetime.datetime.utcnow(),datetime.datetime.utcnow() + datetime.timedelta(hours=12))

                    tasks.append(self.TimeWaiting(acc, timepoint, 'design', design_tasks))


                if account.warming_days in [0,1]:

                    rand = random.randint(2, 4)

                    for i in range(rand):
                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'Follow'))

                else:

                    rand = random.randint(2, 4)

                    for i in range(rand):
                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'Follow'))

                    rand = random.randint(10,20)

                    for i in range(rand):
                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'Like'))

            if self.now_day in [1,2,3,4]:

                for model in self.models:

                    rand = random.randint(0, 2)

                    for i in range(rand):

                        random_acc = random.choice(accounts)

                        acc = {'auth_token': random_acc.auth_token,
                               'ct0': random_acc.ct0,
                               'proxy': random_acc.proxy,
                               'user_agent': random_acc.user_agent,
                               'authorization_token': random_acc.authorization_token,
                               'id': random_acc.id}

                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'SpecialFollow', model))

                        for ii in range(random.randint(0,3)):
                            timepoint2 = random_datetime_from_range(timepoint, timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialLike', [model, ii]))

                        for ii in range(random.randint(0,2)):
                            timepoint2 = random_datetime_from_range(timepoint,timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialComment', [model, ii]))

                        if random.choice([True,False]) == True:
                            timepoint2 = random_datetime_from_range(timepoint,timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialMessage', model))

            elif self.now_day in [5,6,7,8]:

                for model in self.models:

                    rand = random.randint(3,7)

                    for i in range(rand):

                        random_acc = random.choice(accounts)

                        acc = {'auth_token': random_acc.auth_token,
                               'ct0': random_acc.ct0,
                               'proxy': random_acc.proxy,
                               'user_agent': random_acc.user_agent,
                               'authorization_token': random_acc.authorization_token,
                               'id': random_acc.id}

                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'SpecialFollow', model))

                        for ii in range(random.randint(1, 3)):
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialLike', [model, ii]))

                        for ii in range(random.randint(0, 2)):
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialComment', [model, ii]))

                        if random.choice([True, False]) == True:
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialMessage', model))


            elif self.now_day in [9,10,11]:

                for model in self.models:

                    rand = random.randint(5, 9)

                    for i in range(rand):

                        random_acc = random.choice(accounts)

                        acc = {'auth_token': random_acc.auth_token,
                               'ct0': random_acc.ct0,
                               'proxy': random_acc.proxy,
                               'user_agent': random_acc.user_agent,
                               'authorization_token': random_acc.authorization_token,
                               'id': random_acc.id,}

                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'SpecialFollow', model))

                        for ii in range(random.randint(0, 4)):
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialLike', [model, ii]))

                        for ii in range(random.randint(1,3)):
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialComment', [model, ii]))

                        if random.choice([True, False]) == True:
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialMessage', model))

            elif self.now_day in [12,13,14,15]:

                for model in self.models:

                    rand = random.randint(5,15)

                    for i in range(rand):

                        random_acc = random.choice(accounts)

                        acc = {'auth_token': random_acc.auth_token,
                               'ct0': random_acc.ct0,
                               'proxy': random_acc.proxy,
                               'user_agent': random_acc.user_agent,
                               'authorization_token': random_acc.authorization_token,
                               'id': random_acc.id}

                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'SpecialFollow', model))

                        for ii in range(random.randint(0,5)):
                            timepoint2 = random_datetime_from_range(timepoint, timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialLike', [model, ii]))

                        for ii in range(random.randint(1,3)):
                            timepoint2 = random_datetime_from_range(timepoint,timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialComment', [model, ii]))

                        if random.choice([True,False]) == True:
                            timepoint2 = random_datetime_from_range(timepoint,timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialMessage', model))

            else:
                for model in self.models:

                    rand = random.randint(5, 15)

                    for i in range(rand):

                        random_acc = random.choice(accounts)

                        acc = {'auth_token': random_acc.auth_token,
                               'ct0': random_acc.ct0,
                               'proxy': random_acc.proxy,
                               'user_agent': random_acc.user_agent,
                               'authorization_token': random_acc.authorization_token,
                               'id': random_acc.id}

                        timepoint = random_datetime_from_range(datetime.datetime.utcnow(),
                                                               datetime.datetime.utcnow() + datetime.timedelta(
                                                                   hours=24))

                        tasks.append(self.TimeWaiting(acc, timepoint, 'SpecialFollow', model))

                        for ii in range(random.randint(0, 5)):
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialLike', [model, ii]))

                        for ii in range(random.randint(1, 3)):
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialComment', [model, ii]))

                        if random.choice([True, False]) == True:
                            timepoint2 = random_datetime_from_range(timepoint,
                                                                    timepoint + datetime.timedelta(minutes=30))
                            tasks.append(self.TimeWaiting(acc, timepoint2, 'SpecialMessage', model))

            # await View(acc['auth_token'], acc['ct0'], acc['proxy'], f"https://twitter.com/screen_name/status/{self.tweetID}")

            print("Запуск задач")
            await asyncio.gather(*tasks)



    # Async Functions
    async def TimeWaiting(self, acc, target_datetime, target, data=None):
        current_datetime = datetime.datetime.utcnow()

        # Вычисление времени ожидания до указанного target_datetime

        print(target_datetime + datetime.timedelta(hours=3), f'- {target}')

        time_difference = target_datetime - current_datetime
        seconds_to_wait = time_difference.total_seconds()

        if seconds_to_wait > 0:
            await asyncio.sleep(seconds_to_wait)

            if target == 'Like':
                await self.AsyncLike(acc)
            # elif target == 'Comment':
            #     await self.AsyncComment(acc)
            elif target == 'Follow':
                await self.AsyncFollow(acc)
            elif target == 'SpecialFollow':
                await self.AsyncSpecialFollow(acc, data)
            elif target == 'SpecialLike':
                await self.AsyncSpecialLike(acc, data)
            # elif target == 'SpecialComment':
            #     await self.AsyncSpecialComment(acc, data)
            elif target == 'SpecialMessage':
                await self.AsyncSpecialMessage(acc, data)

            elif target == 'design':
                await self.DesignAccount(acc, data)

            await self.Notification(acc['auth_token'], target)

        else:
            return


    async def AsyncLike(self, account):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        # Создайте пул потоков для выполнения синхронных функций
        with ThreadPoolExecutor() as executor:
            # Запустите синхронную функцию в пуле потоков и дождитесь ее завершения

            if account_.authorization_token:

                posts = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                 account_.proxy,
                                                 account_.user_agent).GetRecomendationPosts)

                random_post = random.choice(posts['response']['posts'])

                result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                 account_.proxy,
                                                 account_.user_agent).Like,
                                                 random_post['id'])

                if result == True:
                    logger.success(f"{account_.auth_token} - Like Success")
                else:
                    logger.error(f"{account_.auth_token} - Like Error")


    async def AsyncFollow(self, account):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        # Создайте пул потоков для выполнения синхронных функций
        with ThreadPoolExecutor() as executor:
            # Запустите синхронную функцию в пуле потоков и дождитесь ее завершения

            if account_.authorization_token:

                posts = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                            account_.proxy,
                                                            account_.user_agent).GetRecomendationUsers)

                random_user = random.choice(posts['response']['accounts'])

                result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                             account_.proxy,
                                                             account_.user_agent).Follow,
                                                 random_user['id'])

                if result == True:
                    logger.success(f"{account_.auth_token} - Follow Success")
                else:
                    logger.error(f"{account_.auth_token} - Follow Error")

            else:

                try:
                    authorization_token, user_agent = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                                account_.proxy,
                                                                account_.user_agent).LoginWithTwitter,
                                                                  account_.ct0, account_.auth_token)

                    posts = await asyncio.to_thread(FanslyModel(authorization_token,
                                                                account_.proxy,
                                                                user_agent).GetRecomendationUsers)

                    random_user = random.choice(posts['response']['accounts'])

                    result = await asyncio.to_thread(FanslyModel(authorization_token,
                                                                 account_.proxy,
                                                                 user_agent).Follow,
                                                     random_user['id'])

                    if result == True:
                        logger.success(f"{account_.auth_token} - Follow Success")
                    else:
                        logger.error(f"{account_.auth_token} - Follow Error")

                    async with async_session() as session:

                        bot = await session.execute(select(FanslyAccount).where(FanslyAccount.auth_token == account_.auth_token))
                        bot = bot.scalars().first()

                        bot.authorization_token = authorization_token
                        bot.user_agent = user_agent

                        await session.commit()

                except:

                    async with async_session() as session:

                        bot = await session.execute(
                            select(FanslyAccount).where(FanslyAccount.auth_token == account_.auth_token))
                        bot = bot.scalars().first()

                        bot.status = "ban"

                        await session.commit()

                    logger.error(f"{account_.auth_token} - Follow Error (Twitter)")


    async def AsyncSpecialLike(self, account, data):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        model_id, post_numbers = data

        # Создайте пул потоков для выполнения синхронных функций
        with ThreadPoolExecutor() as executor:
            # Запустите синхронную функцию в пуле потоков и дождитесь ее завершения


            posts = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                             account_.proxy,
                                             account_.user_agent).GetUserPosts,
                                            model_id)

            random_post = random.choice(posts['response']['posts'])

            try:
                result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                 account_.proxy,
                                                 account_.user_agent).Like,
                                                 random_post['id'])

                if result == True:
                    logger.success(f"{account_.auth_token} - Like Success")
                else:
                    logger.error(f"{account_.auth_token} - Like Error")
            except:
                traceback.print_exc()
                logger.error(f"{account_.auth_token} - Like Error")

    async def AsyncSpecialFollow(self, account, data):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        model_id = data

        # Создайте пул потоков для выполнения синхронных функций
        with ThreadPoolExecutor() as executor:

            try:
                result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                             account_.proxy,
                                                             account_.user_agent).Follow,
                                                 model_id)

                if result == True:
                    logger.success(f"{account_.auth_token} - Follow Success")
                else:
                    logger.error(f"{account_.auth_token} - Follow Error")
            except:
                traceback.print_exc()
                logger.error(f"{account_.auth_token} - Follow Error")

    async def AsyncSpecialComment(self, account, data):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        model_id, post_numbers = data

        # Создайте пул потоков для выполнения синхронных функций
        with ThreadPoolExecutor() as executor:
            # Запустите синхронную функцию в пуле потоков и дождитесь ее завершения

            posts = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                        account_.proxy,
                                                        account_.user_agent).GetUserPosts,
                                            model_id)

            random_post = random.choice(posts['response']['posts'])

            random_text = ...

            try:
                result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                             account_.proxy,
                                                             account_.user_agent).MakePost,
                                                 text=random_text, inReplyTo=random_post['id'])

                if result == True:
                    logger.success(f"{account_.auth_token} - Comment Success")
                else:
                    logger.error(f"{account_.auth_token} - Comment Error")
            except:
                traceback.print_exc()
                logger.error(f"{account_.auth_token} - Comment Error")


    async def AsyncSpecialMessage(self, account, data):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        model_id = data

        # Создайте пул потоков для выполнения синхронных функций
        with ThreadPoolExecutor() as executor:
            # Запустите синхронную функцию в пуле потоков и дождитесь ее завершения


            random_text = ...

            try:
                result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                             account_.proxy,
                                                             account_.user_agent).SendMessage,
                                                 text=random_text, groupId=model_id)

                if result == True:
                    logger.success(f"{account_.auth_token} - Message Success")
                else:
                    logger.error(f"{account_.auth_token} - Message Error")
            except:
                traceback.print_exc()
                logger.error(f"{account_.auth_token} - Message Error")

    async def DesignAccount(self, account, data):

        async with async_session() as session:

            account_ = await session.execute(select(FanslyAccount).where(FanslyAccount.id == account['id']))
            account_ = account_.scalars().first()

        with ThreadPoolExecutor() as executor:

            try:

                # if "Ava" in data:
                #
                #     a = []
                #     with open("Files/Photos(links).txt", "r") as file:
                #         for i in file:
                #             a.append(i.rstrip())
                #     random_url = random.choice(a)
                #
                #     filename = DownloadPhoto(random_url)
                #
                #     result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                #                                                  account_.proxy,
                #                                                  account_.user_agent).UploadPhoto,
                #                                      filename)
                #     logger.success(f"{account_.auth_token} - Message Success")
                #
                # if "Banner" in data:
                #     ...
                #     logger.success(f"{account_.auth_token} - Message Success")

                if "Name" in data:

                    result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                                 account_.proxy,
                                                                 account_.user_agent).ChangePassword,
                                                     "aRT909090!")

                    if result:
                        logger.success(f"{account_.auth_token} - Password Change Success")

                        result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                                     account_.proxy,
                                                                     account_.user_agent).ChangeUsername,
                                                         "aRT909090!")
                        print(result)

                        generated_name = random.choice(names) + " " + (random.choice(surnames) if random.randint(0,1) == 1 else "")
                        result = await asyncio.to_thread(FanslyModel(account_.authorization_token,
                                                                     account_.proxy,
                                                                     account_.user_agent).ChangeDisplayName,
                                                         "aRT909090!")

                    else:
                        logger.error(f"{account_.auth_token} - Password Change Error")


            except:
                traceback.print_exc()
                logger.error(f"{account_.auth_token} - Username Change Error")


async def TT():
    a = []
    with open("Files/Photos(links).txt", "r") as file:
        for i in file:
            a.append(i.rstrip())

    while True:

        async with async_session() as session:
            account_ = await session.execute(select(FanslyAccount).where(and_(FanslyAccount.auth_token == "")))
            account_ = account_.scalars().all()

            account_ = random.choice(account_)

            print(account_.auth_token)

            acc = FanslyModel(account_.authorization_token,
                              account_.proxy,
                              account_.user_agent)

            if account_.authorization_token == None:

                try:
                    authorization_token, user_agent = acc.LoginWithTwitter(account_.ct0, account_.auth_token)
                    print("Регистрация прошла успешно")

                except:

                    traceback.print_exc()
                    account_.status = "BAN"

                    print("Аккаунт забанен\n")

                    await session.commit()
                    continue

                account_.authorization_token = authorization_token
                account_.user_agent = user_agent

            info = acc.GetMe()

            if random.randint(0,100) < 30 and random.randint(0,100) < 20:

                random_url = random.choice(a)
                filename = DownloadPhoto(random_url)

                random_url = random.choice(a)
                filename2 = DownloadPhoto(random_url)

                acc.ChangeProfile(banner_path=filename, avatar_path=filename2)

                os.remove(filename)
                os.remove(filename2)

                print("Установлены баннер и аватарка")

            elif random.randint(0,100) < 30:

                random_url = random.choice(a)
                filename2 = DownloadPhoto(random_url)

                acc.ChangeProfile(avatar_path=filename2)

                os.remove(filename2)

                print("Установлена аватарка")

            if random.randint(0,100) < 80:

                random_pass = generate_password()

                d = acc.ChangePassword(random_pass)
                if d['success']:

                    print("Сменен пароль")

                    acc.ChangeUsername(random_pass)
                    print("Установлен юзернейм")

                    generated_name = random.choice(names) + " " + (random.choice(surnames) if random.randint(0, 1) == 1 else "")
                    acc.ChangeDisplayName(info['response']['account']['id'], generated_name)

                    print("Установлен никнейм")

                else:

                    print(d)


            info = acc.GetMe()
            print(info['response']['account']['username'])
            print("")

            account_.fansly_id = info['response']['account']['id']
            account_.username = info['response']['account']['username']
            account_.status = "ACTIVE"
            account_.warming_days += 1

            await session.commit()


if __name__ == '__main__':


    asyncio.run(TT())






