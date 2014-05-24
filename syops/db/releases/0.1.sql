BEGIN;

-- Tables
\i ../schema/tables/users.sql
\i ../schema/tables/teams.sql
\i ../schema/tables/team_users.sql
\i ../schema/tables/apps.sql
\i ../schema/tables/release_statuses.sql
\i ../schema/tables/releases.sql

-- Inserts
\i ../schema/inserts/release_statuses.sql

-- Functions
\i ../schema/functions/set_user.sql
\i ../schema/functions/set_team.sql
\i ../schema/functions/set_app.sql
\i ../schema/functions/set_release.sql

COMMIT;
