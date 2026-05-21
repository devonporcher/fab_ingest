CREATE TABLE IF NOT EXISTS card
(
    unique_id varchar(32) PRIMARY KEY,
    name varchar(64) NOT NULL,
    color varchar(16),
    pitch double precision,
    cost varchar(8),
    power varchar(8),
    defense varchar(8),
    types json,
    functional_text varchar(1024)
);