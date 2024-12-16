import json
import requests
import pandas as pd
from wilayah import kode_wilayah, kode_kecamatan, kode_kota, kode_provinsi

kode_wilayah_df = pd.DataFrame(kode_wilayah)
kode_kecamatan_df = pd.DataFrame(kode_kecamatan)
kode_kota_df = pd.DataFrame(kode_kota)
kode_provinsi_df = pd.DataFrame(kode_provinsi)

wilayah_df = pd.merge(kode_wilayah_df,kode_kecamatan_df,
                      left_on=['provinsi_id','kota_id','kecamatan_id'],
                      right_on=['provinsi_id','kota_id','kecamatan_id'],
                      suffixes=('_wilayah','_kecamatan'))\
            .merge(kode_kota_df,
                   left_on=['provinsi_id','kota_id'],
                   right_on=['provinsi_id','kota_id'])\
            .rename(columns={'nama':'nama_kota'})\
            .merge(kode_provinsi_df,left_on='provinsi_id',right_on='provinsi_id')\
            .rename(columns={'nama':'nama_provinsi'})

wilayah_df['full_id'] = wilayah_df['provinsi_id'] + '.' \
                        + wilayah_df['kota_id'] + '.' \
                        + wilayah_df['kecamatan_id'] + '.' \
                        + wilayah_df['desa_id']

def get_wilayah_id(wilayah):
    get = wilayah_df[wilayah_df['nama_wilayah'] == f'{wilayah.lower()}']
    if get.empty:
        get = wilayah_df[wilayah_df['nama_kecamatan'] == f'{wilayah.lower()}']
        if get.empty:
            get = wilayah_df[wilayah_df['nama_kota'] == f'{wilayah.lower()}']
            if get.empty:
                get = wilayah_df[wilayah_df['nama_provinsi'] == f'{wilayah.lower()}']
    return get['full_id'].values[0]

def get_detail_wilayah(wilayah_id):
    res_df = wilayah_df[wilayah_df['full_id'] == wilayah_id]
    return (res_df['nama_provinsi'].values[0],\
            res_df['nama_kota'].values[0],\
            res_df['nama_kecamatan'].values[0],\
            res_df['nama_wilayah'].values[0])

def extract(wilayah_id):
    api_url = f'https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={wilayah_id}'
    response = json.loads(requests.get(api_url).text)
    return response

def transform(jsonfile):
    transformed_dict = {}
    transformed_dict['local_datetime'] = []
    transformed_dict['analysis_datetime'] = []
    transformed_dict['suhu'] = []
    transformed_dict['kelembapan'] = []
    transformed_dict['deskripsi'] = []
    transformed_dict['kecepatan_angin'] = []
    transformed_dict['arah_angin'] = []
    transformed_dict['tutupan_awan'] = []
    transformed_dict['jarak_pandang'] = []
    transformed_dict['id_wilayah'] = []
    for day in jsonfile['data'][0]['cuaca']:
        for hour in day:
            transformed_dict['local_datetime'].append(hour['local_datetime'])
            transformed_dict['analysis_datetime'].append(hour['analysis_date'])
            transformed_dict['suhu'].append(hour['t'])
            transformed_dict['kelembapan'].append(hour['hu'])
            transformed_dict['deskripsi'].append(hour['weather_desc'])
            transformed_dict['kecepatan_angin'].append(hour['ws']) 
            transformed_dict['arah_angin'].append(hour['wd'])
            transformed_dict['tutupan_awan'].append(hour['tcc'])
            transformed_dict['jarak_pandang'].append(hour['vs_text'])
            transformed_dict['id_wilayah'].append(jsonfile['lokasi']['adm4'])
    df = pd.DataFrame(transformed_dict)
    df['local_datetime'] = pd.to_datetime(df['local_datetime'])
    df['analysis_datetime'] = pd.to_datetime(df['analysis_datetime'])
    # df.sort_values('local_datetime',inplace=True,ascending=False)
    return df

def get_info(wilayah):
    try:
        wilayah_id = get_wilayah_id(wilayah)
        provinsi, kota, kecamatan, nama_wilayah = get_detail_wilayah(wilayah_id)
        result = extract(wilayah_id)
        df = transform(result).iloc[0]
        print(f"Data Cuaca Provinsi {provinsi.capitalize()}, {kota.capitalize()}, {kecamatan.capitalize()}, {nama_wilayah.capitalize()}")
        print(f"{df['local_datetime'].day}-{df['local_datetime'].month}-{df['local_datetime'].year}")
        print(f"{df['deskripsi']}")
        print(f"Suhu : {df['suhu']}°C")
        print(f"Kelembapan Udara : {df['kelembapan']}")
        print(f"Kecepatan Angin : {df['kecepatan_angin']}")
    except Exception as e:
        print(e)

def query_cuaca(wilayah):
    try:
        wilayah_id = get_wilayah_id(wilayah)
        result = extract(wilayah_id)
        df = transform(result)
        return df
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print(wilayah_df.sample(10))
#     print(wilayah_df.info())