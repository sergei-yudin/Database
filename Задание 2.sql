SELECT title, duration
FROM tracks
WHERE duration = (
    SELECT MAX(duration)
    FROM tracks
);


SELECT title, 
       duration || ' minutes' AS duration
FROM tracks
WHERE duration >= 3.5
ORDER BY duration DESC;

SELECT name
FROM collections
WHERE year BETWEEN 2018 AND 2020;

SELECT alias
FROM performers
WHERE alias NOT LIKE '% %';

SELECT title
FROM tracks
WHERE title ILIKE '%мой%' OR title ILIKE '%my%';