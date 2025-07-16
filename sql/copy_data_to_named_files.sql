-- Takes data from the world_content database and puts into a named file at ROOT/data/csv/*
copy (
    select row_number() over (order by Hash) as id,
           Hash,
           Name,
           Description,
           ImageUrl,
           Category
    from (select (json ->> 'hash')::bigint                             as Hash,
                 (json -> 'displayProperties' ->> 'name')::text        as Name,
                 (json -> 'displayProperties' ->> 'description')::text as Description,
                 (json -> 'displayProperties' ->> 'icon')::text        as ImageUrl,
                 (json ->> 'statCategory')::int                        as Category
          from destinystatdefinition) sub
    ) to 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\stat_types.csv'
    with (format csv, header, escape '"', quote '"');
copy (
    select row_number() over (order by Hash) as id,
           Hash,
           ItemType,
           SubType,
           DisplayName
    from (select distinct (json ->> 'hash')::bigint              as Hash,
                          (json ->> 'itemType')::int             as ItemType,
                          (json ->> 'itemSubType')::int          as SubType,
                          (json ->> 'itemTypeDisplayName')::text as DisplayName
          from destinyinventoryitemdefinition
          where (json ->> 'itemTypeDisplayName')::text != '') sub
    ) to 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\item_types.csv'
    with (format csv, header, escape '"', quote '"')