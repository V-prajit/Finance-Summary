import pandas as pd
file_path = 'Chase6686_Activity_20240620.CSV'
df = pd.read_csv(file_path)

colums_to_check = ['Details', 'Posting Date', 'Description', 'Amount', 'Type', 'Balance', 'Check or Slip #']

duplicates = df[df.duplicated(subset=colums_to_check, keep = False)]

if not duplicates.empty:
    print("duplicates dound")
    print(duplicates)
else:
    print("No duplicates")
