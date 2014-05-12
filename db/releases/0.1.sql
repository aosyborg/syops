BEGIN;

-- Tables
\i ../schema/tables/users.sql
\i ../schema/tables/teams.sql
\i ../schema/tables/team_users.sql
\i ../schema/tables/ssh_keys.sql
\i ../schema/tables/apps.sql

-- Inserts
\i ../schema/inserts/users.sql

-- Functions
\i ../schema/functions/set_user.sql

COMMIT;
