from sqlalchemy import create_engine
import sqlalchemy
from data import query_cuaca
import pandas as pd

table_name = 'prediksi_cuaca'
db_name = 'cuaca_koeh'

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

def load_init():
    engine = create_engine(f'postgresql://admin:12345@localhost:5432/{db_name}')
    return engine

def load_into(wilayah):
    engine = load_init()
    resp_data = query_cuaca(wilayah)
    result_df = compare_data(resp_data)
    if result_df.empty:
        print("Data sudah sama dengan data di database. Update tidak dilakukan")
    else:
        print('Menambahkan data ke database')
        result_df.to_sql(table_name,engine,if_exists='append',dtype=dtypes,index=False)
        print('Menambahkan berhasil.')

def load_from(columns=None):
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
    engine = load_init()
    df = pd.read_sql(query, engine, parse_dates=['local_datetime', 'analysis_datetime'])
    return df

def compare_data(df1):
    df2 = load_from(['id_wilayah','local_datetime'])
    result = pd.merge(df1, df2, how='outer', indicator=True, on=['id_wilayah','local_datetime'])
    result = result[result['_merge'] == 'left_only']
    result.drop(['_merge'], axis=1, inplace=True)
    return result

if __name__ == '__main__':
    load_into('palmerah')
    # df = load_from()
    # print(df)