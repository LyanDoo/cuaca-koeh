from data import query_cuaca
import sys

# get_info(sys.argv[1])
print(query_cuaca(sys.argv[1]).info())
print('Sumber: Data Terbuka BMKG')