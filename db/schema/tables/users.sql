DROP TABLE IF EXISTS syops.users CASCADE;
CREATE TABLE syops.users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password CHAR(40) NOT NULL,
    insert_ts TIMESTAMPZ NOT NULL DEFAULT NOW()
);
CREATE INDEX syops_users_email ON syops.users (email, password);
