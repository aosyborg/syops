DROP FUNCTION IF EXISTS set_team (
    i_team_id           BIGINT,
    i_name              VARCHAR(255),
    i_owner_id          BIGINT,
    i_is_organization   BOOLEAN
);
CREATE OR REPLACE FUNCTION set_team (
    i_team_id           BIGINT,
    i_name              VARCHAR(255),
    i_owner_id          BIGINT,
    i_is_organization   BOOLEAN
)
RETURNS BIGINT
SECURITY DEFINER AS
$_$
    DECLARE
        v_old public.teams;
        v_id BIGINT;
    BEGIN
        -- Check if organization already exists
        IF i_team_id IS NULL AND i_is_organization IS True THEN
            SELECT * INTO v_old FROM teams WHERE name = i_name AND is_organization = True;
            IF v_old.id IS NOT NULL THEN
                INSERT INTO team_users (
                    team_id,
                    user_id
                ) VALUES (
                    v_old.id,
                    i_owner_id
                );
                return v_old.id;
            END IF;
        END IF;

        -- Standard team update/insert
        SELECT * INTO v_old FROM teams WHERE id = i_team_id;
        IF v_old.id IS NULL THEN
            INSERT INTO teams (
                user_id,
                name,
                is_organization
            ) VALUES (
                i_owner_id,
                i_name,
                COALESCE(i_is_organization, False)
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
                name = COALESCE(i_name, name),
                is_organization = COALESCE(i_is_organization, is_organization)
            WHERE
                id = i_team_id;

            v_id := v_old.id;
        END IF;

        RETURN v_id;
    END;
$_$
LANGUAGE PLPGSQL;
