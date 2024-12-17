from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    filename= "app.log",
    encoding= "utf-8",
    filemode= "a",
    format= "%(asctime)s : %(levelname)s [%(name)s] %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

table_name = 'prediksi_cuaca'
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
PG_USER = os.getenv("PG_USERNAME")
PASSWORD = os.getenv("PASSWORD")

if ((not DB_NAME) or (not HOST) or (not PG_USER) or (not PASSWORD)):
    logging.error('Gagal menarik data environment')
    raise Exception("Gagal menarik data environment")

dtypes = {
    'id_wilayah': sqlalchemy.types.CHAR(13),
    'local_datetime': sqlalchemy.TIMESTAMP(),
    'analysis_datetime': sqlalchemy.TIMESTAMP(),
    'suhu': sqlalchemy.types.SMALLINT(),
    'kelembapan': sqlalchemy.types.SMALLINT(),
    'kecepatan_angin': sqlalchemy.types.REAL(),
    'arah_angin': sqlalchemy.types.VARCHAR(length=3),
    'tutupan_awan': sqlalchemy.types.SMALLINT(),
    'jarak_pandang': sqlalchemy.types.TEXT(),
    'deskripsi': sqlalchemy.types.TEXT()
}

def load_init(pool_size=50, max_overflow=5):
    engine = create_engine(f'postgresql://{PG_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}',
                           pool_size=pool_size,
                           max_overflow=max_overflow)
    return engine

def load_into(resp_df, engine, verbose = False):
    result_df = compare_data(resp_df, engine)
    if result_df.empty:
        print("Data sudah sama dengan data di database. Update tidak dilakukan.\n" if verbose else '', end='')
    else:
        print('Menambahkan data ke database\n' if verbose else '', end='')
        result_df.to_sql(table_name,engine,if_exists='append',dtype=dtypes,index=False)
        print('Menambahkan berhasil.\n'  if verbose else '', end='')
    is_updated = not result_df.empty
    del result_df
    return is_updated


def load_from(engine, columns=None):
    column_query = ''
    if columns != None:
        for i in range(len(columns)):
            if i == len(columns)-1:
                column_query += f'{columns[i]}'
            else:
                column_query += f'{columns[i]},'
    else:
        column_query = '*'                
    query = f'SELECT {column_query} FROM {table_name};'
    df = pd.read_sql(query, engine, parse_dates=['local_datetime', 'analysis_datetime'])
    return df

def compare_data(df1, engine):
    df2 = load_from(engine,['id_wilayah','local_datetime'])
    result = pd.merge(df1, df2, how='outer', indicator=True, on=['id_wilayah','local_datetime'])
    result = result[result['_merge'] == 'left_only']
    result.drop(['_merge'], axis=1, inplace=True)
    return result

if __name__ == '__main__':
    engine = load_init()
    load_into('palmerah', engine)