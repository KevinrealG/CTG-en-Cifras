## Import data
import pandas as pd
url='base de dinamica.xlsx'
df = pd.read_excel(url,sheet_name='estructura',header=0)
X=df.drop(['Número de Empleados','Activos','Ingresos'],axis=1)
X.to_csv('circle_data.csv',encoding='utf-8')
## Get categorical column names
cat_list = []

for col in df.columns:
  if df[col].dtype == object:
    cat_list.append(col)

## Get all possible levels of every categorical variable and number of data points in each level
cat_levels = {}

for col in cat_list:
  levels = df[col].value_counts().to_dict()
  cat_levels[col] = levels

## Convert nested dictionary to dataframe
nestdict = pd.DataFrame(cat_levels).stack().reset_index()

nestdict.columns = ['Level', 'Category', 'Population']

## Output data to file
nestdict.to_csv("nested_dict.csv")

## Preview dataframe
nestdict.head()
