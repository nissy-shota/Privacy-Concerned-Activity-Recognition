from joblib import delayed, Parallel
import os 
import sys 
import glob 
from tqdm import tqdm 
import cv2
import argparse

import matplotlib.pyplot as plt
import yaml
plt.switch_backend('agg')


def str2bool(s):
    """Convert string to bool (in argparse context)."""
    if s.lower() not in ['true', 'false']:
        raise ValueError('Need bool; got %r' % s)
    return {'true': True, 'false': False}[s.lower()]


def extract_video_opencv(v_path, f_root, dim=240):
    '''v_path: single video path;
       f_root: root to store frames'''
    v_class = v_path.split('/')[-2]
    v_name = os.path.basename(v_path)[0:-4]
    out_dir = os.path.join(f_root, v_class, v_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    vidcap = cv2.VideoCapture(v_path)
    nb_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    if (width == 0) or (height == 0):
        print(v_path, 'not successfully loaded, drop ..'); return
    new_dim = resize_dim(width, height, dim)

    success, image = vidcap.read()
    count = 1
    while success:
        image = cv2.resize(image, new_dim, interpolation = cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(out_dir, '%06d.png' % count), image,
                    [cv2.IMWRITE_JPEG_QUALITY, 80])# quality from 0-100, 95 is default, high is good
        success, image = vidcap.read()
        count += 1

    # Correct the amount of frames
    if (count * 30) < nb_frames:
        nb_frames = int(nb_frames * 30 / 1000)

    if nb_frames > count:
        print('/'.join(out_dir.split('/')[-2::]), 'NOT extracted successfully: %df/%df' % (count, nb_frames))

    vidcap.release()


def resize_dim(w, h, target):
    '''resize (w, h), such that the smaller side is target, keep the aspect ratio'''
    if w >= h:
        return (int(target * w / h), int(target))
    else:
        return (int(target), int(target * h / w)) 

def main_Homage(v_root, f_root, dim):
    print('extracting Homage ... ')
    print('extracting videos from %s' % v_root)
    print('frame save to %s' % f_root)

    if not os.path.exists(f_root): os.makedirs(f_root)
    v_act_root = glob.glob(os.path.join(v_root, '*/'))
    print(len(v_act_root))
    for i, j in tqdm(enumerate(v_act_root), total=len(v_act_root)):
        v_paths = glob.glob(os.path.join(j, '*.mkv'))
        v_paths = sorted(v_paths)
        Parallel(n_jobs=-1)(delayed(extract_video_opencv)(p, f_root, dim) for p in tqdm(v_paths, total=len(v_paths)))


if __name__ == '__main__':
    # v_root is the video source path, f_root is where to store frames
    # edit 'your_path' here:

    parser = argparse.ArgumentParser(description='Privacy Concerned Activity Recognition')
    parser.add_argument("--yaml_file", type=str, default='../config.yaml')
    args = parser.parse_args()

    yaml_file = args.yaml_file

    with open(yaml_file) as stream:
        config = yaml.safe_load(stream)

    v_root = config['preproc']['action_split_data']
    f_root = config['preproc']['save_div_frames']
    dim = config['preproc']['dim']

    main_Homage(v_root=v_root, f_root=f_root, dim=dim)

