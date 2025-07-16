copy (
    select row_number() over (order by Hash) as id,
           Hash,
           Name,
           Description,
           ImageUrl,
           Category
    from (select (json ->> 'hash')::bigint                            as Hash,
                 (json -> 'displayProperties' ->> 'name')::text        as Name,
                 (json -> 'displayProperties' ->> 'description')::text as Description,
                 (json -> 'displayProperties' ->> 'icon')::text       as ImageUrl,
                 (json ->> 'statCategory')::int as Category
          from destinystatdefinition) sub
    ) to 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\stat_types.csv'
    with (format csv, header, escape '"', quote '"');

copy (
    select row_number() over (order by Hash) as id,
           Hash,
           Name,
           Description,
           ImageUrl
    from (select (json ->> 'hash')::bigint                             as Hash,
                 (json -> 'displayProperties' ->> 'name')::text        as Name,
                 (json -> 'displayProperties' ->> 'description')::text as Description,
                 (json -> 'displayProperties' ->> 'icon')::text        as ImageUrl
          from destinystatdefinition
          where (json ->> 'statCategory')::int = 1
             and ((json -> 'displayProperties' ->> 'description')::text != ''
              or (json -> 'displayProperties' ->> 'icon')::text != '')) sub
    ) to 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\weapon_stat_types.csv'
    with (format csv, header, escape '"', quote '"');