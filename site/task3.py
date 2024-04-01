"""ALTER TABLE "Galactic Empire"."Systems" ALTER "Star Type" SET DEFAULT 'Red Dwarf'; 
ALTER TABLE "Galactic Empire"."Systems" ALTER "Allegiance" SET DEFAULT 'Empire';
INSERT INTO "Galactic Empire"."Systems"("Name")
SELECT 'Captain''s ' || c."Captain" || ' system'
FROM "Galactic Empire"."Cruisers" c
WHERE c."Crew" > 100  
AND c."Captain" NOT LIKE '%l%' 
AND c."Captain" NOT LIKE '%L%' 
AND c."Captain" NOT LIKE '%o%' 
AND c."Captain" NOT LIKE '%O%' 
AND c."Captain" NOT LIKE '%h%' 
AND c."Captain" NOT LIKE '%H%'

"""
