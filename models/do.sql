-- v1403 == == == ==
/*
 ALTER TABLE device_logs
 ADD COLUMN IF NOT EXISTS detail varchar;
 ALTER TABLE device
 ADD COLUMN IF NOT EXISTS device_key varchar;
 ALTER TABLE device
 ADD COLUMN IF NOT EXISTS status varchar;
 drop table customer_transactions;
 drop table customer_account;
 drop table customer;
 */
-- v2003
update public.user set status = upper(status), role = upper(role);
alter table public.user add column if not exists created_by int;
update public.user set created_by = 1;
truncate table customer cascade;
truncate table customer_account cascade;
-- $ pip3 install pyyaml
-- set db params in conf/dbconn.yaml
ALTER TABLE customer_account
ADD COLUMN IF NOT EXISTS account_type varchar;
ALTER TABLE customer_account
ADD COLUMN IF NOT EXISTS facility_id int;
alter table settings
ADD COLUMN IF NOT EXISTS ten_id int;
alter table public.user
ADD COLUMN IF NOT EXISTS ten_id int;
alter table user_logs
ADD COLUMN IF NOT EXISTS ten_id int;
alter table customer
ADD COLUMN IF NOT EXISTS ten_id int;
alter table customer
ADD COLUMN IF NOT EXISTS avatar varchar;
alter table customer_account
ADD COLUMN IF NOT EXISTS ten_id int;
alter table customer_transactions
ADD COLUMN IF NOT EXISTS ten_id int;
alter table customer_transactions
ADD COLUMN IF NOT EXISTS drcr varchar;
alter table customer_transactions
ADD COLUMN IF NOT EXISTS balance float;
alter table device
ADD COLUMN IF NOT EXISTS ten_id int;
alter table device_logs
ADD COLUMN IF NOT EXISTS ten_id int;
--=========================================
update customer
set ten_id = 1;
update customer_account
set ten_id = 1;
update customer_transactions
set ten_id = 1;
update device
set ten_id = 1;
update device_logs
set ten_id = 1;
update settings
set ten_id = 1;
update public.user
set ten_id = 1;
ALTER TABLE customer_account
ALTER COLUMN balance TYPE Float;
ALTER TABLE customer_account
ALTER COLUMN last_transaction_amount TYPE Float;
ALTER TABLE customer_transactions
ALTER COLUMN balance TYPE Float;
ALTER TABLE customer_transactions
ALTER COLUMN amount TYPE Float;
ALTER TABLE device_logs
ALTER COLUMN amount TYPE Float;
ALTER TABLE device_logs
ALTER COLUMN volume TYPE Float;
ALTER TABLE device_logs
ALTER COLUMN topup TYPE Float;
-- ==========================================================
ALTER TABLE device
ADD COLUMN IF NOT EXISTS customer_account_id integer,
ADD CONSTRAINT fk_customer_account foreign key(customer_account_id) references customer_account(id);
alter table settings drop constraint settings_phrase_key;
alter table settings
add constraint uq_settings_phrase unique(phrase, ten_id);
alter table tennants
add column config varchar;