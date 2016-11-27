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
