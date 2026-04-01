import asyncio
import json

from redis.asyncio import Redis

from app.core.config import settings


async def main() -> None:
    redis = Redis.from_url(settings.redis_url)
    pubsub = redis.pubsub()
    await pubsub.subscribe("pam.jobs")
    print("worker running - listening pam.jobs")

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        payload = message["data"]
        try:
            body = json.loads(payload)
        except Exception:
            body = {"raw": str(payload)}
        print(f"job processed: {body}")


if __name__ == "__main__":
    asyncio.run(main())
