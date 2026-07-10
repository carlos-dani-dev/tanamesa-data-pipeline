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


CREATE OR REPLACE VIEW kpi_consistency_of_access AS
SELECT
    CASE 
        WHEN "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?" = 'Sim, deixei de comer por falta de dinheiro'
         AND "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?" = 'Sim, tive medo da comida acabar'
        THEN TRUE ELSE FALSE END AS is_vag,
    "Com que frequência você consegue receber alguma refeição do programa Tá Na Mesa?" AS freq_access,
    COUNT(*) AS total
FROM responses
GROUP BY is_vag, freq_access
ORDER BY is_vag, freq_access;


DROP VIEW IF EXISTS kpi_program_dependency;
CREATE OR REPLACE VIEW kpi_program_dependency AS
SELECT
    CASE 
        WHEN "Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?" = 'Sim, deixei de comer por falta de dinheiro'
         AND "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?" = 'Sim, tive medo da comida acabar'
        THEN TRUE ELSE FALSE END AS is_vag,
    CASE
        WHEN "Sem o programa Tá Na Mesa, você continua se alimentando normalmente?" = 'Não, dependo totalmente da refeição servida pelo programa'
        AND ("Contando com a refeição distribuída pelo programa Tá Na Mesa, quantas refeições você faz por dia?" = 'Faço apenas a refeição servida pelo programa'
            OR "Contando com a refeição distribuída pelo programa Tá Na Mesa, quantas refeições você faz por dia?" = 'Faço apenas 2(duas) refeições por dia, contando com a refeição servida pelo programa')
        THEN TRUE ELSE FALSE END AS is_dependent,
    COUNT(*) AS total
FROM responses
GROUP BY is_vag, is_dependent
ORDER BY is_vag, is_dependent;


-- ==========================================
-- KPI: ASSISTED FAMILIES
-- ==========================================
CREATE OR REPLACE VIEW kpi_residence_program_serving AS
SELECT 
    "As refeições do programa Tá Na Mesa servem todas as pessoas da sua casa?" AS serving_status,
    COUNT(*) AS total
FROM responses
GROUP BY serving_status
ORDER BY serving_status;

CREATE OR REPLACE VIEW kpi_entire_served_family_configuration AS
SELECT 
    "Quantas pessoas moram com você?" AS family_size,
    COUNT(*) AS total
FROM responses
WHERE "As refeições do programa Tá Na Mesa servem todas as pessoas da sua casa?" = 'Sim, servem todas as pessoas'
GROUP BY "Quantas pessoas moram com você?"
ORDER BY "Quantas pessoas moram com você?";


CREATE OR REPLACE VIEW kpi_difficulty_of_access_by_region AS
SELECT 
    CASE 
        WHEN "Você mora na zona urbana da cidade ou na zona rural da cidade?" = 'Moro na zona urbana' THEN 'Urbana' 
        ELSE 'Rural' 
    END AS region,
    "Você sente que tipo de dificuldade para chegar ao restaurante?" AS difficulty_type,
    COUNT(*) AS total
FROM responses
GROUP BY region, difficulty_type
ORDER BY region, difficulty_type;


CREATE OR REPLACE VIEW kpi_beneficiaries_not_eating_stats AS
SELECT
    SUM(CASE WHEN "Você já esperou na fila e mesmo assim ficou sem receber a refeição?" IN ('Raramente entro na fila e não recebo a refeição', 'Frequentemente entro na fila e não recebo a refeição') THEN 0 ELSE 1 END) AS await_and_eat,
    SUM(CASE WHEN "Você já esperou na fila e mesmo assim ficou sem receber a refeição?" IN ('Raramente entro na fila e não recebo a refeição', 'Frequentemente entro na fila e não recebo a refeição') THEN 1 ELSE 0 END) AS await_and_not_eat,
    
    SUM(CASE WHEN 
        ("Nos últimos meses, você sentiu fome e não comeu por falta de dinheiro?" = 'Sim, deixei de comer por falta de dinheiro' AND "Nos últimos meses, você teve medo da comida da sua casa acabar antes de ter dinheiro para comprar mais?" = 'Sim, tive medo da comida acabar') 
        AND "Você já esperou na fila e mesmo assim ficou sem receber a refeição?" IN ('Raramente entro na fila e não recebo a refeição', 'Frequentemente entro na fila e não recebo a refeição') 
    THEN 1 ELSE 0 END) AS await_and_not_eat_on_vag
