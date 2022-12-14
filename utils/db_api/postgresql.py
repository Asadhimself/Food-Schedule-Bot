from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS all_users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO all_users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM all_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM all_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM all_users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM all_users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE all_users", execute=True)

    async def set_private_table(self, telegram_id):
        table_name = f"user_{str(telegram_id)}"
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM default_food'
        return await self.execute(sql, execute=True)

    async def send_food(self, when, day, telegram_id):
        table_name = f"user_{str(telegram_id)}"
        sql = f'''SELECT "{when}"
        FROM {table_name}
        WHERE day=$1
        '''
        return await self.execute(sql, day, fetchval=True)

    async def change_food(self, when, day, telegram_id, changes):
        table_name = f"user_{str(telegram_id)}"
        sql = f'''Update {table_name}
        SET "{when}"=$1
        WHERE day=$2
        '''
        return await self.execute(sql, changes, day, execute=True)

    async def get_all_products(self):
        sql = "SELECT * FROM food_calories"
        return await self.execute(sql, fetch=True)
