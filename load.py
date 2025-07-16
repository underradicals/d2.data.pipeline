import io
import os
import csv
import logging
import orjson
from psycopg_pool import ConnectionPool
from redis import Redis
from pathlib import Path
from aiofile import AIOFile, Writer
from utils import timed

ROOT = Path(__file__).parent

logging.basicConfig(level=logging.INFO)
r = Redis(db=1, decode_responses=True)

_keys_list = r.keys("Destiny*:jwccp")
keys_list = [x.split(":")[0] for x in _keys_list]

drop_table_names = '\n'.join([f"drop table if exists {x.split(":")[0]};" for x in _keys_list])
create_table_names = '\n'.join([f"create table if not exists {x.split(":")[0]} (id bigint primary key,json jsonb);" for
                              x in
                              _keys_list])
copy_from_query = '\n'.join([f"COPY {x} (id, json) FROM '{ROOT}\\csv\\{x}.csv' WITH (FORMAT csv,HEADER true,QUOTE \'\"\',ESCAPE \'\"\');" for x in keys_list])


def create_tables_sql():
    with open(f'{ROOT}\\sql\\create_world_content_tables.sql', 'w', encoding='utf-8') as f:
        f.write(create_table_names)

def drop_tables_sql():
    with open(f'{ROOT}\\sql\\drop_world_content_tables.sql', 'w', encoding='utf-8') as f:
        f.write(drop_table_names)


def copy_from_sql():
    with open(f'{ROOT}\\sql\\copy_data_from_world_content.sql', 'w', encoding='utf-8') as f:
        f.write(copy_from_query)


def drop_world_content_tables(conn):
    with conn.cursor() as cur:
        logging.info(f"Dropping tables")
        cur.execute(drop_table_names)


def create_world_content_tables(conn):
    with conn.cursor() as cur:
        logging.info(f"Creating tables")
        cur.execute(create_table_names)


def to_dict(table_name: str):
    json_blob = str(r.get(f"{table_name}:jwccp"))
    return orjson.loads(json_blob.encode('utf-8'))

def create_manifest_schema_csv_files(table_name: str, json_dict: dict):
    with open(f'{ROOT}\\csv\\{table_name}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for key, value in json_dict.items():
            writer.writerow([int(key), orjson.dumps(value).decode('utf-8')])



async def create_manifest_schema_csv_file_async(table_name: str, json_dict: dict):
    filepath = os.path.join(ROOT, 'csv', f'{table_name}.csv')
    async with AIOFile(filepath, 'w', encoding='utf-8') as f:
        writer = Writer(f)

        for key, value in json_dict.items():
            buffer = io.StringIO()
            csv_writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([int(key), orjson.dumps(value).decode('utf-8')])
            await writer(buffer.getvalue())
        await f.fsync()


def seed_world_content_database(conn):
    with conn.cursor() as cur:
        logging.info(f"Seeding Data...")
        cur.execute(copy_from_query)
        logging.info(f"Seeding Complete")

@timed('Copy From Sync')
def copy_from():
    with ConnectionPool(conninfo='host=localhost port=5432 dbname=world_content user=postgres password=postgres') as pool:
        with pool.connection() as conn:
            drop_world_content_tables(conn)

        with pool.connection() as conn:
            create_world_content_tables(conn)

        for table_name in keys_list:
            logging.info(f"Creating {table_name}.csv")
            json_dict = to_dict(table_name)
            create_manifest_schema_csv_files(table_name, json_dict)

        with pool.connection() as conn:
            seed_world_content_database(conn)
            conn.commit()


def load_main():
    create_tables_sql()
    drop_tables_sql()
    copy_from_sql()
    copy_from()


if __name__ == '__main__':
    pass