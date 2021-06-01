import argparse
import json
from pathlib import Path

import pandas as pd

import os

def get_n_frames(video_path):
    return len([
        x for x in video_path.iterdir()
        if 'image' in x.name and x.name[0] != '.'
    ])

def convert_csv_to_dict(csv_path, subset,video_dir_path):
    data = pd.read_csv(csv_path, delimiter=',', header=None)
    keys = []
    key_labels = []
    for i in range(data.shape[0]):
        row = data.iloc[i, :]
        #slash_rows = data.iloc[i, 0].split('/')
        #class_name = slash_rows[0]
        class_name = data.iloc[i,1]
        #basename = slash_rows[1].split('.')[0]
        basename = data.iloc[i,0]
        #print("--------------------------------------------------------")
        #print(type(basename))

        video_label_path =  video_dir_path / class_name
        video_files = os.listdir(video_label_path)
        base_p = basename[1:5]

        for vf in video_files:
            #vf = str(vf)
            #print(vf)
            vfp = vf[1:5]
            #print(vf)
            if vfp in base_p:
                #print(vfp)
                #vfv = vf[12:15]
                #print("v")
                #print(vfv)
                keys.append(vf)
                key_labels.append(class_name)

    database = {}
    for i in range(len(keys)):
        key = keys[i]
        database[key] = {}
        database[key]['subset'] = subset
        label = key_labels[i]
        database[key]['annotations'] = {'label': label}

    return database

def load_labels(label_csv_path):
    data = pd.read_csv(label_csv_path, delimiter=',', header=None)
    labels = []
    for i in range(data.shape[0]):
        labels.append(data.iloc[i, 1])
    return labels

def convert_homage_csv_to_json(train_csv_path, val_csv_path,video_dir_path, dst_json_path):
    labels = load_labels(label_csv_path)
    train_database = convert_csv_to_dict(train_csv_path, 'training',video_dir_path)
    val_database = convert_csv_to_dict(val_csv_path, 'validation',video_dir_path)

    dst_data = {}
    dst_data['labels'] = labels
    dst_data['database'] = {}
    dst_data['database'].update(train_database)
    dst_data['database'].update(val_database)

    for k, v in dst_data['database'].items():
        if v['annotations'] is not None:
            label = v['annotations']['label']
        else:
            label = 'test'
            
        video_path = video_dir_path / label / k
        n_frames = get_n_frames(video_path)
        v['annotations']['segment'] = (1, n_frames + 1)

    with dst_json_path.open('w') as dst_file:
        json.dump(dst_data, dst_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path',
                        default=None,
                        type=Path,
                        help=('Directory path including  trainlist0-.txt, testlist0-.txt'))
    parser.add_argument('video_path',
                        default=None,
                        type=Path,
                        help=('Path of video directory (jpg).'
                              'Using to get n_frames of each video.'))
    parser.add_argument('dst_path',
                        default=None,
                        type=Path,
                        help='Directory path of dst json file.')

    args = parser.parse_args()

    #for split_index in range(1, 4):
    label_csv_path = args.dir_path / 'classInd.txt'
    train_csv_path = args.dir_path / 'train_list.csv'#.format(split_index)
    val_csv_path = args.dir_path / 'val_list.csv'#.format(split_index)
    dst_json_path = args.dst_path / 'homage.json'#.format(split_index)

    convert_homage_csv_to_json(train_csv_path, val_csv_path,args.video_path, dst_json_path)    #for end