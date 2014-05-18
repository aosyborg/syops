DROP TABLE IF EXISTS public.ssh_keys CASCADE;
CREATE TABLE public.ssh_keys (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES public.users (id) ON DELETE CASCADE,
    key TEXT,
    last_used TIMESTAMPTZ,
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
