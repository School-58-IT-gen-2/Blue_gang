'''SELECT pt.id, pt."Name" , COUNT(p."Type") AS planet_count
FROM "Galactic Empire"."Planets" p
RIGHT JOIN "Galactic Empire"."Planet Types" pt ON p."Type" = pt.id
GROUP BY pt.id, pt."Name"
ORDER BY planet_count DESC;'''