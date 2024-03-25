"""SELECT 
    c."id", 
    c."Name", 
    c."Crew", 
    c."Captain", 
    COALESCE(p."Name", 'unknown') AS "Location"
FROM "Galactic Empire"."Cruisers" c
LEFT JOIN "Galactic Empire"."Planets" p ON c."Name" = CAST(p."id" AS text)
WHERE c."Crew" <= 200 AND c."Captain" LIKE 'L%'


ORDER BY id ASC """