import pandas as pd

df = pd.read_excel("1.xlsx", engine="openpyxl")
df.to_excel("text1.xlsx")
