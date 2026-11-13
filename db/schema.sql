\restrict dbmate

-- Dumped from database version 18.6 (Debian 18.6-1.pgdg12+2)
-- Dumped by pg_dump version 18.6 (Ubuntu 18.6-1.pgdg26.04+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: atalaya; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA atalaya;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cell_observations; Type: TABLE; Schema: atalaya; Owner: -
--

CREATE TABLE atalaya.cell_observations (
    cell_id integer NOT NULL,
    date date NOT NULL,
    sst numeric(5,2),
    anomaly numeric(5,2),
    hotspot numeric(5,2),
    dhw numeric(5,2),
    crw_baa smallint,
    alert_level smallint,
    run_id bigint NOT NULL,
    CONSTRAINT cell_observations_alert_level_check CHECK (((alert_level >= 0) AND (alert_level <= 7))),
    CONSTRAINT cell_observations_anomaly_check CHECK (((anomaly >= ('-15'::integer)::numeric) AND (anomaly <= (15)::numeric))),
    CONSTRAINT cell_observations_crw_baa_check CHECK (((crw_baa >= 0) AND (crw_baa <= 4))),
    CONSTRAINT cell_observations_dhw_check CHECK (((dhw >= (0)::numeric) AND (dhw <= (100)::numeric))),
    CONSTRAINT cell_observations_hotspot_check CHECK (((hotspot >= ('-15'::integer)::numeric) AND (hotspot <= (15)::numeric))),
    CONSTRAINT cell_observations_sst_check CHECK (((sst >= ('-2'::integer)::numeric) AND (sst <= (50)::numeric)))
);


--
-- Name: cells; Type: TABLE; Schema: atalaya; Owner: -
--

CREATE TABLE atalaya.cells (
    id integer NOT NULL,
    longitude numeric(7,3) NOT NULL,
    latitude numeric(6,3) NOT NULL,
    CONSTRAINT cells_latitude_check CHECK (((abs((latitude * (1000)::numeric)) % (50)::numeric) = (25)::numeric)),
    CONSTRAINT cells_latitude_check1 CHECK (((latitude >= '-89.975'::numeric) AND (latitude <= 89.975))),
    CONSTRAINT cells_longitude_check CHECK (((abs((longitude * (1000)::numeric)) % (50)::numeric) = (25)::numeric)),
    CONSTRAINT cells_longitude_check1 CHECK (((longitude >= '-179.975'::numeric) AND (longitude <= 179.975)))
);


--
-- Name: cells_id_seq; Type: SEQUENCE; Schema: atalaya; Owner: -
--

ALTER TABLE atalaya.cells ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME atalaya.cells_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ingestion_runs; Type: TABLE; Schema: atalaya; Owner: -
--

CREATE TABLE atalaya.ingestion_runs (
    id bigint NOT NULL,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    finished_at timestamp with time zone,
    source_url text NOT NULL,
    rows_written integer DEFAULT 0 NOT NULL,
    status text DEFAULT 'running'::text NOT NULL,
    error text,
    CONSTRAINT ingestion_runs_check CHECK (((status = 'running'::text) = (finished_at IS NULL))),
    CONSTRAINT ingestion_runs_check1 CHECK ((finished_at >= started_at)),
    CONSTRAINT ingestion_runs_check2 CHECK (((status <> 'failed'::text) OR (error IS NOT NULL))),
    CONSTRAINT ingestion_runs_rows_written_check CHECK ((rows_written >= 0)),
    CONSTRAINT ingestion_runs_status_check CHECK ((status = ANY (ARRAY['running'::text, 'succeeded'::text, 'failed'::text])))
);


--
-- Name: ingestion_runs_id_seq; Type: SEQUENCE; Schema: atalaya; Owner: -
--

ALTER TABLE atalaya.ingestion_runs ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME atalaya.ingestion_runs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: schema_migrations; Type: TABLE; Schema: atalaya; Owner: -
--

CREATE TABLE atalaya.schema_migrations (
    version character varying NOT NULL
);


--
-- Name: site_cells; Type: TABLE; Schema: atalaya; Owner: -
--

CREATE TABLE atalaya.site_cells (
    site_id smallint NOT NULL,
    cell_id integer NOT NULL
);


--
-- Name: site_observations; Type: VIEW; Schema: atalaya; Owner: -
--

CREATE VIEW atalaya.site_observations AS
 SELECT DISTINCT ON (sc.site_id, o.date) sc.site_id,
    o.date,
    o.cell_id,
    o.sst,
    o.anomaly,
    o.hotspot,
    o.dhw,
    o.crw_baa,
    o.alert_level
   FROM (atalaya.site_cells sc
     JOIN atalaya.cell_observations o ON ((o.cell_id = sc.cell_id)))
  ORDER BY sc.site_id, o.date, o.alert_level DESC NULLS LAST, o.dhw DESC NULLS LAST, o.hotspot DESC NULLS LAST, o.cell_id;


--
-- Name: sites; Type: TABLE; Schema: atalaya; Owner: -
--

CREATE TABLE atalaya.sites (
    id smallint NOT NULL,
    slug text NOT NULL,
    name text NOT NULL,
    coast text NOT NULL,
    longitude numeric(8,4) NOT NULL,
    latitude numeric(7,4) NOT NULL,
    active boolean DEFAULT true NOT NULL,
    note text DEFAULT ''::text NOT NULL,
    CONSTRAINT sites_coast_check CHECK ((coast = ANY (ARRAY['pacific'::text, 'caribbean'::text, 'oceanic'::text]))),
    CONSTRAINT sites_latitude_check CHECK (((latitude >= ('-90'::integer)::numeric) AND (latitude <= (90)::numeric))),
    CONSTRAINT sites_longitude_check CHECK (((longitude >= ('-180'::integer)::numeric) AND (longitude <= (180)::numeric)))
);


--
-- Name: sites_id_seq; Type: SEQUENCE; Schema: atalaya; Owner: -
--

ALTER TABLE atalaya.sites ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME atalaya.sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cell_observations cell_observations_pkey; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.cell_observations
    ADD CONSTRAINT cell_observations_pkey PRIMARY KEY (cell_id, date);


--
-- Name: cells cells_longitude_latitude_key; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.cells
    ADD CONSTRAINT cells_longitude_latitude_key UNIQUE (longitude, latitude);


--
-- Name: cells cells_pkey; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.cells
    ADD CONSTRAINT cells_pkey PRIMARY KEY (id);


--
-- Name: ingestion_runs ingestion_runs_pkey; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.ingestion_runs
    ADD CONSTRAINT ingestion_runs_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: site_cells site_cells_pkey; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.site_cells
    ADD CONSTRAINT site_cells_pkey PRIMARY KEY (site_id, cell_id);


--
-- Name: sites sites_pkey; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (id);


--
-- Name: sites sites_slug_key; Type: CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.sites
    ADD CONSTRAINT sites_slug_key UNIQUE (slug);


--
-- Name: cell_observations cell_observations_cell_id_fkey; Type: FK CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.cell_observations
    ADD CONSTRAINT cell_observations_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES atalaya.cells(id);


--
-- Name: cell_observations cell_observations_run_id_fkey; Type: FK CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.cell_observations
    ADD CONSTRAINT cell_observations_run_id_fkey FOREIGN KEY (run_id) REFERENCES atalaya.ingestion_runs(id);


--
-- Name: site_cells site_cells_cell_id_fkey; Type: FK CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.site_cells
    ADD CONSTRAINT site_cells_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES atalaya.cells(id);


--
-- Name: site_cells site_cells_site_id_fkey; Type: FK CONSTRAINT; Schema: atalaya; Owner: -
--

ALTER TABLE ONLY atalaya.site_cells
    ADD CONSTRAINT site_cells_site_id_fkey FOREIGN KEY (site_id) REFERENCES atalaya.sites(id);


--
-- PostgreSQL database dump complete
--

\unrestrict dbmate


--
-- Dbmate schema migrations
--

INSERT INTO atalaya.schema_migrations (version) VALUES
    ('20261113032031');
