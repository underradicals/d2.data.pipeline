import json
from os import environ
from asyncio import run, gather
from json import loads
from httpx import AsyncClient
from orjson import loads as orjson_loads
from redis.asyncio import Redis
from requests import get
import logging

from domain.pd.Manifest import Manifest

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
            content = response.content
            await store.set(_cache_key, content, ex=604800)
            return content.decode('utf-8')

    logging.info("Returning Cache Value")
    return cache_key_value



async def download_file_async(client: AsyncClient, url: str, api_key: str, cache_key: str):
    _cache_key = f'{cache_key}:jwccp'
    cache_key_value: str | bytes | None = await store.get(_cache_key)

    if cache_key_value is None:
        logging.info('Max Age Expired')
        response = await client.get(url, follow_redirects=True, headers={'x-api-key': api_key})
        response.raise_for_status()
        logging.info(response.status_code)
        content = response.content
        await store.set(_cache_key, content, ex=604800)
    return None


async def get_json_world_component_content_paths(url_list: list[tuple[str, str]]):
    async with AsyncClient(http2=True, base_url='https://www.bungie.net') as client:
        tasks = [download_file_async(client, url[1], API_KEY, url[0]) for url in url_list]
        await gather(*tasks)




async def deserialize() -> Manifest:
    manifest_string = await get_manifest('https://www.bungie.net/Platform/Destiny2/Manifest', API_KEY, 'manifest')
    with open('manifest.json', 'w') as manifest:
        manifest.write(json.dumps(json.loads(manifest_string), indent=2))
    return Manifest.model_validate(loads(manifest_string))


async def to_json():
    manifest_string = await get_manifest('https://www.bungie.net/Platform/Destiny2/Manifest', API_KEY, 'manifest')
    return orjson_loads(manifest_string.encode('utf-8'))


async def get_uris(result: Manifest) -> list[tuple[str, str]]:
    return [x for x in result.Response.jsonWorldComponentContentPaths.en.model_dump().items()]


async def ingestion_main() -> None:
    manifest = await deserialize()
    uris = await get_uris(manifest)
    await get_json_world_component_content_paths(uris)

if __name__ == '__main__':
    pass