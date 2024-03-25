"""SELECT 
    c."id", 
    c."Name", 
    c."Crew", 
    c."Captain", 
    COALESCE(CAST(p."id" AS text), 'unknown') AS "Location"
FROM "Galactic Empire"."Cruisers" c
LEFT JOIN "Galactic Empire"."Planets" p ON c."Location" = p."Name"
WHERE c."Crew" <= 200 AND c."Captain" LIKE 'L%'


ORDER BY id ASC """