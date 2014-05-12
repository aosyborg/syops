DROP TABLE IF EXISTS public.teams CASCADE;
CREATE TABLE public.teams (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES public.users (id),
    name VARCHAR(255),
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
