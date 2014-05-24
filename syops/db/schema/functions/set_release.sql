DROP FUNCTION IF EXISTS set_release (
    i_id                    BIGINT,
    i_app_id                BIGINT,
    i_release_status_id     INTEGER,
    i_version               VARCHAR,
    i_tagged_branch         VARCHAR,
    i_description           TEXT,
    i_build_output          TEXT
);
CREATE OR REPLACE FUNCTION set_release (
    i_id                    BIGINT,
    i_app_id                BIGINT,
    i_release_status_id     INTEGER,
    i_version               VARCHAR,
    i_tagged_branch         VARCHAR,
    i_description           TEXT,
    i_build_output          TEXT
)
RETURNS BIGINT
SECURITY DEFINER AS
$_$
    DECLARE
        v_old public.releases;
        v_id BIGINT;
    BEGIN
        SELECT * INTO v_old FROM releases WHERE id = i_id;
        IF v_old.id IS NULL THEN
            INSERT INTO releases (
                app_id,
                release_status_id,
                version,
                tagged_branch,
                description,
                build_output
            ) VALUES (
                i_app_id,
                i_release_status_id,
                i_version,
                i_tagged_branch,
                i_description,
                i_build_output
            );
            v_id := CURRVAL('public.releases_id_seq');
        ELSE
            UPDATE releases SET
                app_id = COALESCE(i_app_id, app_id),
                release_status_id = COALESCE(i_release_status_id, release_status_id),
                version = COALESCE(i_version, version),
                tagged_branch = COALESCE(i_tagged_branch, tagged_branch),
                description = COALESCE(i_description, description),
                build_output = COALESCE(i_build_output, build_output),
                update_ts = NOW()
            WHERE
                id = i_id;

            v_id := v_old.id;
        END IF;

        RETURN v_id;
    END;
$_$
LANGUAGE PLPGSQL;
