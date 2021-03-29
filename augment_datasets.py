import os
import cv2
import math
import numpy as np
from augmentation import aug_image
from tqdm import tqdm


def getFilePaths(path):
    # read a folder, return the complete path
    ret = []
    for root, dirs, files in os.walk(path):
        print
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    ret.sort()
    return ret


if __name__ == '__main__':
    s_base = (
        '/home/zeit/SDB/NiseEngFolder/newDownloads/forFontDatasets/'
        'forCooperation/images')
    
    li_char_folders = []
    for root, dirs, files in os.walk(s_base):
        li_char_folders.append(root)
    li_char_folders = li_char_folders[1:]
    li_char_folders.sort()
    
    for idx, s_folder in enumerate(tqdm(li_char_folders[:-1])):
        f_save_images_aug = s_folder.replace('images', 'images_aug')
        
        li_img_paths = getFilePaths(s_folder)
        for _, s_img in enumerate(tqdm(li_img_paths[:-1])):
            n_file = os.path.basename(s_img)
            f_save_per_img = os.path.join(f_save_images_aug, n_file[:-4])
            os.makedirs(f_save_per_img, exist_ok=True)
            
            n_aug = 10
            z = math.floor(math.log10(n_aug)) + 1
            for i in range(n_aug):
                n_file_aug = f'{i:0{z}}{n_file[-4:]}'
                s_save_img_aug = os.path.join(f_save_per_img, n_file_aug)
                
                # ------------------------------------
                #           Real Processing
                # ------------------------------------
                if not os.path.exists(s_save_img_aug):
                    img_inp = cv2.imread(s_img)
                    img_aug = aug_image(img_inp)
                    cv2.imwrite(s_save_img_aug, img_aug)
