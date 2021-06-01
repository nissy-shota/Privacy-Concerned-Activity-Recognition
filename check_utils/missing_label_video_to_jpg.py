import os
import glob
import subprocess
import argparse
from pathlib import Path

from joblib import Parallel, delayed
import json

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



target_dir = '/media/shota/HDD1TB/dst'
save_dir = '/media/shota/HDD1TB/dst_jpg'

target_dirs = glob.glob(f'{target_dir}/*')
target_dirs.sort()

video_names = []
for itarget_dir in target_dirs:
    print(itarget_dir)
    os.makedirs(itarget_dir.replace('dst','dst_jpg'),exist_ok=True)

    files = glob.glob(f'{itarget_dir}/*.mkv')
    files.sort()
    video_names+= files

video_names.sort()
print(video_names)
dst_names = []
for dst_file_name in video_names:
    dst_file_name = dst_file_name.replace('dst', 'dst_jpg')
    file_path, ext = dst_file_name.split('.')
    print(file_path)
    dst_names.append(file_path)
dst_names.sort()

n_jobs = -1
fps = -1
ext = '.mkv'
status_list = Parallel(
    n_jobs=n_jobs,
    backend='threading')(delayed(video_process)(
    video_names[i], dst_names[i], ext, fps) for i in range(len(video_names)))
