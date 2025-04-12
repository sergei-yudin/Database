SELECT a.name AS album_name
FROM albums a
JOIN album_performer ap ON a.albumID = ap.albumID
JOIN performer_genre pg ON ap.performerID = pg.performerID
GROUP BY a.albumID
HAVING COUNT(DISTINCT pg.genreID) > 1;

SELECT t.title AS track_name
FROM tracks t
LEFT JOIN collection_tracks ct ON t.trackID = ct.trackID
WHERE ct.trackID IS NULL;

SELECT DISTINCT p.alias, t.title, t.duration
FROM performers p
JOIN album_performer ap ON p.performerID = ap.performerID
JOIN albums a ON ap.albumID = a.albumID
JOIN tracks t ON a.albumID = t.albumID
WHERE t.duration = (
    SELECT MIN(duration)
    FROM tracks
);


SELECT a.name, COUNT(t.trackID) AS track_count
FROM albums a
JOIN tracks t ON a.albumID = t.albumID
GROUP BY a.albumID
HAVING COUNT(t.trackID) = (
    SELECT COUNT(t2.trackID)
    FROM albums a2
    JOIN tracks t2 ON a2.albumID = t2.albumID
    GROUP BY a2.albumID
    ORDER BY COUNT(t2.trackID)
    LIMIT 1
);