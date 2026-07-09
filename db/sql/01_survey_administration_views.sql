CREATE OR REPLACE VIEW kpi_time_survey_administration_summary AS
SELECT
    (NOW()::date - MIN("Submitted at")::date) AS days_until_now,
    ((NOW()::date - MIN("Submitted at")::date) / 7) + 1 AS weeks_until_now
FROM responses
LIMIT 1;


CREATE OR REPLACE VIEW kpi_submissions_by_day AS
SELECT
    ("Submitted at"::date - (SELECT MIN("Submitted at")::date FROM responses)) AS day_offset,
    COUNT(*) AS submissions
FROM responses
GROUP BY day_offset
ORDER BY day_offset;


CREATE OR REPLACE VIEW kpi_submissions_by_week AS
SELECT
    ("Submitted at"::date - (SELECT MIN("Submitted at")::date FROM responses))/7 AS week_offset,
    COUNT(*)::integer AS submissions
FROM responses
GROUP BY week_offset
ORDER BY week_offset;


