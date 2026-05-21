CREATE TABLE IF NOT EXISTS card_printing
(
    unique_id varchar(32) PRIMARY KEY,
    card_unique_id varchar(32) REFERENCES card (unique_id),
    card_id varchar(8),
    set_printing_unique_id varchar(32),
    set_id varchar(8),
    edition char(1),
    rarity char(1),
    foiling char(1),
    art_variations json,
    artists varchar(64),
    expansion_slot bool NOT NULL DEFAULT FALSE,
    flavor_text varchar(512),
    image_url varchar(256),
    image_rotation_degrees double precision,
    tcgplayer_id double precision
);