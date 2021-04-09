<!-- eliminate PSQL session connectivity -->
SELECT pid, pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = current_database() AND pid <> pg_backend_pid();
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';


<!-- dump table -->
pg_dump -U postgres -a -t contest_game_joined_users_id_seq cc_temp | psql -U postgres -d contest; 