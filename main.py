from os import environ
from asyncio import run, gather
from json import loads

import httpx
from httpx import AsyncClient, stream

from orjson import loads as orjson_loads, OPT_INDENT_2
from redis.asyncio import Redis
from requests import Session, get

from domain.pd.Manifest import Manifest
import logging

logging.basicConfig(level=logging.INFO)

API_KEY = environ['D2_API_KEY']
store = Redis(db=1, decode_responses=True)

async def get_manifest(url: str, api_key: str, cache_key: str) -> str:
    _cache_key = f'{cache_key}:value'
    cache_key_value: str | bytes | None = await store.get(_cache_key)

    if cache_key_value is None:
        print('Cache key not found')
        with get(url, stream=True, allow_redirects=True, headers={'x-api-key': api_key}) as response:
            response.raise_for_status()
            max_age = response.headers.get('Cache-Control').split('=')[-1]
            content = response.content
            await store.set(_cache_key, content, ex=int(max_age))
            return content.decode('utf-8')

    logging.info("Returning Cache Value")
    return cache_key_value



async def download_file_async(client: httpx.AsyncClient, url: str, api_key: str, cache_key: str):
    _cache_key = f'{cache_key}:jwccp'
    _last_modified_cache_key = f'{cache_key}:last_modified'
    last_modified_cache_value: str = await store.get(_last_modified_cache_key)
    cache_key_value: str | bytes | None = await store.get(_cache_key)

    if last_modified_cache_value is None:
        logging.info('First Time: Lets make a good impression')
        response = await client.get(url, follow_redirects=True, headers={'x-api-key': api_key})
        response.raise_for_status()
        last_modified = response.headers.get('Last-Modified')
        max_age = response.headers.get('Cache-Control').split('=')[-1]
        content = response.content
        await store.set(_cache_key, content, ex=int(max_age))
        await store.set(_last_modified_cache_key, last_modified)
        return None

    if cache_key_value is None:
        logging.info('Max Age Expired: Falling back to last modified')
        headers = {'x-api-key': api_key, 'If-None-Match': last_modified_cache_value}
        response = await client.get(url, follow_redirects=True, headers=headers)
        response.raise_for_status()

        if response.status_code != 304:
            logging.info('Last Modified Expired: Refilling Cache')
            last_modified = response.headers.get('Last-Modified')
            max_age = response.headers.get('Cache-Control').split('=')[-1]
            content = response.content
            await store.set(_cache_key, content, ex=int(max_age))
            await store.set(_last_modified_cache_key, last_modified)
            return None
        else:
            return None
    return None


async def get_json_world_component_content_paths(url_list: list[tuple[str, str]]):
    async with AsyncClient(http2=True, base_url='https://www.bungie.net') as client:
        tasks = [download_file_async(client, url[1], API_KEY, url[0]) for url in url_list]
        await gather(*tasks)




async def deserialize() -> Manifest:
    manifest_string = await get_manifest('https://www.bungie.net/Platform/Destiny2/Manifest', API_KEY, 'manifest')
    return Manifest.model_validate(loads(manifest_string))


async def to_json():
    manifest_string = await get_manifest('https://www.bungie.net/Platform/Destiny2/Manifest', API_KEY, 'manifest')
    return orjson_loads(manifest_string.encode('utf-8'))


async def get_uris(result: Manifest) -> list[tuple[str, str]]:
    return [x for x in result.Response.jsonWorldComponentContentPaths.en.model_dump().items()]


async def main() -> None:
    manifest = await deserialize()
    uris = await get_uris(manifest)
    await get_json_world_component_content_paths(uris)

if __name__ == '__main__':
    run(main())