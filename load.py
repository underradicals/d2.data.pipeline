import csv
import logging
import orjson
from psycopg_pool import ConnectionPool
from redis import Redis
from pathlib import Path

ROOT = Path(__file__).parent

logging.basicConfig(level=logging.INFO)
r = Redis(db=1, decode_responses=True)

_keys_list = r.keys("Destiny*:jwccp")
keys_list = [x.split(":")[0] for x in _keys_list]

drop_table_names = '\n'.join([f"drop table if exists {x.split(":")[0]};" for x in _keys_list])
create_table_names = '\n'.join([f"create table if not exists {x.split(":")[0]} (id bigint primary key,json jsonb);" for
                              x in
                              _keys_list])
def create_tables_sql():
    with open(f'{ROOT}\\sql\\tables.sql', 'w', encoding='utf-8') as f:
        f.write(create_table_names)

def drop_tables_sql():
    with open(f'{ROOT}\\sql\\drop_tables.sql', 'w', encoding='utf-8') as f:
        f.write(drop_table_names)


def copy_from_sql():
    with open(f'{ROOT}\\sql\\copy_from_table.sql', 'w', encoding='utf-8') as f:
        copy_from_query = '\n'.join([f"COPY {x} (id, json) FROM '{ROOT}\\csv\\{x}.csv' WITH (FORMAT csv,HEADER true,QUOTE \'\"\',ESCAPE \'\"\');" for x in keys_list])
        f.write(copy_from_query)

def copy_from():
    with ConnectionPool(conninfo='host=localhost port=5432 dbname=world_content user=postgres password=postgres') as pool:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                logging.info(f"Dropping tables")
                cur.execute(drop_table_names)

        with pool.connection() as conn:
            with conn.cursor() as cur:
                logging.info(f"Creating tables")
                cur.execute(create_table_names)

        for table_name in keys_list:
            logging.info(f"Creating {table_name}.csv")
            json_blob = str(r.get(f"{table_name}:jwccp"))
            json_dict = orjson.loads(json_blob.encode('utf-8'))
            with open(f'{ROOT}\\csv\\{table_name}.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                for key, value in json_dict.items():
                    writer.writerow([int(key), orjson.dumps(value).decode('utf-8')])

        with pool.connection() as conn:
            with conn.cursor() as cur:
                for table_name in keys_list:
                    logging.info(f"COPY FROM {table_name}.csv")
                    cur.execute(f"""
                        COPY {table_name} (id, json)
                        FROM '{ROOT}\\csv\\{table_name}.csv'
                        WITH (
                            FORMAT csv,
                            HEADER true,
                            QUOTE '"',
                            ESCAPE '"'
                        )
                    """)
            conn.commit()

def load_main():
    create_tables_sql()
    drop_tables_sql()
    copy_from_sql()
    copy_from()

if __name__ == '__main__':
    pass