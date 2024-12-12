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


if __name__ == '__main__':
    print(wilayah_df.sample(10))
#     print(wilayah_df.info())