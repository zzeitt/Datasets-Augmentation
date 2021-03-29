import cv2
import numpy as np
from imgaug.augmenters import Augmenter
from imgaug import augmenters as iaa


# ========= Shading Augmentation ============
def gen_linear_bgd(img, high=0.5):
    mask = np.repeat(
        np.tile(
            np.linspace(high, 0, img.shape[1]),
            (img.shape[0], 1))[:, :, np.newaxis],
        1, axis=2)
    return mask

def fill_color(img, val_fgd=0.5, val_bgd=0.5):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[:,:,np.newaxis]
    _, img_thr = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    img_bin = img_thr.astype(np.bool)

    # Generate background
    img_bgd = gen_linear_bgd(img, val_bgd)
    bgd_seq = iaa.Sequential([
        iaa.Resize(1.42),
        iaa.Rotate((-90, 90)),
        iaa.CropToFixedSize(img.shape[1], img.shape[0], position='center'),
    ])
    img_bgd = img_bgd[np.newaxis, :, :, :]
    img_bgd = bgd_seq(images=img_bgd)[0]
    
    # Composition
    img_ret = img_bgd.copy()
    img_ret[img_bin] = val_fgd
    
    # Convert float64 to uint8
    img_ret *= 255
    img_ret = np.uint8(img_ret)
    return img_ret

def func_images(images, random_state, parents, hooks):
    images_ret = images.copy()
    # WxHxCxB
    for i in range(images.shape[3]):
        val_fgd = np.random.uniform(0.5, 1.0)
        val_bgd = np.random.uniform(0.3, 0.5)
        images_ret[:, :, :, i] = fill_color(
            images_ret[:, :, :, i], val_fgd, val_bgd)
    return images_ret

shade_aug = iaa.Lambda(func_images=func_images)
shade_seq = iaa.Sequential([
    shade_aug,
])

# ========== Other Augmentation =============
# perspective transform
# rotation (affine transform)
# blur (gaussian blur)
# noise (gaussian noise)
other_seq = iaa.Sequential([
    iaa.PerspectiveTransform(scale=(0.01, 0.15)),
    iaa.Affine(rotate=(-30, 30)),
    iaa.GaussianBlur(sigma=(0.0, 1.0)),
    iaa.AdditiveGaussianNoise(scale=(0, 0.1*255)),
])

# =========== Whole Pipeline =================
def aug_image(img_inp):
    # Shading augmentations
    img_shade_aug = shade_seq(images=img_inp)
    # Other augmentations
    img_shade_aug = cv2.cvtColor(img_shade_aug, cv2.COLOR_BGR2GRAY)
    img_other_aug = other_seq(images=img_shade_aug)
    return img_other_aug


if __name__ == '__main__':
    img_src = cv2.imread('./images/一/24.png')
    
    for i in range(100):
        img_out = aug_image(img_src)
        print(f'====> img_out.shape: {img_out.shape}')
    
        # Show images
        cv2.imshow('img_src', img_src)
        cv2.imshow('img_out', img_out)
        
        k = cv2.waitKey(0)
        if k == ord('q'):
            break
        else:
            pass
        cv2.destroyAllWindows()
