drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	hash text not null,
	url text not null
);
