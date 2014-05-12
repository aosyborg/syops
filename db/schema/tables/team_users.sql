DROP TABLE IF EXISTS public.team_users CASCADE;
CREATE TABLE public.team_users (
    team_id BIGINT NOT NULL REFERENCES public.teams (id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES public.users (id),
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX syops_team_users_team_user ON public.team_users (team_id, user_id);
