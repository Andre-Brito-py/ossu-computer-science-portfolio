-- Trigger example for PostgreSQL
-- Automatically updates the rating date to CURRENT_DATE if it is inserted as NULL

CREATE OR REPLACE FUNCTION update_date_if_null()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ratingDate IS NULL THEN
        NEW.ratingDate := CURRENT_DATE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_rating_date
BEFORE INSERT ON Rating
FOR EACH ROW
EXECUTE FUNCTION update_date_if_null();

-- View to see only highly rated movies
CREATE VIEW HighlyRatedMovies AS
SELECT m.title, m.director, AVG(r.stars) as avg_rating
FROM Movie m
JOIN Rating r ON m.mID = r.mID
GROUP BY m.title, m.director
HAVING AVG(r.stars) >= 4;
