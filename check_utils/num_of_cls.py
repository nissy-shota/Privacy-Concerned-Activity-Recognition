import os

BASE_DIR = '/home/shota/AIST/Privacy-Concerned-Activity-Recognition/list_with_activity_labels'
file_name = 'classInd.txt'

file_path = os.path.join(BASE_DIR, file_name)

with open(file_path, mode='rt', encoding='utf-8') as f:
    read_data = f.readlines()

# print(read_data)
# print(len(read_data))

labels_name = []
for line in read_data:
    l = line.split(',')
    labels_name.append(l[1])

non_labels_name = []
for label_name in labels_name:
    non_labels_name.append(label_name.strip('\n'))

# print(non_labels_name)

pwd_names = os.listdir('/media/shota/HDD1TB/split')
# print(pwd_names)


unique = set(non_labels_name).difference(set(pwd_names))
# print(unique)

# Missing label name
missin_labels = list(unique)
print(missin_labels)