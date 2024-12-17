import re
import csv

filename = 'data/base.csv'
testing = False

provinsi_pattern = r'^([0-9]{2})$'
kota_pattern = r'^([0-9]{2})\.([0-9]{2})$' 
kecamatan_pattern = r'^([0-9]{2})\.([0-9]{2})\.([0-9]{2})$'
wilayah_pattern = r'^([0-9]{2})\.([0-9]{2})\.([0-9]{2})\.([0-9]{4})$'

tingkat4_pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.([0-9])'
tingkat2_pattern = r'([A-Za-z]+)'

kode_provinsi = {}
kode_provinsi['provinsi_id'] = []
kode_provinsi['nama'] = []

kode_kota = {}
kode_kota['provinsi_id'] = []
kode_kota['kota_id'] = []
kode_kota['nama'] = []
kode_kota['jenis_kota'] = []

kode_kecamatan = {}
kode_kecamatan['provinsi_id'] = []
kode_kecamatan['kota_id'] = []
kode_kecamatan['kecamatan_id'] = []
kode_kecamatan['nama'] = []

kode_wilayah = {}
kode_wilayah['provinsi_id'] = []
kode_wilayah['kota_id'] = []
kode_wilayah['kecamatan_id'] = []
kode_wilayah['desa_id'] = []
kode_wilayah['nama'] = []
kode_wilayah['jenis_wilayah'] = []


def extract_transform(filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # print(next(csvreader))
        for row_data in csvreader:
            transform_upper_level(row_data)
        if testing == True:
            test_transform_upper()

def transform_provinsi(row_data):
    result = re.search(provinsi_pattern,row_data[0])
    if (result != None):
        kode_provinsi['provinsi_id'].append(result.group(1))
        kode_provinsi['nama'].append(row_data[1].lower())

def transform_kota(row_data):
    result = re.search(kota_pattern,row_data[0])
    if (result != None):
        kode_kota['provinsi_id'].append(result.group(1))
        kode_kota['kota_id'].append(result.group(2))
        filt = re.findall(tingkat2_pattern, row_data[1])
        if filt[0] == 'KAB':
            kode_kota['jenis_kota'].append('kabupaten')
        else:
            kode_kota['jenis_kota'].append('kota')
        kode_kota['nama'].append((' '.join([filt[i] for i in range(2,len(filt))]) if filt[1] == 'ADM' \
                                 else ' '.join([filt[i] for i in range(1,len(filt))])).lower())

def transform_kecamatan(row_data):
    result = re.search(kecamatan_pattern,row_data[0])
    if (result != None):
        kode_kecamatan['provinsi_id'].append(result.group(1))
        kode_kecamatan['kota_id'].append(result.group(2))
        kode_kecamatan['kecamatan_id'].append(result.group(3))
        kode_kecamatan['nama'].append(row_data[1].lower())

def transform_wilayah(row_data):
    result = re.search(wilayah_pattern,row_data[0])
    if (result != None):
        kode_wilayah['provinsi_id'].append(result.group(1))
        kode_wilayah['kota_id'].append(result.group(2))
        kode_wilayah['kecamatan_id'].append(result.group(3))
        kode_wilayah['desa_id'].append(result.group(4))
        kode_wilayah['nama'].append(row_data[1].lower())
        filt = re.search(tingkat4_pattern,row_data[0])
        kode_wilayah['jenis_wilayah'].append('kelurahan' if filt.group(1) == '1' else 'desa')

def transform_upper_level(row_data):
    transform_provinsi(row_data)
    transform_kota(row_data)
    transform_kecamatan(row_data)
    transform_wilayah(row_data)


# Testing Code 
def test_provinsi():
    assert kode_provinsi['provinsi_id'][0] == '11', f'kode provinsi harusnya 11, dapatnya {kode_provinsi['provinsi_id'][0]}'
    assert kode_provinsi['nama'][0] == 'aceh', f'nama provinsi harusnya aceh, dapatnya {kode_provinsi['nama'][0]}'

def test_kota():
    assert kode_kota['provinsi_id'][0] == '11', f'kode provinsi harusnya 11, dapatnya {kode_kota['provinsi_id'][0]}'
    assert kode_kota['nama'][0] == 'aceh selatan', f'nama provinsi harusnya aceh selatan, dapatnya {kode_kota['nama'][0]}'
    assert kode_kota['kota_id'][0] == '01', f'kode kota harusnya 01, dapatnya {kode_kota['kota_id'][0]}'

def test_kecamatan():
    assert kode_kecamatan['provinsi_id'][0] == '11', f'kode provinsi harusnya 11, dapatnya {kode_kecamatan['provinsi_id'][0]}'
    assert kode_kecamatan['nama'][0] == 'bakongan', f'nama provinsi harusnya bakongan, dapatnya {kode_kecamatan['nama'][0]}'
    assert kode_kecamatan['kota_id'][0] == '01', f'kode kota harusnya 01, dapatnya {kode_kecamatan['kota_id'][0]}'
    assert kode_kecamatan['kecamatan_id'][0] == '01', f'kode kota harusnya 01, dapatnya {kode_kecamatan['kecamatan_id'][0]}'


def test_transform_upper(verbose=False):
    test_provinsi()
    print('' if verbose == False else 'Test Provinsi Sukses\n',end='')
    test_kota()
    print('' if verbose == False else 'Test Kota Sukses\n',end='')
    test_kecamatan()
    print('' if verbose == False else 'Test Kecamatan Sukses\n',end='')

# Test purposes
if __name__ == '__main__':
    testing = True
    print('Testing Purposes Only')

# Start executing
extract_transform(filename)

if __name__ == '__main__':
    for i in range(3):
        print(kode_wilayah['provinsi_id'][i],'.',kode_wilayah['kota_id'][i],'.',
                kode_wilayah['kecamatan_id'][i],'.',kode_wilayah['desa_id'][i],end=' ')
        print(kode_wilayah['nama'][i])