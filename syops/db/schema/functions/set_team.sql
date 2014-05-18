DROP FUNCTION IF EXISTS set_team (
    i_team_id           BIGINT,
    i_name              VARCHAR(255),
    i_owner_id          BIGINT
);
CREATE OR REPLACE FUNCTION set_team (
    i_team_id           BIGINT,
    i_name              VARCHAR(255),
    i_owner_id          BIGINT
)
RETURNS BIGINT
SECURITY DEFINER AS
$_$
    DECLARE
        v_old public.teams;
        v_id BIGINT;
    BEGIN
        SELECT * INTO v_old FROM teams WHERE id = i_team_id;
        IF v_old.id IS NULL THEN
            INSERT INTO teams (
                user_id,
                name
            ) VALUES (
                i_owner_id,
                i_name
            );
            v_id := CURRVAL('public.teams_id_seq');
            INSERT INTO team_users (
                team_id,
                user_id
            ) VALUES (
                v_id,
                i_owner_id
            );
            v_id := CURRVAL('public.teams_id_seq');
        ELSE
            UPDATE teams SET
                user_id = COALESCE(i_owner_id, user_id),
                name = COALESCE(i_name, name)
            WHERE
                id = i_team_id;

            v_id := v_old.id;
        END IF;

        RETURN v_id;
    END;
$_$
LANGUAGE PLPGSQL;
