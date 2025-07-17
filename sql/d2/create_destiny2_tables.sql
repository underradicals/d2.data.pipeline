create table if not exists StatType (
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


create table if not exists ItemType (
    id bigint primary key ,
    displayName text,
    itemType bigint ,
    subType text
);


create index if not exists idx_itemtype_itemType on ItemType using btree (itemType);
create index if not exists idx_itemtype_subType on ItemType using btree (subType);
create index if not exists idx_itemtype_displayName on ItemType using btree (displayName);
