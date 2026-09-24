-- =========================================================
-- Vaccination Data Analytics
-- MySQL Database Setup and Analysis
-- =========================================================

CREATE DATABASE IF NOT EXISTS vaccination_analytics;

USE vaccination_analytics;


-- =========================================================
-- 1. Coverage Table
-- =========================================================

CREATE TABLE IF NOT EXISTS coverage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_group VARCHAR(100),
    country_code VARCHAR(20),
    country_name VARCHAR(150),
    year INT,
    antigen VARCHAR(100),
    antigen_description TEXT,
    coverage_category VARCHAR(100),
    coverage_category_description TEXT,
    target_number BIGINT,
    doses BIGINT,
    coverage DECIMAL(6,2)
);


-- =========================================================
-- 2. Incidence Rate Table
-- =========================================================

CREATE TABLE IF NOT EXISTS incidence_rate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(150),
    year INT,
    disease VARCHAR(150),
    disease_description TEXT,
    denominator BIGINT,
    incidence_rate DECIMAL(15,4),
    country_group VARCHAR(100),
    country_code VARCHAR(20)
);


-- =========================================================
-- 3. Reported Cases Table
-- =========================================================

CREATE TABLE IF NOT EXISTS reported_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(150),
    year INT,
    disease VARCHAR(150),
    disease_description TEXT,
    cases BIGINT,
    country_group VARCHAR(100),
    country_code VARCHAR(20)
);


-- =========================================================
-- 4. Vaccine Introduction Table
-- =========================================================

CREATE TABLE IF NOT EXISTS vaccine_introduction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso_country_code VARCHAR(20),
    country VARCHAR(150),
    who_region VARCHAR(100),
    year INT,
    vaccine_description TEXT,
    introduction_status VARCHAR(100)
);


-- =========================================================
-- 5. Vaccine Schedule Table
-- =========================================================

CREATE TABLE IF NOT EXISTS vaccine_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso_3_code VARCHAR(20),
    country VARCHAR(150),
    who_region VARCHAR(100),
    year INT,
    vaccine_code VARCHAR(50),
    vaccine_description TEXT,
    schedule_rounds DECIMAL(10,2),
    target_pop VARCHAR(100),
    target_pop_description TEXT,
    geographic_area TEXT,
    age_administered VARCHAR(100),
    source_comment TEXT
);


-- =========================================================
-- 6. Indexes for Faster Analysis
-- =========================================================

CREATE INDEX idx_coverage_country_year
ON coverage(country_code, year);

CREATE INDEX idx_incidence_country_year
ON incidence_rate(country_code, year);

CREATE INDEX idx_cases_country_year
ON reported_cases(country_code, year);

CREATE INDEX idx_introduction_country_year
ON vaccine_introduction(iso_country_code, year);

CREATE INDEX idx_schedule_country_year
ON vaccine_schedule(iso_3_code, year);


-- =========================================================
-- 7. Summary Views
-- =========================================================

CREATE OR REPLACE VIEW vw_coverage_summary AS
SELECT
    country_code,
    country_name,
    year,
    antigen,
    coverage_category,
    coverage
FROM coverage
WHERE coverage IS NOT NULL;


CREATE OR REPLACE VIEW vw_incidence_summary AS
SELECT
    country_code,
    country,
    year,
    disease,
    disease_description,
    incidence_rate
FROM incidence_rate
WHERE incidence_rate IS NOT NULL;


CREATE OR REPLACE VIEW vw_reported_cases_summary AS
SELECT
    country_code,
    country,
    year,
    disease,
    disease_description,
    cases
FROM reported_cases
WHERE cases IS NOT NULL;


CREATE OR REPLACE VIEW vw_vaccine_introduction_summary AS
SELECT
    iso_country_code,
    country,
    who_region,
    year,
    vaccine_description,
    introduction_status
FROM vaccine_introduction;


CREATE OR REPLACE VIEW vw_vaccine_schedule_summary AS
SELECT
    iso_3_code,
    country,
    who_region,
    year,
    vaccine_code,
    vaccine_description,
    schedule_rounds,
    target_pop,
    target_pop_description,
    geographic_area,
    age_administered,
    source_comment
FROM vaccine_schedule;


-- =========================================================
-- 8. Basic Verification Queries
-- =========================================================

SELECT COUNT(*) AS coverage_records
FROM coverage;

SELECT COUNT(*) AS incidence_records
FROM incidence_rate;

SELECT COUNT(*) AS reported_cases_records
FROM reported_cases;

SELECT COUNT(*) AS vaccine_introduction_records
FROM vaccine_introduction;

SELECT COUNT(*) AS vaccine_schedule_records
FROM vaccine_schedule;