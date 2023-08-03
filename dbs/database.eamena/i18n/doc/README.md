select distinct nodetype from concepts

...

select * from concepts
where nodetype like 'ConceptScheme'
order by nodetype

"00000000-0000-0000-0000-000000000001"  "ARCHES"  "ConceptScheme"
"00000000-0000-0000-0000-000000000006"  "CANDIDATES"  "ConceptScheme"
"470882be-9ca4-450a-bf49-f394c75f5d44"  "https://database.eamena.org/concepts/470882be-9ca4-450a-bf49-f394c75f5d44" "ConceptScheme"
"4a98075d-815f-327b-be0e-518b32f7623b"  "https://database.eamena.org/concepts/4a98075d-815f-327b-be0e-518b32f7623b" "ConceptScheme"

select * from concepts
where nodetype like 'Collection'
order by legacyoid
limit 10

"00000000-0000-0000-0000-000000000005"  "ARCHES RESOURCE CROSS-REFERENCE RELATIONSHIP TYPES COLLECTION" "Collection"
"050d11e9-576c-4238-8623-e797dd2d7dce"  "https://database.eamena.org/concepts/050d11e9-576c-4238-8623-e797dd2d7dce" "Collection"
"0678d237-f891-44b8-b090-440ca4b53004"  "https://database.eamena.org/concepts/0678d237-f891-44b8-b090-440ca4b53004" "Collection"
"07f55568-98b7-44ef-a4f0-f21317c2f3f6"  "https://database.eamena.org/concepts/07f55568-98b7-44ef-a4f0-f21317c2f3f6" "Collection"
"0933ae5f-2e95-47c9-9766-9d32c1bd24a8"  "https://database.eamena.org/concepts/0933ae5f-2e95-47c9-9766-9d32c1bd24a8" "Collection"
"094c866e-6367-400c-9f68-619765af9e20"  "https://database.eamena.org/concepts/094c866e-6367-400c-9f68-619765af9e20" "Collection"
"099c9fff-65b0-4356-8e9f-4252dbd4925f"  "https://database.eamena.org/concepts/099c9fff-65b0-4356-8e9f-4252dbd4925f" "Collection"
"0e514275-1dbe-4b57-a9ac-bbec7d0a3a19"  "https://database.eamena.org/concepts/0e514275-1dbe-4b57-a9ac-bbec7d0a3a19" "Collection"
"0e997a49-bad6-43d3-8465-d4e01e50786e"  "https://database.eamena.org/concepts/0e997a49-bad6-43d3-8465-d4e01e50786e" "Collection"
"107ef12d-fcc3-44b8-85cb-f5fc2b35dbd1"  "https://database.eamena.org/concepts/107ef12d-fcc3-44b8-85cb-f5fc2b35dbd1" "Collection"

select * from concepts
where nodetype like 'Concept'
order by legacyoid
limit 10

"00000000-0000-0000-0000-000000000004"  "ARCHES RESOURCE CROSS-REFERENCE RELATIONSHIP TYPES CONCEPT"  "Concept"
"bc9d4f2e-b732-4e99-ad2c-36bb3bf7d855"  "bc9d4f2e-b732-4e99-ad2c-36bb3bf7d855"  "Concept"
"c3a4906f-c2ec-444d-aeac-5bbfc90961c3"  "c3a4906f-c2ec-444d-aeac-5bbfc90961c3"  "Concept"
"00000000-0000-0000-0000-000000000007"  "DEFAULT RESOURCE TO RESOURCE RELATIONSHIP TYPE"  "Concept"
"000d5675-6671-32f2-918d-f8b14460f305"  "https://database.eamena.org/concepts/000d5675-6671-32f2-918d-f8b14460f305" "Concept"
"00539d1b-4ec9-3afa-a9d3-9a94c5af792b"  "https://database.eamena.org/concepts/00539d1b-4ec9-3afa-a9d3-9a94c5af792b" "Concept"
"0090df22-2b96-3340-9727-ba4399fc9f27"  "https://database.eamena.org/concepts/0090df22-2b96-3340-9727-ba4399fc9f27" "Concept"
"009d2cf0-7439-3875-814a-2149e5190232"  "https://database.eamena.org/concepts/009d2cf0-7439-3875-814a-2149e5190232" "Concept"
"009ea2f3-ab34-3fd8-b875-1ae6996268fb"  "https://database.eamena.org/concepts/009ea2f3-ab34-3fd8-b875-1ae6996268fb" "Concept"
"00a95e08-0062-4712-bb1c-41eda7660585"  "https://database.eamena.org/concepts/00a95e08-0062-4712-bb1c-41eda7660585" "Concept"

SELECT legacyoid, COUNT(*) as nb
FROM concepts
GROUP BY legacyoid
HAVING COUNT(*) > 1
LIMIT 10

[Empty]

--

Thesauri : Bronze Age (Arabia) (en-US) (Concept) -> https://database.eamena.org/concepts/4550d0f3-24c2-4ada-9fbe-52e5974db973
Concepts : Bronze Age (Arabia) (en-US) (Concept) -> 4550d0f3-24c2-4ada-9fbe-52e5974db973

select * from concepts
where legacyoid like 'https://database.eamena.org/concepts/4550d0f3-24c2-4ada-9fbe-52e5974db973'

"4550d0f3-24c2-4ada-9fbe-52e5974db973"  "https://database.eamena.org/concepts/4550d0f3-24c2-4ada-9fbe-52e5974db973" "Concept"

e9b0c0c9-9bdb-43f5-a25c-d82870e056b7

https://database.eamena.org/

---

translation

py3 skos2excel ./data/EAMENA.xml ./data/EAMENA_out.csv -lang fr -f csv