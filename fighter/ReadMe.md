<!-- eliminate PSQL session connectivity -->
SELECT pid, pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = current_database() AND pid <> pg_backend_pid();
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';


psql -d cc_temp -f contest.sql
<!-- dump table -->
pg_dump -U postgres -a -t socialaccount_socialtoken cc_temp | psql -U postgres -d contest; 

<!-- migration order -->
contest_chatfile
contest_chatroom
contest_customuser
contest_customuser_groups
contest_customuser_user_permissions
contest_faq
contest_fighter
contest_event
contest_bout
contest_chatmessage
contest_role
contest_customuser_roles
contest_ticket
contest_notification
contest_game
contest_game_bouts
contest_game_entrants
contest_game_joined_users
contest_entry
contest_selection
account_emailaddress
account_emailconfirmation
auth_group
auth_group_permissions
socialaccount_socialaccount
socialaccount_socialapp
socialaccount_socialapp_sites
socialaccount_socialtoken