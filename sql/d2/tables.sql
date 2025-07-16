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