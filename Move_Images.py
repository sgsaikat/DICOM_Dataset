import os
import shutil
import pandas as pd
from datetime import datetime

start_time = datetime.now()

meta_info = pd.read_csv('Meta_Info.csv', usecols=['File Name', 'Response'])
meta_info['File Name'] = meta_info['File Name'].apply(lambda x: x + '.jpg')
print("Meta Info Shape ->", meta_info.shape)

unlabelled_data = meta_info[meta_info['Response'] == 'None']
meta_info = meta_info[meta_info['Response'] != 'None']

train_data = meta_info.iloc[:92189]
validation_data = train_data.sample(frac=0.3, random_state=42)
test_data = meta_info.iloc[92189:]

print(f"Train Data Size -> {train_data.shape[0] - validation_data.shape[0]}")
print(f"Validation Data Size -> {validation_data.shape[0]}")
print(f"Test Data Size -> {test_data.shape[0]}")
print(f"Unlabelled Data Size -> {unlabelled_data.shape[0]}")

def move_imgs(dest, data, sub_dir=True):
    print(f"Processing {dest}...\n")

    files_not_found = []
    src = 'Orig_Images'
    dest = f'Images/{dest}'
    for _,row in data.iterrows():
        file_name = row['File Name']
        response = row['Response']
        try:
            if sub_dir:
                shutil.move(f'{src}/{file_name}', f'{dest}/{response}/{file_name}')
            else:
                shutil.move(f'{src}/{file_name}', f'{dest}/{file_name}')
        except FileNotFoundError as err:
            files_not_found.append(file_name)
    
    if sub_dir:
        print(f"No. of Images in -> {dest}/pCR: {len(os.listdir(f'{dest}/pCR'))}, {dest}/non-pCR: {len(os.listdir(f'{dest}/non-pCR'))}")
    else:
        print(f"No. of Images in -> {src}/{dest}: {len(os.listdir(f'{dest}'))}")
    
    print(f"# Files not found -> {len(files_not_found)}")
    print(files_not_found)
    print()

move_imgs('Unlabelled Images', unlabelled_data, sub_dir=False)
move_imgs('Test Images', test_data)
move_imgs('Validation Images', validation_data)
move_imgs('Train Images', train_data)

print(f"Time Taken -> {datetime.now() - start_time}")

