import asyncio
import datetime
import random
import time
import uuid

from DB import *

async def AddBots():

    accs1 = []
    accs2 = []

    with open("Files/proxies.txt", "r") as file:
        for i in file:
            accs1.append(i.rstrip())

    with open("Files/twitters.txt", "r") as file:
        for i in file:
            accs2.append([i.rstrip().split("auth_token=")[-1].split(";")[0], i.rstrip().split("ct0=")[-1].split(";")[0]])

    for index, item in enumerate(accs1):

        if accs2[index] == ["",""]:
            continue

        b = FanslyAccount(id=str(uuid.uuid4()),
                          auth_token=accs2[index][0],
                          ct0=accs2[index][1],
                          proxy=item,

                          max_follows= random.randint(20,50))

        async with async_session() as session:

            session.add(b)

            await session.commit()

async def AllBots():

    async with async_session() as session:
        bots = await session.execute(select(FanslyAccount))
        bots = bots.scalars().all()

        c = 0
        for bot in bots:
            print(bot.auth_token, bot.ct0, bot.proxy, bot.warming_days, bot.status)
            c+=1

        print(c)

async def CleanBots():

    async with async_session() as session:
        bots = await session.execute(select(FanslyAccount))
        bots = bots.scalars().all()

        c = 0
        for bot in bots:
            if len(bot.ct0) != 160:
                await session.delete(bot)
            c+=1

        await session.commit()

async def EditBots():

    async with async_session() as session:
        bots = await session.execute(select(FanslyAccount))
        bots = bots.scalars().all()

        c = 0
        for bot in bots:
            bot.status = "ACTIVE"
            c+=1

        await session.commit()

async def EditBot():

    async with async_session() as session:
        bots = await session.execute(select(FanslyAccount).where(FanslyAccount.proxy=="154.95.0.19:6272:wnfefygv:cw1tbwmm3mdn"))
        bots = bots.scalars().first()

        bots.auth_token = ""
        bots.ct0 = ""

        bots.status = "ACTIVE"

        await session.commit()

async def DeleteBots():

    async with async_session() as session:
        bots = await session.execute(select(FanslyAccount))
        bots = bots.scalars().all()

        c = 0
        for bot in bots:
            await session.delete(bot)
            c+=1

        await session.commit()


if __name__ == '__main__':

    asyncio.run(DeleteBots())


