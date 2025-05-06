# innovaccer
Innovaccer Internship

I first inspected the SyntheticMass Data, Version 2 (24 May, 2017) datasets. I created a script which checked whether the SNOMED diagnosis codes for CKD Stages 1 through 5 existed. I discovered through testing (at the bottom of my code), that there were 0 occurrences of these codes among all 12 CSV files given.

I discovered that there were only two relevant codes regarding renal disease in these datasets. Specifically, '127013003 - Diabetic renal disease' and '46177005 - End Stage Renal Disease'. However, '127013003 - Diabetic renal disease' is not relevant as it is not a CKD stage of interest.

At this point, it is not possible to find the time period in days (mean and median) for patients to go from Stage 1 to 2, Stage 2 to 3,..., to End stage renal disease. However, I decided to implement the script regardless and see if I could find the time period in days for patients to go from Stage 1 to End stage renal disease. My results showed that no time periods could be found, as expected.

I wanted to inspect the dataset even further, and identified a specific patient ID with 46177005 - End Stage Renal Disease. After testing, I discovered that this patient did not have other relevant codes across all CSV files besides 127013003 - Diabetic renal disease.

Conclusion: Without the relevant codes, there is no possibility of finding the time period in days for patients to go from Stage 1 to End stage renal disease.
