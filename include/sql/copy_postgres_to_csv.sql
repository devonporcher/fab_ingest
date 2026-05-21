COPY card TO '/opt/airflow/include/data/temp/card.csv' WITH (FORMAT CSV, HEADER);
COPY card_printing TO '/opt/airflow/include/data/temp/card_printing.csv' WITH (FORMAT CSV, HEADER);
COPY price_history TO '/opt/airflow/include/data/temp/price_history.csv' WITH (FORMAT CSV, HEADER);