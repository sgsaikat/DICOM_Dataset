import pydicom as dicom
import sys
import os
import pandas as pd
from matplotlib import pyplot as plt, image, cm
from datetime import datetime
import traceback

start_time = datetime.now()
meta_info = []
in_path = 'Downloaded_Data/QIN-BREAST'
out_path = 'Images'
patients = os.listdir(in_path)
responses = dict()

treat_file = pd.read_excel('QIN-Breast_TreatmentResponse(2014-12-16).xlsx')
def get_resp(row):
    responses[row['Patient ID']] = row['Response']
treat_file.apply(get_resp, axis=1)

with open("Logs.txt", "w") as log:
    log.write(f"File contains the errors ecountered ::\n{'='*80}\n")

with open("Meta_Info.csv", "w") as info:
    info.write("File Name,Patient Age,Patient Birth Date,Patient ID,Patient Identity Removed,Patient Name,Patient Position,Patient Sex,Patient Size,Patient Weight,Response\n")

for patient in patients:
    print(f"Processing {patient}...")
    count = 0
    dates = os.listdir(f"{in_path}/{patient}")
    # print("Dates", dates)
    for date in dates:
        print(f"\tProcessing {date}...")
        scans = os.listdir(f"{in_path}/{patient}/{date}")
        # print("Scans", scans)
        for scan in scans:
            # print(f"\t\tProcessing {scan}...")
            dcm_files = os.listdir(f"{in_path}/{patient}/{date}/{scan}")
            # print("Files", dcm_files)
            for dcm_file in dcm_files:
                # print(f"\t\t\tProcessing {dcm_file}...")
                try:
                    ds = dicom.dcmread(f"{in_path}/{patient}/{date}/{scan}/{dcm_file}")
                    file_name = f"{patient}_{str(count).rjust(3, '0')}"
                    count += 1
                    image.imsave(f"{out_path}/{file_name}.jpg", ds.pixel_array, cmap=cm.get_cmap('Greys'))

                    PatientAge = ds.get('PatientAge', default='')
                    PatientBirthDate = ds.get('PatientBirthDate', default='')
                    PatientID = ds.get('PatientID', default='')
                    PatientIdentityRemoved = ds.get('PatientIdentityRemoved', default='')
                    PatientName = ds.get('PatientName', default='')
                    PatientPosition = ds.get('PatientPosition', default='')
                    PatientSex = ds.get('PatientSex', default='')
                    PatientSize = ds.get('PatientSize', default='')
                    PatientWeight = ds.get('PatientWeight', default='')
                    TreatmentResponse = responses.get(patient, None)
                    
                    meta_info.append((file_name, PatientAge, PatientBirthDate, PatientID, PatientIdentityRemoved,
                                    PatientName, PatientPosition, PatientSex, PatientSize, PatientWeight, TreatmentResponse))
                    with open("Meta_Info.csv", "a") as info:
                        info.write(f"{file_name},{PatientAge},{PatientBirthDate},{PatientID},{PatientIdentityRemoved},{PatientName},{PatientPosition},{PatientSex},{PatientSize},{PatientWeight},{TreatmentResponse}\n")
                
                except Exception as err:
                    print(f"\t\t\t**Error encountered at -> {file_name}")
                    tb = "".join(traceback.TracebackException.from_exception(err).format())
                    with open("Logs.txt", "a") as log:
                        log.write(f"{tb}\n{'-'*80}\n")
            # sys.exit()

            print(f"\t\tTime elapsed since start -> {datetime.now() - start_time}")
    
    print(f"No. of Images found -> {count}")
    print()

print("Total No. of Images ->", len(meta_info))
df = pd.DataFrame(meta_info, columns=['File Name', 'Patient Age', 'Patient Birth Date', 'Patient ID', 'Patient Identity Removed',
                                       'Patient Name', 'Patient Position', 'Patient Sex', 'Patient Size', 'Patient Weight', 'Response'])
df.to_csv('Image_Info.csv', index=False)
print(f"Total Time Taken -> {datetime.now() - start_time}")