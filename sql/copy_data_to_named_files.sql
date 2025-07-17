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
    select row_number() over (order by ItemType) as id,
           DisplayName,
           ItemType,
           SubType
    from (select distinct (json ->> 'itemTypeDisplayName')::text as DisplayName,
                          (json ->> 'itemType')::int             as ItemType,
                          (json ->> 'itemSubType')::int          as SubType
          from destinyinventoryitemdefinition
          where ((json ->> 'itemTypeDisplayName')::text is not null and (json ->> 'itemTypeDisplayName')::text != '')
            and ((json ->> 'itemType')::int = 2 or (json ->> 'itemType')::int = 3 or (json ->> 'itemType')::int = 19)
          order by ItemType
) sub
    ) to 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\item_types.csv'
with (format csv, header, escape '"', quote '"');
