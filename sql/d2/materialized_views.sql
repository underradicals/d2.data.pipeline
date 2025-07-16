create materialized view if not exists  WeaponStatType as
select id, hash, name, description from StatType where category = 1 and (name != '' or description != '');

create index concurrently if not exists idx_weaponstattype_hash on WeaponStatType using btree (hash);
create index concurrently if not exists idx_weaponstattype_name on WeaponStatType using btree (name);