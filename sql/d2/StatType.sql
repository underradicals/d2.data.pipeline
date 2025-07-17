drop table if exists StatType cascade;

create table StatType (
    id bigint primary key,
    hash bigint ,
    name text,
    description text,
    imageUrl text,
    category int
);

create index if not exists idx_stattype_hash on StatType using btree (hash);
create index if not exists idx_stattype_name on StatType using btree (name);
create index if not exists idx_stattype_category on StatType using btree (category);

copy StatType from 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\stat_types.csv' with (format csv, header, escape '"', quote '"');

create materialized view if not exists  WeaponStatType as
select id, hash, name, description from StatType where category = 1 and (name != '' or description != '');

create index if not exists idx_weaponstattype_hash on WeaponStatType using btree (hash);
create index if not exists idx_weaponstattype_name on WeaponStatType using btree (name);