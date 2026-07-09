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


CREATE OR REPLACE VIEW kpi_submissions_by_city AS
SELECT
    "Selecione o seu município" AS city,
    COUNT(*)::integer AS submissions
FROM responses
GROUP BY city
ORDER BY city;


CREATE OR REPLACE VIEW kpi_beneficiaries_socioechonomics_stats AS
SELECT

    SUM(
        CASE WHEN "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?" = 'Sim, deixei de comer por falta de dinheiro'
        AND "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?" = 'Sim, tive medo da comida acabar'
        THEN 1 ELSE 0 END
    ) AS beneficiaries_on_vag,
    
    SUM(
        CASE WHEN "Você é inscrito no programa CadÚnico?" = 'Sim, sou inscrito' THEN 1 ELSE 0 END
    ) AS beneficiaries_on_cadunico,

    SUM(
        CASE WHEN "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?" = 'Sim, deixei de comer por falta de dinheiro'
        AND "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?" = 'Sim, tive medo da comida acabar'
        AND "Você é inscrito no programa CadÚnico?" = 'Sim, sou inscrito'
        THEN 1 ELSE 0 END
    ) AS beneficiaries_on_cadunico_on_vag
FROM responses;