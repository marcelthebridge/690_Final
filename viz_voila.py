from collections import Counter

import pandas as pd
import plotly.express as px
import requests
from IPython.display import display
from IPython.html import widgets
from google.colab import drive

drive.mount('/content/drive')

def h_bar(df, title, names, savefile):
  fig = px.bar(df, x=sorted(df['count']), y=df[names], orientation='h',
               color=df['count'],
               color_continuous_scale=px.colors.sequential.Viridis
               )

  fig.show()

  fig.write_html('/content/drive/MyDrive/EcoMap/Viz/'+city+savefile+'_hbar.html', include_plotlyjs = 'cdn' )

def pie_chart(df, title, names, savefile):
# , width=1000, height=800,
  fig = px.pie(df, values='count', names=names, title=title, color=df['count'],color_discrete_sequence=px.colors.qualitative.Vivid)
  fig.update_traces(textfont_size=15, textposition='outside',textinfo='percent+label')

  fig.show()
  fig.write_html('/content/drive/MyDrive/EcoMap/Viz/'+city+savefile+'_pie.html', include_plotlyjs = 'cdn')


def get_bases(map, base_id, col_clean):
    table_name = 'Resources'
    tableurl = "https://api.airtable.com/v0/meta/bases/" + base_id + "/tables"
    url = "https://api.airtable.com/v0/" + base_id + '/' + table_name
    api_key = 'key7agJ92G5p6P5bU'
    headers = {'Authorization': 'Bearer ' + api_key}
    response = requests.get(url, headers=headers)
    params = ({'view': 'API Call'})
    airtable_records = []
    run = True

    while run is True:
        response = requests.get(url, params=params, headers=headers)
        airtable_response = response.json()
        airtable_records += (airtable_response['records'])
        if 'offset' in airtable_response:
            run = True
            params = (('offset', airtable_response['offset']),)
        else:
            run = False

    airtable_rows = []
    for records in airtable_records:
        airtable_rows.append(records['fields'])
    df = pd.DataFrame(airtable_rows)
    df = df.fillna('0')
    return (df)

    df.to_csv('/content/drive/MyDrive/EcoMap/Data/' + map + '.csv')

split = lambda x: pd.Series(str(x).split(';'))

def get_counts(map, count_list):

  df = pd.read_csv('/content/drive/MyDrive/EcoMap/Data/'+map+'.csv')
  writer = pd.ExcelWriter('/content/drive/MyDrive/EcoMap/Data/'+map+'_counts.xlsx')

  for col in count_list:
    temp = df[col].apply(split)
    temp_clean = []

    for i, r in temp.iterrows():
      for x in range(len(r)):
        if r[x] == 0 or r[x] is None:
          pass
        else:
          temp_clean.append(r[x])
      counted = Counter(temp_clean)
      temp_list = pd.DataFrame(counted.items(), columns=[col, 'count'])
      temp_list = temp_list[temp_list[col]!='0'].dropna()

    temp_list.to_excel(writer, sheet_name=col, index=False)

  writer.save()

for m in maps:
  df= get_bases(m[0], m[1], m[2])
  for col in m[2]:
    df[col] = [';'.join(map(str,l)) for l in df[col]]
  df.to_csv('/content/drive/MyDrive/EcoMap/Data/'+m[0]+'.csv')

  get_counts(m[0], m[3])

map_dict={'Baltimore':['Resource Type','Tags','Venture Types','Industry Groups Format','Industry','Stage','Audience','Subtype','Category','New Type'],
           'Dallas':['Resource Type','Subtypes','Venture Types','Industry Groups','Industry','Stage','Founder Type'],
      'Birmingham': ['Resource Type','Tags','Venture Types','Industry Groups Format','Industry','Stage','Recurrence Timeline','Subtype','Founder Type']}

def print_field(field):
    print(field)

def select_map(map):
    field_w.options = map_dict[map]

def h_bar(map, field):
  df = pd.read_excel('/content/drive/MyDrive/EcoMap/Data/'+map+'_counts.xlsx', sheet_name=field)
  df = df.sort_values(by='count')
  fig = px.bar(df, x=sorted(df['count']), y=df[field], orientation='h',
               color=df['count'],
               color_continuous_scale=px.colors.sequential.Viridis
               )

  fig.show()

map_w = widgets.Dropdown(options=map_dict.keys())
init = map_w.value
field_w = widgets.Dropdown(options=map_dict[init])

eco_mapper = widgets.interactive(h_bar, map=map_w, field=field_w)
j = widgets.interactive(print_field, field=field_w)
i = widgets.interactive(select_map, map=map_w)
#display(i)
#display(j)
display(eco_mapper)