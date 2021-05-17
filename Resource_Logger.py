import io
import json

import pandas as pd
import requests
from ipywidgets import *


class EcoMap:
    def __init__(self):
        self.Title = widgets.HTML("EcoMap Table Builder")

        self.file_load = FileUpload(accept=".csv", multiple=False)
        # self.download = Button(description = 'CSV ')
        # self.download.on_click

        # New Record
        self.header = widgets.HTML("New Record Info:")
        self.Name = Text(description='Resource Name:', style={'description_width': 'initial'})
        self.County = ToggleButtons(description='County:', options=['None', 'Allegany', 'Anne Arundel',
                                                                    'Baltimore City', 'Baltimore',
                                                                    'Calvert', 'Caroline',
                                                                    'Carrol', 'Cecil', 'Charles',
                                                                    'Dorchester', 'Frederick',
                                                                    'Garret', 'Harford',
                                                                    'Howard', 'Kent', 'Montgomery',
                                                                    'Prince George\'s', 'Queen Anne\'s',
                                                                    'Somerset', 'St. Mary\'s',
                                                                    'Talbot', 'Wicomic', 'Worcester'],
                                    tooltips=['None', 'Allegany', 'Anne Arundel',
                                              'Baltimore City', 'Baltimore',
                                              'Calvert', 'Caroline',
                                              'Carrol', 'Cecil', 'Charles',
                                              'Dorchester', 'Frederick',
                                              'Garret', 'Harford',
                                              'Howard', 'Kent', 'Montgomery',
                                              'Prince George\'s', 'Queen Anne\'s',
                                              'Somerset', 'St. Mary\'s',
                                              'Talbot', 'Wicomic', 'Worcester'],
                                    button_style='')
        self.Category = ToggleButtons(description='Category:', button_style='', options=['None', 'Events and Networks',
                                                                                         'Structured Progreams',
                                                                                         'Tools and Funding'])
        self.Type = ToggleButtons(description='Type:', button_style='', options=['None', 'Accelerator', 'Bootcamp',
                                                                                 'Competitions', 'Digital Tool',
                                                                                 'Educational Program', 'Fellowship',
                                                                                 'Funding', 'Incubator', 'Large Event',
                                                                                 'Media Source', 'Network',
                                                                                 'Registration', 'Showcase',
                                                                                 'Small Event',
                                                                                 'Space', 'Talent Source',
                                                                                 'Technical Assistance'],
                                  tooltips=['None', 'Accelerator', 'Bootcamp',
                                            'Competitions', 'Digital Tool',
                                            'Educational Program', 'Fellowship',
                                            'Funding', 'Incubator', 'Large Event',
                                            'Media Source', 'Network',
                                            'Registration', 'Showcase', 'Small Event',
                                            'Space', 'Talent Source',
                                            'Technical Assistance'])
        self.General = ToggleButtons(description='General:', button_style='',
                                     options=['None', 'Corporate-Sponsored', 'COVID-Specific',
                                              'Discounted', 'Free',
                                              'Government Funded', 'In-Person',
                                              'Modified Due to COVID', 'Open to Public',
                                              'Paid', 'Promotional Opportunities',
                                              'University-Affiliated', 'Virtual',
                                              'Volunteering'],
                                     tooltips=['None', 'Corporate-Sponsored', 'COVID-Specific',
                                               'Discounted', 'Free',
                                               'Government Funded', 'In-Person',
                                               'Modified Due to COVID', 'Open to Public',
                                               'Paid', 'Promotional Opportunities',
                                               'University-Affiliated', 'Virtual',
                                               'Volunteering'])
        self.Industry = ToggleButtons(description='Industry:', button_style='',
                                      options=['None', 'Arts, Media, and Entertainment',
                                               'Community and Economic Development',
                                               'Construction and Real Estate',
                                               'Energy, Sustainability, and Agriculture',
                                               'Finance, Insurance, and Business Services',
                                               'Food, Drink, and Hospitality',
                                               'Government, Defense, and Aerospace',
                                               'Healthcare and Life Sciences',
                                               'Industry Agnostic',
                                               'Infrastructure, Utilities, and Mining',
                                               'Management, Law, and Policy',
                                               'Manufacturing and Advanced Materials',
                                               'Recreation, Fitness, and Tourism',
                                               'Retail, Product, and Personal Services',
                                               'Social Impact, Education, and Youth',
                                               'Technology, IT, and Cybersecurity',
                                               'Transportation, Wholesale, and Logistics'],
                                      tooltips=['None', 'Arts, Media, and Entertainment',
                                                'Community and Economic Development',
                                                'Construction and Real Estate',
                                                'Energy, Sustainability, and Agriculture',
                                                'Finance, Insurance, and Business Services',
                                                'Food, Drink, and Hospitality',
                                                'Government, Defense, and Aerospace',
                                                'Healthcare and Life Sciences',
                                                'Industry Agnostic',
                                                'Infrastructure, Utilities, and Mining',
                                                'Management, Law, and Policy',
                                                'Manufacturing and Advanced Materials',
                                                'Recreation, Fitness, and Tourism',
                                                'Retail, Product, and Personal Services',
                                                'Social Impact, Education, and Youth',
                                                'Technology, IT, and Cybersecurity',
                                                'Transportation, Wholesale, and Logistics'])
        self.Audience = ToggleButtons(description='Audience:', button_style='',
                                      options=['None', 'All Entrepreneurs', 'Black Founders',
                                               'Ecosystem Builders', 'Faculty',
                                               'Female Founders', 'Founders of Color',
                                               'Founders with Disabilities',
                                               'Immigrant Founders', 'LatinX Founders',
                                               'LGBTQIA Founders',
                                               'Previously Incarcerated Founders',
                                               'Students', 'Underserved Founders',
                                               'University Affiliates', 'Veteran Founders',
                                               'Youth'],
                                      tooltips=['None', 'All Entrepreneurs', 'Black Founders',
                                                'Ecosystem Builders', 'Faculty',
                                                'Female Founders', 'Founders of Color',
                                                'Founders with Disabilities',
                                                'Immigrant Founders', 'LatinX Founders',
                                                'LGBTQIA Founders',
                                                'Previously Incarcerated Founders',
                                                'Students', 'Underserved Founders',
                                                'University Affiliates', 'Veteran Founders',
                                                'Youth'])
        self.Stage = ToggleButtons(description='Stage:', button_style='',
                                   options=['None', 'Early', 'Growth', 'Idea', 'Mature'],
                                   tooltips=['None', 'Early', 'Growth', 'Idea', 'Mature'])
        self.Venture = ToggleButtons(description='Venture:', button_style='',
                                     options=['None', 'All Venture Types', 'COVID-Impacted',
                                              'Creative Ventures', 'Event or Experience Ventures',
                                              'Growth Startups', 'Nonprofit Organizations',
                                              'Product-based Ventures',
                                              'Restaurants or Food Service',
                                              'Retail or Main Street Stores',
                                              'Service-based Ventures',
                                              'Social Enterprises', 'Technology-Based Ventures',
                                              'Traditional Businesses'],
                                     tooltips=['None', 'All Venture Types', 'COVID-Impacted',
                                               'Creative Ventures', 'Event or Experience Ventures',
                                               'Growth Startups', 'Nonprofit Organizations',
                                               'Product-based Ventures',
                                               'Restaurants or Food Service',
                                               'Retail or Main Street Stores',
                                               'Service-based Ventures',
                                               'Social Enterprises', 'Technology-Based Ventures',
                                               'Traditional Businesses'])

        self.submit = Button(description='Submit Records', tooltip='Click to Submit',
                             layout=Layout(width='50%', height='50px'))
        self.submit.on_click(self.submit_data)
        self.tab = Tab(layout=Layout(height='666px'))
        self.enter = widgets.HTML('Date Entered')
        self.enter.layout.visibility = 'hidden'

        # load it up

        # layout Record
        self.file_load = HBox([self.file_load])
        self.topper = VBox([self.header, self.file_load, self.header])
        self.columnL = VBox([self.Name, self.County, self.Category, self.Type, self.General])
        self.columnR = VBox([self.Industry, self.Audience, self.Stage, self.Venture, self.submit])
        self.Input_Data = AppLayout(header=self.topper,
                                    left_sidebar=self.columnL,
                                    right_sidebar=self.columnR)

        self.tab.children = [self.Input_Data]
        # self.tab.children=[self.]
        self.tab.set_title(0, 'Record Entry')
        self.container = VBox([self.Title, self.tab])

    def submit_data(self, btn):
        try:
            upload_file = self.file_load.value
            file_content = upload_file[str(list(upload_file.keys())[0])]['content']
            data = pd.read_csv(io.BytesIO(file_content))
            print(data)
            json1 = data.to_json(orient="columns")
            print(json1)
            r = requests.put('http://127.0.0.1:5000/submitdata', data=json1)
        except:
            schema_dict = dict(
                {'Name': [self.Name.value], 'County': [self.County.value], 'Category': [self.Category.value],
                 'Type': [self.Type.value], 'General': [self.General.value], 'Industry': [self.Industry.value],
                 'Audience': [self.Audience.value], 'Stage': [self.Stage.value], 'Venture': [self.Venture.value]})
            json1 = json.dumps(schema_dict, skipkeys=True)
            r = requests.put('http://localhost:5000/submitdata', data=json1)
        self.submitted.layout.visibility = 'visible'

    def get_layout(self):
        return self.container


app = EcoMap()
app.get_layout()