import argparse
import json
import pandas as pd

from scripts.utils import get_engine, insert_on_conflict_nothing

fab_cube_mapping = {
    'card': {
        'Unique ID'                   : 'unique_id',
        'Name'                        : 'name',
        'Color'                       : 'color',
        'Pitch'                       : 'pitch',
        'Cost'                        : 'cost',
        'Power'                       : 'power',
        'Defense'                     : 'defense',
        # 'Health'                      : '',
        # 'Intelligence'                : '',
        # 'Arcane'                      : '',
        'Types'                       : 'types',
        # 'Traits'                      : 'traits',
        # 'Card Keywords'               : '',
        # 'Abilities and Effects'       : '',
        # 'Ability and Effect Keywords' : '',
        # 'Granted Keywords'            : '',
        # 'Removed Keywords'            : '',
        # 'Interacts with Keywords'     : '',
        'Functional Text'             : 'functional_text',
        # 'Type Text'                   : '',
        # 'Card Played Horizontally'    : '',
        # 'Blitz Legal'                 : '',
        # 'CC Legal'                    : '',
        # 'Silver Age Legal'            : '',
        # 'Commoner Legal'              : '',
        # 'LL Legal'                    : '',
    },
    'card_printing': {
        'Unique ID': 'unique_id',
        'Card Unique ID': 'card_unique_id',
        'Card ID': 'card_id',
        'Set Printing Unique ID': 'set_printing_unique_id',
        'Set ID': 'set_id',
        'Edition': 'edition',
        'Rarity': 'rarity',
        'Foiling': 'foiling',
        'Art Variations': 'art_variations',
        'Artists': 'artists',
        'Expansion Slot': 'expansion_slot',
        'Flavor Text': 'flavor_text',
        'Image URL': 'image_url',
        'Image Rotation Degrees': 'image_rotation_degrees',
        'TCGPlayer ID': 'tcgplayer_id',
    }
}


def ingest_fab_cube_file(file=None, object_type=None, verbose=False):
    mapping_dict = fab_cube_mapping.get(object_type)
    if not mapping_dict:
        return

    df = pd.read_csv(
        file,
        usecols=mapping_dict.keys(),
        sep='\t',
    )
    df = df.rename(columns=mapping_dict).set_index('unique_id')
    list_columns = ['types', 'art_variations']
    for col in list_columns:
        if col in df.columns:
            df[col] = df[col].str.split(',').apply(json.dumps).where(df[col].notnull(), None)

    engine = get_engine()
    with engine.connect() as connection:
        df.to_sql(object_type, connection, if_exists='append', method=insert_on_conflict_nothing)


def parse_arguments():
    parser = argparse.ArgumentParser(description='ingest target fab cube file')
    parser.add_argument('-object_type', choices=['card', 'card_printing'], help='target object type to ingest')
    parser.add_argument('-input_file', help='input file path')
    parser.add_argument('-v', '--verbose', action='store_true', help='printout verbosity')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    ingest_fab_cube_file(
        file=args.input_file,
        object_type=args.object_type,
        verbose=args.verbose,
    )


if __name__ == '__main__':
    main()
