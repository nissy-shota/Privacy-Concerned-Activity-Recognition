import os
import pandas as pd
import glob
import shutil
#
mkv_dir = '/media/shota/HDD1TB/HomeActionGenome/home_action_gemone_v1/hacgen/action_split_data/V1.0'
dst_dir = '/media/shota/HDD1TB/dst'
#
missing_labels_name = ['packing_suitcase', 'listening_to_music', 'ironing_clothes', 'folding_clothes', 'getting_in_bed', 'unpacking_suitcase']

target_missing_label_name = missing_labels_name[0]

print(target_missing_label_name)

# search train and val
df_train = pd.read_csv('/home/shota/AIST/Privacy-Concerned-Activity-Recognition/list_with_activity_labels/train_list.csv', names=('path', 'label_name'))
# print(df_train)

df_val = pd.read_csv('/home/shota/AIST/Privacy-Concerned-Activity-Recognition/list_with_activity_labels/val_list.csv', names=('path', 'label_name'))
# print(df_val)

df_concat = pd.concat([df_train, df_val])
print(df_concat)


# tmp = df_concat[df_concat['label_name']==target_missing_label_name]['path']
# print(tmp)

for target_missing_label_name in missing_labels_name:
    print('--'*20)
    print(target_missing_label_name)
    tmp = df_concat[df_concat['label_name']==target_missing_label_name]['path']
    tmps = tmp.astype(str).tolist()
    print(tmps)
    os.makedirs(f'{dst_dir}/{target_missing_label_name}', exist_ok=True)

    for itmp in tmps:

        person, room, action = itmp.split('_')
        path = f'{mkv_dir}/{person}/{person}_{room}_v*_{action}.mkv'
        files = glob.glob(path)

        for file in files:
            shutil.move(file, f'{dst_dir}/{target_missing_label_name}')

# target = 'p0002_r001_a007'
# person, room, action = target.split('_')
# import shutil
#
# path = f'{mkv_dir}/{person}/{person}_{room}_v*_{action}.mkv'
# print(path)
# import glob
#
# file = glob.glob(path)
# print(file)
#
# shutil.move(file[0], dst_dir)