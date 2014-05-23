DROP TABLE IF EXISTS public.teams CASCADE;
CREATE TABLE public.teams (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES public.users (id),
    name VARCHAR(255),
    is_organization BOOLEAN NOT NULL DEFAULT False,
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
