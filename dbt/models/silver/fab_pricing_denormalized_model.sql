{{ config(materialized='table') }}

WITH price_history_denormalized as (
    SELECT
        ph.tcgplayer_id,
        ph.foiling,
        ph.condition,
        ph.snapshot_date,
        ph.price,
        cp.unique_id AS card_printing_unique_id,
        cp.card_id,
        cp.set_printing_unique_id,
        cp.set_id,
        cp.edition,
        cp.rarity,
        cp.art_variations,
        cp.artists,
        cp.expansion_slot,
        cp.flavor_text,
        cp.image_url,
        cp.image_rotation_degrees,
        c.unique_id AS card_unique_id,
        c.name,
        c.color,
        c.pitch,
        c.cost,
        c.power,
        c.defense,
        c.types,
        c.functional_text
    FROM FAB.CARDS.PRICE_HISTORY AS ph
    INNER JOIN FAB.CARDS.CARD_PRINTING AS cp
        ON ph.tcgplayer_id = cp.tcgplayer_id AND ph.foiling = cp.foiling
    INNER JOIN FAB.CARDS.CARD AS c
        ON cp.card_unique_id = c.unique_id

)

SELECT *
FROM price_history_denormalized

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
