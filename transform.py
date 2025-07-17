from psycopg_pool import ConnectionPool

def transforms():
    with open('D:\\Personal\\D2.Data.Pipeline\\sql\\copy_data_to_named_files.sql', 'r', encoding='utf-8', newline='') as copy_data_to_named_files_handler:
        with ConnectionPool(conninfo='host=localhost port=5432 dbname=world_content user=postgres password=postgres') as pool:
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(copy_data_to_named_files_handler.read())
                conn.commit()

        with ConnectionPool(conninfo='host=localhost port=5432 dbname=destiny2 user=postgres password=postgres') as pool:
            with open('D:\\Personal\\D2.Data.Pipeline\\sql\\d2\\drop_destiny2_tables.sql', 'r', encoding='utf-8', newline='') as drop_handler:
                with pool.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(drop_handler.read())
                    conn.commit()

            with open('D:\\Personal\\D2.Data.Pipeline\\sql\\d2\\create_destiny2_tables.sql', 'r', encoding='utf-8', newline='') as create_handler:
                with pool.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(create_handler.read())
                    conn.commit()

            with open('D:\\Personal\\D2.Data.Pipeline\\sql\\d2\\copy_data_to_destiny2.sql', 'r', encoding='utf-8', newline='') as copy_data_handler:
                with pool.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(copy_data_handler.read())
                    conn.commit()

            with open('D:\\Personal\\D2.Data.Pipeline\\sql\\d2\\materialized_views.sql', 'r', encoding='utf-8', newline='') as materialized_view_handler:
                with pool.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(materialized_view_handler.read())
                    conn.commit()

if __name__ == '__main__':
    pass