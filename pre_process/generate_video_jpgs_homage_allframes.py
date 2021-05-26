import subprocess
import argparse
from pathlib import Path

from joblib import Parallel, delayed
import json
import os
from tqdm import tqdm
import imageio
import ffmpeg
import numpy
import cv2
import sys
import random
#### image size
####TODO ### No segment

#### confirm 0 start or 1 start #### 

### parameters to be adjusted

def video_process(video_file_path, dst_root_path, ext, fps=-1):
    #if ext != video_file_path.suffix:
    #    return

    ffprobe_cmd = ('ffprobe -v error -select_streams v:0 '
                   '-of default=noprint_wrappers=1:nokey=1 -show_entries '
                   'format=width,height,avg_frame_rate,duration').split()
    ffprobe_cmd.append(str(video_file_path))

    print(video_file_path)

    p = subprocess.run(ffprobe_cmd, capture_output=True)
    res = p.stdout.decode('utf-8').splitlines()
    if len(res) < 1 or 'N' in res[0]:
        return

    #frame_rate = [float(r) for r in res[2].split('/')]
    frame_rate = 30
    duration = float(res[0])
    n_frames = int(frame_rate * duration)#-1

    name = video_file_path#.stem
    dst_dir_path = dst_root_path #/ name
    Path(dst_dir_path).mkdir(exist_ok=True)
    #if not os.path.exists(dst_dir_path):
    #  os.mkdir(dst_dir_path)
      
    #dst_dir_path.mkdir(exist_ok=True)
    #print('-----------------------------------------------------------')
    #print(n_frames)
    
    n_exist_frames = len([
        x for x in os.listdir(dst_dir_path)#.iterdir()
        if '.jpg' in x and x[0] != '.'
    ])

    if n_exist_frames >= n_frames - 1: ##TODO##
        #print('bbbb')
        return

    width = int(1024)
    height = int(768)

    #if width > height:
    #    vf_param = 'scale=-1:{}'.format(size)
    #else:
    vf_param = 'scale=1024:768'

    if fps > 0:
        vf_param += ',minterpolate={}'.format(fps)

    ffmpeg_cmd = ['ffmpeg', '-i', str(video_file_path), '-vf', vf_param]
    ffmpeg_cmd += ['-threads', '1', '{}/image_%05d.jpg'.format(dst_dir_path)]
    print(ffmpeg_cmd)
    subprocess.run(ffmpeg_cmd)
    print('\n')


def class_process(video_names, dst_names, ext, fps=-1):
    for idx in range(len(video_names)):
        video_process(video_names[idx], dst_names[idx], ext, fps)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dst_json_path', default=None, type=str)
    parser.add_argument('mkv_video_dir_path', default=None, type=str)
    parser.add_argument('jpg_video_dir_path', default=None, type=str)

    parser.add_argument(
        '--n_jobs', default=-1, type=int, help='Number of parallel jobs')
    parser.add_argument(
        '--fps',
        default=-1,
        type=int,
        help=('Frame rates of output videos. '
              '-1 means original frame rates.'))
    
    args = parser.parse_args()
  
    ext = '.mkv'

    # read json file
    with open(args.dst_json_path+'/homage_scene_graph_qiu_split_new.json', 'r') as f:
      ori_json = json.load(f)

    # review all frames
    all_frames = ori_json['database']
    
    video_names = []
    action_types = []
    dst_names = []
    for fn in all_frames:
      video_names.append(args.mkv_video_dir_path + '/'+fn.split('_')[0] + '/' + fn.split('_frame')[0]+'.mkv')
      action_types.append(all_frames[fn]['annotations']['label'])
      dst_names.append(args.jpg_video_dir_path+'/'+all_frames[fn]['annotations']['label']+'/'+fn.split('_frame')[0])
      
    for item in action_types:
      #print(item)
      if not os.path.exists(args.jpg_video_dir_path+'/'+item):
        os.mkdir(args.jpg_video_dir_path+'/'+item)
        
    print("YOU ARE HERE!")
    
    status_list = Parallel(
      n_jobs=args.n_jobs,
      backend='threading')(delayed(video_process)(
      video_names[i], dst_names[i], ext, args.fps) for i in range(len(video_names)))
