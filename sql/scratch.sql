SELECT DISTINCT (json ->> 'itemTypeDisplayName')::text AS DisplayName
FROM destinyinventoryitemdefinition
WHERE (json ->> 'itemTypeDisplayName')::text != ''
  and (json ->> 'itemType')::int = 3;


select distinct (json ->> 'itemType')::int             as Category,
                (json ->> 'itemSubType')::int          as SubType,
                (json ->> 'itemTypeDisplayName')::text as DisplayName
from destinyinventoryitemdefinition
where (json ->> 'itemSubType')::int != 0
  and (json ->> 'itemType')::int != 0
order by (json ->> 'itemType')::int;

-- SELECT DISTINCT (json ->> 'itemType')::int AS ItemType
-- FROM destinyinventoryitemdefinition
-- WHERE (json ->> 'itemType')::int IS NOT NULL
-- order by (json ->> 'itemType')::int asc;
--
-- COPY (
--     SELECT ROW_NUMBER() OVER (ORDER BY ItemType) AS id,
--            ItemType
--     FROM (SELECT DISTINCT (json ->> 'itemType')::int AS ItemType
--           FROM destinyinventoryitemdefinition
--           WHERE (json ->> 'itemType')::int IS NOT NULL
--           order by (json ->> 'itemType')::int asc
-- ) sub
--     ) TO 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\item_type.csv'
-- WITH (FORMAT csv, HEADER);
--
-- COPY (
--     SELECT ROW_NUMBER() OVER (ORDER BY DisplayName) AS id,
--            DisplayName
--     FROM (SELECT DISTINCT (json ->> 'itemTypeDisplayName')::text AS DisplayName
--           FROM destinyinventoryitemdefinition
--           WHERE (json ->> 'itemTypeDisplayName')::text != ''
--             and (json ->> 'itemType')::int = 3) sub
--     ) TO 'D:\\Personal\\D2.Data.Pipeline\\data\\csv\\display_name.csv'
--     WITH (FORMAT csv, HEADER);