import os
import pandas as pd
from datetime import datetime
from collections import defaultdict
import numpy as np

# SNOMED codes
CKD_stage_1 = '431856005'
end_stage   = '46177005'

# These stages are NOT present in SyntheticMass Data, Version 2 (24 May, 2017)
# stage_2     = '431856006'
# stage_3     = '433144002'
# stage_3a    = '700378005'
# stage_3b    = '700379002'
# stage_4     = '431857002'
# stage_5     = '433146000'

path = '/Users/jiro/Desktop/syntheticmass_data'

# Dictionary to store patient events
# Format: {patient_id: {'stage1': [dates], 'esrd': [dates]}}
patient_events = defaultdict(lambda: {'stage1': [], 'esrd': []})

# Loop through all output directories
for i in range(1, 13):
    file_path = os.path.join(path, f'output_{i}', 'csv', 'conditions.csv')
    if not os.path.exists(file_path):
        continue

    df = pd.read_csv(file_path, usecols=['PATIENT', 'CODE', 'START'])
    df['CODE'] = df['CODE'].astype(str).str.strip()

    df = df[df['CODE'].isin([CKD_stage_1, end_stage])]
    df['START'] = pd.to_datetime(df['START'], format='%m/%d/%y', errors='coerce')
    df = df.dropna(subset=['START'])

    # Split stage 1 and ESRD entries
    stage1_df = df[df['CODE'] == CKD_stage_1]
    esrd_df = df[df['CODE'] == end_stage]

    # Group and store earliest dates
    for patient_id, group in stage1_df.groupby('PATIENT'):
        earliest = group['START'].min()
        patient_events[patient_id]['stage1'].append(earliest)

    for patient_id, group in esrd_df.groupby('PATIENT'):
        earliest = group['START'].min()
        patient_events[patient_id]['esrd'].append(earliest)

# Calculate time differences in days
time_deltas = []

for patient_id, events in patient_events.items():
    if events['stage1'] and events['esrd']:
        # Use the earliest dates
        stage1_date = min(events['stage1'])
        esrd_date = min(events['esrd'])
        delta = (esrd_date - stage1_date).days
        if delta >= 0:
            time_deltas.append(delta)


# Calculate mean and median
if time_deltas:
    mean_days = np.mean(time_deltas)
    median_days = np.median(time_deltas)
    print(f"Mean time from Stage 1 to ESRD: {mean_days:.2f} days")
    print(f"Median time from Stage 1 to ESRD: {median_days:.2f} days")
else:
    print("No patient transitions found from Stage 1 to ESRD.")


# # Test: Check if CKD stages 1-5 exist in given dataset
# # Conclusion: SNOMED codes for CKD stages 1-5 do not exist in given dataset

# # Target CKD codes and their descriptions
# target_codes = {
#     '431856005': 'Chronic kidney disease stage 1',
#     '431856006': 'Chronic kidney disease stage 2',
#     '433144002': 'Chronic kidney disease stage 3',
#     '700378005': 'Chronic kidney disease stage 3A',
#     '700379002': 'Chronic kidney disease stage 3B',
#     '431857002': 'Chronic kidney disease stage 4',
#     '433146000': 'Chronic kidney disease stage 5'
# }

# path = '/Users/jiro/Desktop/syntheticmass_data'
# code_counts = defaultdict(int)

# for i in range(1, 13):
#     file_path = os.path.join(path, f'output_{i}', 'csv', 'conditions.csv')
#     if not os.path.exists(file_path):
#         continue

#     try:
#         df = pd.read_csv(file_path, usecols=['CODE'], dtype=str)
#         df['CODE'] = df['CODE'].str.strip()  # Clean leading/trailing spaces

#         for code in target_codes:
#             code_counts[code] += (df['CODE'] == code).sum()
#     except Exception as e:
#         print(f"Error reading {file_path}: {e}")

# print("CKD Code Occurrences Across All Files:")
# for code, label in target_codes.items():
#     print(f"{code} – {label}: {code_counts[code]} occurrences")



# # Test: Check what codes exist for a patient with end stage renal disease
# # Conclusion: Patient does not have any other SNOMED codes besides code for ESRD

# # Target patient ID
# target_patient = '2dcf495c-f71e-4d3c-af17-a281d0830299'
# path = '/Users/jiro/Desktop/syntheticmass_data'

# all_codes = set()

# # Loop through all output folders
# for i in range(1, 13):
#     file_path = os.path.join(path, f'output_{i}', 'csv', 'conditions.csv')
#     if not os.path.exists(file_path):
#         continue

#     df = pd.read_csv(file_path, usecols=['PATIENT', 'CODE', 'START'])
#     patient_df = df[df['PATIENT'] == target_patient]

#     if not patient_df.empty:
#         print(f"\nFound records in output_{i}:")
#         print(patient_df[['CODE', 'START']])
#         all_codes.update(patient_df['CODE'].unique())

# # Print all unique codes found
# print("\nAll unique CODE values for patient:")
# for code in sorted(all_codes):
#     print(code)