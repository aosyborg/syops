DROP FUNCTION IF EXISTS set_user (
    i_user_id           BIGINT,
    i_email             VARCHAR(255),
    i_password          CHAR(40),
    i_name              VARCHAR(255),
    i_is_admin          BOOLEAN
);
CREATE OR REPLACE FUNCTION set_user (
    i_user_id           BIGINT,
    i_email             VARCHAR(255),
    i_password          CHAR(40),
    i_name              VARCHAR(255),
    i_is_admin          BOOLEAN
)
RETURNS BIGINT
SECURITY DEFINER AS
$_$
    DECLARE
        v_old public.users;
        v_id BIGINT;
    BEGIN
        SELECT * INTO v_old FROM users WHERE id = i_user_id;
        IF v_old.id IS NULL THEN
            INSERT INTO users (
                email,
                password,
                name,
                is_admin
            ) VALUES (
                lower(i_email),
                i_password,
                i_name,
                COALESCE(i_is_admin, False)
            );
            v_id := CURRVAL('public.users_id_seq');
        ELSE
            UPDATE users SET
                email = COALESCE(lower(i_email), email),
                password = COALESCE(i_password, password),
                name = COALESCE(i_name, name),
                is_admin = COALESCE(i_is_admin, is_admin)
            WHERE
                id = i_user_id;

            v_id := v_old.id;
        END IF;

        RETURN v_id;
    END;
$_$
LANGUAGE PLPGSQL;
