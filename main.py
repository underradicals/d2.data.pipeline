from os import environ
from asyncio import run

from redis.asyncio import Redis
from requests import Session, get

API_KEY = environ['D2_API_KEY']
store = Redis(db=1, decode_responses=True)

async def get_manifest(url: str, api_key: str, cache_key: str) -> str:
    _cache_key = f'{cache_key}:value'
    cache_key_value: str | bytes | None = await store.get(_cache_key)

    if cache_key_value is None:
        with get(url, stream=True, allow_redirects=True, headers={'x-api-key': api_key}) as response:
            response.raise_for_status()
            max_age = response.headers.get('Cache-Control').split('=')[-1]
            content = response.content
            await store.set(_cache_key, content, ex=int(max_age))
            return content.decode('utf-8')

    return cache_key_value

async def main():
    manifest_string = await get_manifest('https://www.bungie.net/Platform/Destiny2/Manifest', API_KEY, 'manifest')
    print(type(manifest_string))

if __name__ == '__main__':
    run(main())