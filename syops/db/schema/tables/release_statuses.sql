DROP TABLE IF EXISTS public.release_statuses CASCADE;
CREATE TABLE public.release_statuses (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
