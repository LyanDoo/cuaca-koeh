import re
import csv

filename = 'data/base.csv'

provinsi_pattern = r'^([0-9]{2})$'
kota_pattern = r'^([0-9]{2})\.([0-9]{2})$' 
kecamatan_pattern = r'^([0-9]{2})\.([0-9]{2})\.([0-9]{2})$'
wilayah_pattern = r'^([0-9]{2})\.([0-9]{2})\.([0-9]{2})\.([0-9]{4})$'

kode_provinsi = {}
kode_provinsi['provinsi_id'] = []
kode_provinsi['nama'] = []

kode_kota = {}
kode_kota['provinsi_id'] = []
kode_kota['kota_id'] = []
kode_kota['nama'] = []

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


def extract_transform(filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # print(next(csvreader))
        for row_data in csvreader:
            transform_upper_level(row_data)
        test_transform_upper()
            
            




def transform_provinsi(row_data):
    result = re.search(provinsi_pattern,row_data[0])
    if (result != None):
        kode_provinsi['provinsi_id'].append(result.group(1))
        kode_provinsi['nama'].append(row_data[1])

def transform_kota(row_data):
    result = re.search(kota_pattern,row_data[0])
    if (result != None):
        kode_kota['provinsi_id'].append(result.group(1))
        kode_kota['kota_id'].append(result.group(2))
        kode_kota['nama'].append(row_data[1])

def transform_kecamatan(row_data):
    result = re.search(kecamatan_pattern,row_data[0])
    if (result != None):
        kode_kecamatan['provinsi_id'].append(result.group(1))
        kode_kecamatan['kota_id'].append(result.group(2))
        kode_kecamatan['kecamatan_id'].append(result.group(3))
        kode_kecamatan['nama'].append(row_data[1])

def transform_wilayah(row_data):
    result = re.search(wilayah_pattern,row_data[0])
    if (result != None):
        kode_wilayah['provinsi_id'].append(result.group(1))
        kode_wilayah['kota_id'].append(result.group(2))
        kode_wilayah['kecamatan_id'].append(result.group(3))
        kode_wilayah['desa_id'].append(result.group(4))
        kode_wilayah['nama'].append(row_data[1])

def transform_upper_level(row_data):
    transform_provinsi(row_data)
    transform_kota(row_data)
    transform_kecamatan(row_data)
    transform_wilayah(row_data)


# Testing Code 
def test_provinsi():
    assert kode_provinsi['provinsi_id'][0] == '11', f'kode provinsi harusnya 11, dapatnya {kode_provinsi['provinsi_id'][0]}'
    assert kode_provinsi['nama'][0] == 'ACEH', f'nama provinsi harusnya ACEH, dapatnya {kode_provinsi['nama'][0]}'

def test_kota():
    assert kode_kota['provinsi_id'][0] == '11', f'kode provinsi harusnya 11, dapatnya {kode_kota['provinsi_id'][0]}'
    assert kode_kota['nama'][0] == 'KAB. ACEH SELATAN', f'nama provinsi harusnya KAB. ACEH SELATAN, dapatnya {kode_kota['nama'][0]}'
    assert kode_kota['kota_id'][0] == '01', f'kode kota harusnya 01, dapatnya {kode_kota['kota_id'][0]}'

def test_kecamatan():
    assert kode_kecamatan['provinsi_id'][0] == '11', f'kode provinsi harusnya 11, dapatnya {kode_kecamatan['provinsi_id'][0]}'
    assert kode_kecamatan['nama'][0] == 'Bakongan', f'nama provinsi harusnya Bakongan, dapatnya {kode_kecamatan['nama'][0]}'
    assert kode_kecamatan['kota_id'][0] == '01', f'kode kota harusnya 01, dapatnya {kode_kecamatan['kota_id'][0]}'
    assert kode_kecamatan['kecamatan_id'][0] == '01', f'kode kota harusnya 01, dapatnya {kode_kecamatan['kecamatan_id'][0]}'


def test_transform_upper(verbose=False):
    test_provinsi()
    print('' if verbose == False else 'Test Provinsi Sukses\n',end='')
    test_kota()
    print('' if verbose == False else 'Test Kota Sukses\n',end='')
    test_kecamatan()
    print('' if verbose == False else 'Test Kecamatan Sukses\n',end='')


# Start Executing
extract_transform(filename)

# Test purposes
if __name__ == '__main__':
    print('Testing Purposes Only')
    for i in range(3):
        print(kode_wilayah['provinsi_id'][i],'.',kode_wilayah['kota_id'][i],'.',
                kode_wilayah['kecamatan_id'][i],'.',kode_wilayah['desa_id'][i],end=' ')
        print(kode_wilayah['nama'][i])
        # print('len of dict : ',len(kode_wilayah['desa_id']))