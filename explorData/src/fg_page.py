import justpy as jp
import pandas as pd

import matplotlib.pyplot as plt


df = pd.read_parquet('202207261319_processed_enterprise.parquet')

my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
my_button_style = "inline-block px-6 py-2 border-2 border-blue-600 text-blue-600 font-medium text-xs leading-tight uppercase rounded-full hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out"

def click_home(self, msg):
    msg.page.redirect = '/'

def click_schema(self, msg):
    msg.page.redirect = '/schema'

def get_home_div(wp: jp.WebPage, on_click):
    nav = jp.Nav(classes="relative w-full flex flex-wrap items-center justify-between \
        py-3 bg-gray-900 text-gray-200 shadow-lg navbar navbar-expand-lg navbar-light",\
            a=wp)
    nav.add(jp.Div(classes='container-fluid w-full flex flex-wrap items-center justify-between px-6'))
    nav.add(jp.Button(text='Home', onclick=on_click))
    return nav

@jp.SetRoute('/')
def root_event(): 
    button_classes = 'w-32 mr-2 mb-2 bg-gray-500 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-full'
    wp = jp.WebPage()
    home_div_bar = get_home_div(wp, click_home)
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    b = jp.Button(text='Go2Schema', a=button_div,
                  classes=button_classes, click=click_schema)
    return wp


@jp.SetRoute('/schema')
def print_schema():
    wp = jp.WebPage(title='FG')
    home_div_bar = get_home_div(wp, click_home)
    _df = df.loc[:, ['Regione', 'Provincia',
                     'Ragione Sociale', 'Sede Legale', 'Attività']]
    grid = _df.jp.ag_grid(a=wp)
    grid.options.pagination = True
    grid.options.paginationAutoPageSize = True
    grid.options.columnDefs[0].cellClass = [
        'text-white', 'bg-blue-500', 'hover:bg-blue-200']
    for col_def in grid.options.columnDefs[1:]:
        col_def.cellClassRules = {
            'font-bold': 'x < 20',
            'bg-red-300': 'x < 20',
            'bg-yellow-300': 'x >= 20 && x < 50',
            'bg-green-300': 'x >= 50'
        }
    return wp

jp.justpy(port=5010)
