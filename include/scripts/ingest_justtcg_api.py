import argparse
# from dotenv import load_dotenv
import json
import os
import pandas as pd
from psycopg2.extras import execute_values
import requests
from requests.adapters import HTTPAdapter, Retry
import sys

from scripts.utils import get_engine

# dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
# load_dotenv(dotenv_path)


justtcg_printing_mapping = {
    'S': 'Normal',
    'R': 'Rainbow Foil',
    'C': 'Cold Foil',
}

justtcg_printing_inv_mapping = {
    v: k for k, v in justtcg_printing_mapping.items()
}


def get_insert_list_from_body(response_body=None):
    ret_val = []
    for card in response_body['data']:
        for v in card['variants']:
            for ph in v['priceHistory']:
                insert_dict = {
                    'tcgplayer_id': card['tcgplayerId'],
                    'foiling': justtcg_printing_inv_mapping.get(v['printing'], None),
                    'condition': v['condition'],
                    'snapshot_date': pd.to_datetime(ph['t'], unit='s').date(),
                    'price': ph['p'],
                }
                ret_val.append(insert_dict)
    return ret_val


def ingest_justtcg_api(verbose=False):
    engine = get_engine()
    with engine.raw_connection() as connection:
    # with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
            WITH cp_rr AS (
                SELECT
                    *,
                    CASE
                        WHEN cp.foiling = 'S' THEN 0
                        WHEN cp.foiling = 'R' THEN 1
                        WHEN cp.foiling = 'C' THEN 2
                        WHEN cp.foiling = 'G' THEN 3
                    ELSE
                        4
                    END AS rarity_rank
                FROM card_printing AS cp
            )

            SELECT DISTINCT
                cp_rr.tcgplayer_id,
                cp_rr.foiling
            FROM cp_rr
            WHERE
                cp_rr.rarity in ('M', 'L', 'F') AND
                (cp_rr.card_id, cp_rr.rarity_rank) IN (
                    SELECT
                        cp_rr.card_id,
                        MIN(cp_rr.rarity_rank)
                    FROM cp_rr
                    GROUP BY cp_rr.card_id
                ) AND
                (cp_rr.tcgplayer_id, cp_rr.foiling) NOT IN (
                    SELECT DISTINCT
                        ph.tcgplayer_id,
                        ph.foiling
                    FROM price_history AS ph
                ) AND
                cp_rr.set_id IN ('SEA', 'SUP', 'PEN', 'MPG');
        ''')
        card_printings = cursor.fetchall()


        url = 'https://api.justtcg.com/v1/cards'
        headers = {
            # 'x-api-key': settings.JUSTTCG_API_KEY,
            'x-api-key': os.environ.get('JUSTTCG_API_KEY'),
            'Content-Type': 'application/json',
        }

        insert_list = []
        cards_per_req = int(os.environ.get('JUSTTCG_CARDS_PER_REQ'))

        for i in range(
            0,
            len(card_printings),
            # cards_per_req,
            cards_per_req,
            # settings.JUSTTCG_CARDS_PER_REQ,
            # settings.JUSTTCG_CARDS_PER_REQ,
        ):
            req_list = []
            card_printing_chunk = card_printings[i:i + cards_per_req]
            for card_printing in card_printing_chunk:
                d = {
                  'tcgplayerId': str(int(card_printing[0])),
                  'condition': 'Near Mint',
                  'priceHistoryDuration': '1y',
                }
                card_printing = justtcg_printing_mapping.get(card_printing[1])
                if card_printing:
                    d['printing'] = card_printing
                req_list.append(d)
            if verbose:
                print('req_list: ', req_list)
            session = requests.Session()
            retries = Retry(total=2, backoff_factor=120, status_forcelist=[429])
            session.mount('https://', HTTPAdapter(max_retries=retries))
            r = session.post(url, headers=headers, json=req_list)
            # r = requests.post(url, headers=headers, json=req_list)
            if verbose:
                print('r.status_code:', r.status_code)
            if r.status_code == 200:
                r_body = r.json()
                chunk_insert_list = get_insert_list_from_body(r_body)
                # if verbose:
                #     print('r_body:', r_body)
                #     print('chunk_insert_list:', chunk_insert_list)
                insert_list.extend(chunk_insert_list)
            else:
                break

        if verbose:
            print('insert_list: ', insert_list)
        if insert_list:
            columns = insert_list[0].keys()
            query = """
                INSERT INTO price_history ({})
                VALUES %s  
                ON CONFLICT (tcgplayer_id, foiling, condition, snapshot_date)
                DO UPDATE SET 
                    price = EXCLUDED.price;
            """.format(','.join(columns))
            values = [[value for value in price_history.values()] for price_history in insert_list]
            execute_values(cursor, query, values)
            connection.commit()


def parse_arguments():
    parser = argparse.ArgumentParser(description='ingest justtcg api data')
    parser.add_argument('-v', '--verbose', action='store_true', help='printout verbosity')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    ingest_justtcg_api(
        verbose=args.verbose,
    )


if __name__ == '__main__':
    main()
