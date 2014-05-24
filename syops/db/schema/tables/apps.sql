DROP TABLE IF EXISTS public.apps CASCADE;
CREATE TABLE public.apps (
    id BIGSERIAL PRIMARY KEY,
    team_id BIGINT NOT NULL REFERENCES public.teams (id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    clone_url VARCHAR(255) NOT NULL,
    github_owner VARCHAR(255) NOT NULL,
    github_repo VARCHAR(255) NOT NULL,
    doc_url VARCHAR(255),
    build_instructions TEXT,
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
