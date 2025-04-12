SELECT g.name AS genre, COUNT(pg.performerID) AS performer_count
FROM genre g
LEFT JOIN performer_genre pg ON g.genreID = pg.genreID
GROUP BY g.name;

SELECT a.name AS album_name, COUNT(t.trackID) AS track_count
FROM albums a
JOIN tracks t ON a.albumID = t.albumID
WHERE a.year BETWEEN 2019 AND 2020
GROUP BY a.name;

SELECT a.name AS album_name, 
       AVG(t.duration) AS avg_duration_minutes
FROM albums a
JOIN tracks t ON a.albumID = t.albumID
GROUP BY a.name;

SELECT p.alias
FROM performers p
WHERE p.performerID NOT IN (
    SELECT DISTINCT ap.performerID
    FROM album_performer ap
    JOIN albums a ON ap.albumID = a.albumID
    WHERE a.year = 2020
);

SELECT c.name AS collection_name
FROM collections c
JOIN collection_tracks ct ON c.collectionID = ct.collectionID
JOIN tracks t ON ct.trackID = t.trackID
JOIN album_performer ap ON t.albumID = ap.albumID
JOIN performers p ON ap.performerID = p.performerID
WHERE p.alias = 'Michael Jackson';

