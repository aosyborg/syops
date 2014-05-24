DROP FUNCTION IF EXISTS set_app (
    i_app_id                BIGINT,
    i_team_id               BIGINT,
    i_name                  VARCHAR(255),
    i_clone_url             VARCHAR(255),
    i_github_owner          VARCHAR(255),
    i_github_repo           VARCHAR(255),
    i_doc_url               VARCHAR(255),
    i_build_instructions    TEXT
);
CREATE OR REPLACE FUNCTION set_app (
    i_app_id                BIGINT,
    i_team_id               BIGINT,
    i_name                  VARCHAR(255),
    i_clone_url             VARCHAR(255),
    i_github_owner          VARCHAR(255),
    i_github_repo           VARCHAR(255),
    i_doc_url               VARCHAR(255),
    i_build_instructions    TEXT
)
RETURNS BIGINT
SECURITY DEFINER AS
$_$
    DECLARE
        v_old public.apps;
        v_id BIGINT;
    BEGIN
        SELECT * INTO v_old FROM apps WHERE id = i_app_id;
        IF v_old.id IS NULL THEN
            INSERT INTO apps (
                team_id,
                name,
                clone_url,
                github_owner,
                github_repo,
                doc_url,
                build_instructions
            ) VALUES (
                i_team_id,
                i_name,
                i_clone_url,
                i_github_owner,
                i_github_repo,
                i_doc_url,
                i_build_instructions
            );
            v_id := CURRVAL('public.apps_id_seq');
        ELSE
            UPDATE apps SET
                team_id = COALESCE(i_team_id, team_id),
                name = COALESCE(i_name, name),
                clone_url = COALESCE(i_clone_url, clone_url),
                github_owner = COALESCE(i_github_owner, github_owner),
                github_repo = COALESCE(i_github_repo, github_repo),
                doc_url = COALESCE(i_doc_url, doc_url),
                build_instructions = COALESCE(i_build_instructions, build_instructions)
            WHERE
                id = i_app_id;

            v_id := v_old.id;
        END IF;

        RETURN v_id;
    END;
$_$
LANGUAGE PLPGSQL;
