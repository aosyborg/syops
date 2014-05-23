DROP TABLE IF EXISTS public.releases CASCADE;
CREATE TABLE public.releases (
    id BIGSERIAL PRIMARY KEY,
    app_id BIGINT NOT NULL REFERENCES public.apps (id) ON DELETE CASCADE,
    release_status_id INTEGER NOT NULL REFERENCES public.release_statuses (id),
    version VARCHAR(255) NOT NULL,
    tagged_branch VARCHAR(255) NOT NULL,
    description TEXT,
    build_output TEXT,
    update_ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