FROM responses;



CREATE OR REPLACE VIEW kpi_time_on_queue_stats AS
SELECT
    "Quanto tempo você espera na fila para receber a sua refeição?" AS queue_time,
    COUNT(*) AS total
FROM responses
GROUP BY "Quanto tempo você espera na fila para receber a sua refeição?"
ORDER BY "Quanto tempo você espera na fila para receber a sua refeição?";

CREATE OR REPLACE VIEW kpi_average_time_on_queue AS
SELECT
    (SUM(
        CASE
            WHEN "Quanto tempo você espera na fila para receber a sua refeição?" LIKE '%Não preciso%' THEN 0.25
            WHEN "Quanto tempo você espera na fila para receber a sua refeição?" LIKE '%até 30%' THEN 0.5
            WHEN "Quanto tempo você espera na fila para receber a sua refeição?" LIKE '%de 30%' THEN 0.75
            WHEN "Quanto tempo você espera na fila para receber a sua refeição?" LIKE '%de 1(uma)%' THEN 1.5
            WHEN "Quanto tempo você espera na fila para receber a sua refeição?" LIKE '%por mais de 2(duas)%' THEN 1.0
            ELSE 0
        END
    ) / NULLIF(COUNT(*), 0)) * 60 AS average_queue_time_minutes
FROM responses;


CREATE OR REPLACE VIEW kpi_restaurant_menu_summary AS
SELECT 
    'menu_change_suggestions' AS metric, 
    "Você já tentou sugerir alguma mudança ao cardápio do restaurante?" AS answer, 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'daily_menu_realization', 
    "Em que momento você descobre o cardápio que será servido no dia?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'menu_variety', 
    "As refeições ofertadas diariamente são variadas?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'menu_satisfaction', 
    "Você já deixou de comer alguma refeição do programa Tá Na Mesa por que não gostou do cardápio do dia?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'action_when_beneficiary_dislikes_food', 
    "Quando você não gosta do cardápio do dia, o que você faz com a refeição?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2;


CREATE OR REPLACE VIEW kpi_restaurant_infrastructure_summary AS
SELECT 
    'beneficiary_knows_maximum_daily_food_served' AS metric, 
    "Você sabe quantas refeições o restaurante pode servir todo dia?" AS answer, 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'payment_and_serving_separation', 
    "A pessoa que recebe o seu pagamento também entrega a sua refeição ao mesmo tempo?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'restaurant_program_signposted', 
    "O restaurante é identificado como parte do programa Tá Na Mesa?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'restaurant_cleaning', 
    "Em relação à limpeza do restaurante, qual a sua opinião?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'cold_food', 
    "Você já recebeu sua refeição fria?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'package_integrity', 
    "Você já recebeu refeições servidas em embalagens danificadas ou sujas?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'food_integrity', 
    "Você já percebeu alguma refeição estragada?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'difficulty_on_waiting', 
    "Você sente alguma dificuldade enquanto espera pela sua refeição?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2;


SELECT 
    'menu_satisfaction', 
    "Você já deixou de comer alguma refeição do programa Tá Na Mesa por que não gostou do cardápio do dia?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'action_when_beneficiary_dislikes_food', 
    "Quando você não gosta do cardápio do dia, o que você faz com a refeição?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2;

CREATE OR REPLACE VIEW kpi_program_evaluation_summary AS
SELECT 
    'food_quantity_review' AS metric, 
    "Para uma única pessoa, a quantidade de comida das refeições é suficiente?" AS answer, 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'protein_quantity_review', 
    "A quantidade de carne, frango ou peixe servida nas refeições é suficiente?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'food_flavor_review', 
    "Levando em conta todas as refeições que você já recebeu durante o programa Tá Na Mesa, como você avalia o sabor das refeições?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'program_satisfaction_review', 
    "Em relação a todo o programa Tá Na Mesa, qual o seu nível de satisfação?", 
    COUNT(*) AS total 
FROM responses GROUP BY 2

UNION ALL

SELECT 
    'program_continuity', 
    "Na sua opinião, o programa Tá Na Mesa precisa ser continuado? ", 
    COUNT(*) AS total 
FROM responses GROUP BY 2;