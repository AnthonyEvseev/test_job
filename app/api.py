import asyncio
from contextlib import asynccontextmanager
from typing import Optional
from uuid import UUID

import aio_pika
import aioredis
from aio_pika import IncomingMessage, Message
from aio_pika.abc import AbstractQueueIterator, AbstractRobustChannel
from fastapi import Query, FastAPI

from .model import Task
from .settings import conf

app = FastAPI(version=conf.version)


@asynccontextmanager
async def get_pika() -> AbstractRobustChannel:
    connection = await aio_pika.connect_robust(conf.rabbit_dsn)
    async with connection:
        channel = await connection.channel()
        yield channel


@asynccontextmanager
async def get_redis() -> aioredis.Redis:
    conn = await aioredis.create_redis_pool(conf.redis_dsn)
    try:
        yield conn
    finally:
        conn.close()


@app.on_event('startup')
async def pika_declare():
    asyncio.get_running_loop().create_task(calc_worker())


@app.post("/add_two_numbers")
async def send_task(a: int = Query(...), b: int = Query(...), ) -> UUID:
    task = Task(a=a, b=b)
    message = task.json().encode()
    async with get_pika() as pika_channel:
        await pika_channel.default_exchange.publish(Message(message), routing_key=conf.queue_name)
    return task.task_uid


@app.get("/get_adds_result")
async def get_task(task_uid: UUID = Query(...), ) -> Optional[int]:
    async with get_redis() as redis:
        if await redis.exists(str(task_uid)):
            return await redis.get(str(task_uid))


async def calc_worker():
    async with get_pika() as pika_channel:
        await pika_channel.set_qos(prefetch_count=10)
        queue = await pika_channel.declare_queue(conf.queue_name, durable=True)
        async with queue.iterator() as queue_iter:  # type: AbstractQueueIterator
            async for message in queue_iter:  # type: IncomingMessage
                async with message.process():
                    await process_calc_service_operation(message.body)


async def process_calc_service_operation(message: bytes):
    task = Task.parse_raw(message)
    async with get_redis() as redis:
        await redis.set(str(task.task_uid), str(task.a + task.b))
