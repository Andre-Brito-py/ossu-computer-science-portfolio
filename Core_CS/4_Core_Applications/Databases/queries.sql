-- Stanford Databases - SQL Queries Exercises

-- 1. Find the titles of all movies directed by Steven Spielberg.
SELECT title 
FROM Movie 
WHERE director = 'Steven Spielberg';

-- 2. Find all years that have a movie that received a rating of 4 or 5, and sort them in increasing order.
SELECT DISTINCT year 
FROM Movie 
JOIN Rating USING(mID) 
WHERE stars >= 4 
ORDER BY year;

-- 3. Find the titles of all movies that have no ratings.
SELECT title 
FROM Movie 
WHERE mID NOT IN (SELECT mID FROM Rating);

-- 4. Some reviewers didn't provide a date with their rating. Find the names of all reviewers who have ratings with a NULL value for the date.
SELECT name 
FROM Reviewer 
JOIN Rating USING(rID) 
WHERE ratingDate IS NULL;

-- 5. Write a query to return the ratings data in a more readable format: reviewer name, movie title, stars, and ratingDate. Also, sort the data, first by reviewer name, then by movie title, and lastly by number of stars.
SELECT name, title, stars, ratingDate 
FROM Movie 
JOIN Rating USING(mID) 
JOIN Reviewer USING(rID) 
ORDER BY name, title, stars;

-- 6. For all cases where the same reviewer rated the same movie twice and gave it a higher rating the second time, return the reviewer's name and the title of the movie.
SELECT name, title 
FROM (
    SELECT r1.rID, r1.mID 
    FROM Rating r1 
    JOIN Rating r2 ON r1.rID = r2.rID AND r1.mID = r2.mID 
    WHERE r1.ratingDate < r2.ratingDate AND r1.stars < r2.stars
) AS improved 
JOIN Reviewer USING(rID) 
JOIN Movie USING(mID);
