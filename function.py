from database import load_init
from data import wilayah_df, extract_transform_load
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import gc
import logging

logging.basicConfig(
    filename= "app.log",
    encoding= "utf-8",
    filemode= "a",
    format= "%(asctime)s : %(levelname)s [%(name)s] %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

def update_cuaca(max_threads = 20, verbose = False):
    start_time = time.time()
    print("Update dimulai")
    engine = load_init()
    semua_wilayah_id = wilayah_df['id_wilayah'].values
    count_wilayah = semua_wilayah_id.shape[0]
    task_completed = 0
    task_failed = 0
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(extract_transform_load, wilayah_id, engine, verbose): wilayah_id for wilayah_id in semua_wilayah_id}
        for future in as_completed(futures):
            wilayah_id = futures[future]
            try: 
                is_updated = future.result()
                task_completed += 1
                print(f"{(task_completed/count_wilayah)*100:.2f}% update berhasil dikerjakan. {task_failed} gagal dikerjakan.")
                if is_updated == False:
                    logging.info('Data %s sudah terbaru. Update tidak dilakukan',wilayah_id)
                else:
                    logging.info('Data %s telah selesai diupdate.',wilayah_id)
            except Exception as e:
                print(f"GAGAL update untuk wilayah {wilayah_id}")
                logging.error('Gagal update %s dengan error "%s"',wilayah_id,e)
                task_failed += 1
            finally:
                del future
                del is_updated
                gc.collect()

    end_time = time.time()
    print(f"Update selesai dalam waktu {end_time - start_time:.2f} detik.")

if __name__ == '__main__':
    update_cuaca()