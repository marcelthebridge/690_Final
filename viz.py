from collections import Counter
import pandas as pd
import plotly.express as px


def h_bar(df, title, names, savefile):
  fig = px.bar(df, x=sorted(df['count']), y=df[names], orientation='h',
               color=df['count'],
               color_continuous_scale=px.colors.sequential.Viridis
               )

  fig.show()

def pie_chart(df, title, names, savefile):
  # , width=1000, height=800,
  fig = px.pie(df, values='count', names=names, title=title, color=df['count'],
               color_discrete_sequence=px.colors.qualitative.Vivid)
  fig.update_traces(textfont_size=15, textposition='outside', textinfo='percent+label')

  fig.show()

countlist = ['County', 'Category', 'Type', 'General', 'Industry', 'Audience', 'Stage', 'Venture']
df = pd.read_csv('./Project2Data.csv')
writer = pd.ExcelWriter('./counts.xlsx')

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

map_dict={'Resource':['County','Category','Type','General','Industry','Audience','Stage','Venture']}

def print_field(field):
    print(field)

def select_map(map):
    field_w.options = map_dict[map]

def h_bar(map, field):
  df = pd.read_csv('./counts.xlsx')
  df = df.sort_values(by='count')
  fig = px.bar(df, x=sorted(df['count']), y=df[field], orientation='h',
               color=df['count'],
               color_continuous_scale=px.colors.sequential.Viridis
               )

  fig.show()






map_w = widgets.Dropdown(options=map_dict.keys())
init = map_w.value
field_w = widgets.Dropdown(options=map_dict[init])
sx
eco_mapper = widgets.interactive(h_bar, map=map_w, field=field_w)
j = widgets.interactive(print_field, field=field_w)
i = widgets.interactive(select_map, map=map_w)
display(eco_mapper)