alter table orders add column status varchar(20) not null default 'NEW';
create index orders_status_idx on orders (status);
