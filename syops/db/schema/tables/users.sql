DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE public.users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    access_token VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255) NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    insert_ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX syops_users_email ON public.users (email);
