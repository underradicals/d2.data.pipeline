create materialized view if not exists  WeaponStatType as
select id, hash, name, description from StatType where category = 1 and (name != '' or description != '');

create index if not exists idx_weaponstattype_hash on WeaponStatType using btree (hash);
create index if not exists idx_weaponstattype_name on WeaponStatType using btree (name);


create materialized view if not exists WeaponItemType as
select id, displayname from itemtype where itemtype = 3;

create index if not exists idx_weaponitemtype_displayname on WeaponItemType using btree (displayname);

create materialized view if not exists ArmorItemType as
select id, displayname from itemtype where itemtype = 2;

create index if not exists idx_weaponitemtype_displayname on ArmorItemType using btree (displayname);

create materialized view if not exists ModItemType as
select id, displayname from itemtype where itemtype = 19;

create index if not exists idx_weaponitemtype_displayname on ModItemType using btree (displayname);