

SELECT c.category, COUNT(c.case_id) FROM harass_category c GROUP BY c.category ORDER BY COUNT(c.case_id) DESC;


