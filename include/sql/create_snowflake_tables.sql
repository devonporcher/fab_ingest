CREATE TABLE IF NOT EXISTS FAB.CARDS.CARD
(
    unique_id varchar(32) PRIMARY KEY,
    name varchar(64) NOT NULL,
    color varchar(16),
    pitch double precision,
    cost varchar(8),
    power varchar(8),
    defense varchar(8),
    types array,
    functional_text varchar(1024)
);

CREATE TABLE IF NOT EXISTS FAB.CARDS.CARD_PRINTING
(
    unique_id varchar(32) PRIMARY KEY,
    card_unique_id varchar(32) REFERENCES card (unique_id),
    card_id varchar(8),
    set_printing_unique_id varchar(32),
    set_id varchar(8),
    edition char(1),
    rarity char(1),
    foiling char(1),
    art_variations array,
    artists varchar(64),
    expansion_slot boolean NOT NULL DEFAULT FALSE,
    flavor_text varchar(512),
    image_url varchar(256),
    image_rotation_degrees double precision,
    tcgplayer_id double precision
);

CREATE TABLE IF NOT EXISTS FAB.CARDS.PRICE_HISTORY
(
    tcgplayer_id double precision NOT NULL,
    foiling char(1) NOT NULL,
    condition varchar(32) NOT NULL,
    snapshot_date date NOT NULL,
    price decimal(10,2),
    PRIMARY KEY (tcgplayer_id, foiling, condition, snapshot_date)
);