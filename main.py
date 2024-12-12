import json
import requests
from data import wilayah_df


def req_api(wilayah):
    api_url = f'https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={wilayah}'
    response = requests.get(api_url)
    return response

try:
    result = json.loads(req_api(wilayah_df[wilayah_df['nama_wilayah'] == 'Keude Bakongan']['full_id'].values[0]).text)
    print(result)
except Exception as e:
    print(e)
