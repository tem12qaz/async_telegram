import logging
import asyncio

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine

from .config import database_uri, QUERY



class Database:
    engine = create_async_engine(database_uri)

    async def update_user(telegram_id, **kwargs):
        async with Database.engine.begin() as conn:
            args = (str(kwargs)[1:-1]).replace(':' , '=').replace("'",'')
            await conn.execute(text(f'UPDATE telegram_user SET {args} WHERE telegram_id=telegram_id'))


    async def create_user(**kwargs):
        async with Database.engine.begin() as conn:
            keys = str(list(kwargs.keys()))[1:-1].replace("'", '')
            values = str(list(kwargs.values()))[1:-1].replace("'", '')
            await conn.execute(text(f'INSERT INTO telegram_user ({keys})  VALUES ({values})'))

    async def get_user(telegram_id):
        async with Database.engine.begin() as conn:
            result = await conn.execute(text(f'SELECT * FROM telegram_user WHERE telegram_id={telegram_id}'))
        row = result.fetchone()
        if row == None:
            raise IndexError('user not found')
        return row

    async def get_all_messages():
        async with Database.engine.begin() as conn:
            result = await conn.execute(
                text(QUERY)
            )
        rows = list(result.fetchall())

        for k in range (3,5):
            for i in range (len(rows)):
                rows[i] = list(rows[i])
                if rows[i][k] == [None]:
                    rows[i][k] = []

                else:
                    keys = []
                    values = []
                    for j in range (len(rows[i][k])):
                        rows[i][k][j] = dict(rows[i][k][j])
                        if k == 3:
                            keys.append(rows[i][k][j].get('text'))
                            values.append(rows[i][k][j])

                    if k==3:
                        rows[i][k] = dict(zip(keys, values))
        return rows
