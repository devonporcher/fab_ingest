CREATE TABLE IF NOT EXISTS price_history
(
	tcgplayer_id double precision NOT NULL,
	foiling char(1) NOT NULL,
	condition varchar(32) NOT NULL,
	snapshot_date date NOT NULL,
	price decimal(10,2),
	PRIMARY KEY (tcgplayer_id, foiling, condition, snapshot_date)
);