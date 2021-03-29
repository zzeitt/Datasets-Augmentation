import os
import csv
import urllib
import requests
import time
from itertools import islice
from tqdm import tqdm
from multiprocessing import Pool


def downloadImgs(link_file_path, download_dir, suffix=None):
    with open(link_file_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader = list(csv_reader)
        csv_reader = csv_reader[:-1]
        for row in tqdm(csv_reader):
            n_dir = row[0]
            s_link = row[1]
            n_file = os.path.basename(s_link)
            if suffix:
                n_file = n_file[:-4] + suffix

            # Execute downloading
            s_save_dir = os.path.join(download_dir, n_dir)
            os.makedirs(s_save_dir, exist_ok=True)
            # Parse link
            s_link = s_link.replace('-internal', '')
            s_link = urllib.parse.quote(s_link, safe='/,:')
            s_save_file = os.path.join(s_save_dir, n_file)
            if not os.path.exists(s_save_file):
                for i in range(10):
                    try:
                        r = requests.get(s_link)
                    except Exception as e:
                        print(f'====> Attempt {i+1}')
                        print(f'====> [Exception]: {e}')
                        time.sleep(0.5)
                    else:
                        with open(s_save_file, 'wb') as f:
                            f.write(r.content)
                        time.sleep(0.1)
                        break


if __name__ == '__main__':
    s_save = './images'
    
    # Part 1
    s_csv1 = './fonts/fonts.csv'    
    downloadImgs(s_csv1, s_save, suffix='.png')
    
    # Part 2
    s_csv2 = './fonts/fonts2.csv'
    downloadImgs(s_csv2, s_save)
