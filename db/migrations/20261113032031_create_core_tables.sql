-- migrate:up


-- Reef sites, loaded from data/sites/sites.csv (ADR-020).
CREATE TABLE sites (
    id        smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slug      text NOT NULL UNIQUE,
    name      text NOT NULL,
    coast     text NOT NULL CHECK (coast IN ('pacific', 'caribbean', 'oceanic')),
    longitude numeric(8, 4) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    latitude  numeric(7, 4) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    active    boolean NOT NULL DEFAULT true,
    note      text NOT NULL DEFAULT ''
);

-- NOAA 0.05 degree cells, stored by their center (always ends in .x25 or .x75).
CREATE TABLE cells (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    longitude numeric(7, 3) NOT NULL CHECK (abs(longitude * 1000) % 50 = 25),
    latitude  numeric(6, 3) NOT NULL CHECK (abs(latitude * 1000) % 50 = 25),
    UNIQUE (longitude, latitude),
    CHECK (longitude BETWEEN -179.975 AND 179.975),
    CHECK (latitude BETWEEN -89.975 AND 89.975)
);

-- Which cells describe each site (ADR-020, ADR-022).
CREATE TABLE site_cells (
    site_id smallint NOT NULL REFERENCES sites (id),
    cell_id integer  NOT NULL REFERENCES cells (id),
    PRIMARY KEY (site_id, cell_id)
);

-- One record per ingestion run (RF-2, ADR-021).
CREATE TABLE ingestion_runs (
    id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    started_at   timestamptz NOT NULL DEFAULT now(),
    finished_at  timestamptz,
    source_url   text NOT NULL,
    rows_written integer NOT NULL DEFAULT 0 CHECK (rows_written >= 0),
    status       text NOT NULL DEFAULT 'running'
                 CHECK (status IN ('running', 'succeeded', 'failed')),
    error        text,
    CHECK ((status = 'running') = (finished_at IS NULL)),
    CHECK (finished_at >= started_at),
    CHECK (status <> 'failed' OR error IS NOT NULL)
);

-- Daily NOAA values per cell, as published (ADR-021, ADR-022).
-- A value is NULL when NOAA has no data for that cell and day.
CREATE TABLE cell_observations (
    cell_id     integer NOT NULL REFERENCES cells (id),
    date        date    NOT NULL,
    sst         numeric(5, 2) CHECK (sst BETWEEN -2 AND 50),
    anomaly     numeric(5, 2) CHECK (anomaly BETWEEN -15 AND 15),
    hotspot     numeric(5, 2) CHECK (hotspot BETWEEN -15 AND 15),
    dhw         numeric(5, 2) CHECK (dhw BETWEEN 0 AND 100),
    crw_baa     smallint CHECK (crw_baa BETWEEN 0 AND 4),
    alert_level smallint CHECK (alert_level BETWEEN 0 AND 7),
    run_id      bigint  NOT NULL REFERENCES ingestion_runs (id),
    PRIMARY KEY (cell_id, date)
);

-- One row per site and day, taken whole from its most stressed cell (ADR-022).
CREATE VIEW site_observations AS
SELECT DISTINCT ON (sc.site_id, o.date)
    sc.site_id,
    o.date,
    o.cell_id,
    o.sst,
    o.anomaly,
    o.hotspot,
    o.dhw,
    o.crw_baa,
    o.alert_level
FROM site_cells AS sc
JOIN cell_observations AS o ON o.cell_id = sc.cell_id
ORDER BY
    sc.site_id,
    o.date,
    o.alert_level DESC NULLS LAST,
    o.dhw DESC NULLS LAST,
    o.hotspot DESC NULLS LAST,
    o.cell_id;

REVOKE ALL ON schema_migrations FROM atalaya_ingest, atalaya_api;

-- migrate:down

DROP VIEW site_observations;
DROP TABLE cell_observations;
DROP TABLE ingestion_runs;
DROP TABLE site_cells;
DROP TABLE cells;
DROP TABLE sites;