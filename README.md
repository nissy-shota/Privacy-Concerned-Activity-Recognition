# Privacy-Concerned-Activity-Recognition

## prerequisite

```shell
tree -L 2
```

```shell
├── action_split_data
│   └── V1.0 -> /media/shota/HDD1TB/HomeActionGenome/home_action_gemone_v1/hacgen/action_split_data/V1.0
├── annotation_files
│   └── atomic_actions
├── homage
│   ├── backbone
│   ├── data
│   ├── data_utils.py
│   ├── hierarchical_homage_single_sample.py
│   ├── model_utils.py
│   ├── readme.md
│   └── utils
├── list_with_activity_labels
│   ├── classInd_atomic.txt
│   ├── classInd.txt
│   ├── train_list.csv
│   └── val_list.csv
├── pre_process
│   ├── extract_frame.py
│   └── write_csv.py
└── README.md

```
## preprocessing

- extract_frame.py
  config.yamlで指定したsave_div_framesにpngを保存する．
```shell
cd pre_process
python3 extract_frame.py
```
