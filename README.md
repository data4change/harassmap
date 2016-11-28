# HarassMap Exploration

This repository contains some of the code used to analyse the HarassMap
data at D4C.

### Inspiration

* https://theintercept.co/condolences/
* http://www.wefeelfine.org/
* http://moritz.stefaner.eu/projects/revisit/
* http://www.onthegrid.city/

### Queries

```sql
SELECT
  c.category, COUNT(c.case_id)
  FROM harass_category c
  GROUP BY c.category
  ORDER BY COUNT(c.case_id) DESC;
```

```sql
SELECT
	SUBSTR(COALESCE(h.date_of_incident, h.date), 1, 4) AS year,
    c.category AS category,
    COUNT(h.case_id) AS cases 
  FROM harass h LEFT JOIN harass_category c ON c.case_id = h.case_id
  GROUP BY 
    c.category,
    SUBSTR(COALESCE(h.date_of_incident, h.date), 1, 4);
```