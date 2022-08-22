from genericpath import isdir
import os
import base64
import pathlib

import justpy as jp
import pandas as pd

from wasabi import msg as Wmsg


### BASE TEST

def download_test():
    wp = jp.WebPage()
    in1 = jp.Input(type='file', classes=jp.Styles.input_classes, a=wp, multiple=True, change=file_input)
    in1.file_div = jp.Div(a=wp)
    return wp

def file_input(self, msg):
    self.file_div.delete_components()
    for f in msg.files:
        jp.Div(text=f'{f.name} | {f.size} | {f.type} | {f.lastModified} | {f.file_content}', a=self.file_div, classes='font-mono m-1 p-2')

class DF(jp.A):

    def __init__(self, **kwargs):
        self.downloaded = True
        super().__init__(**kwargs)
        self.target = '_blank'
        self.df = None
        self.style = 'height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;'
    
    def react(self, data):
        Wmsg.good(f'DF react called with {self.file_path} file path ...')
        self.file_path = pathlib.Path(self.file_path)
        self.df = pd.read_csv(self.file_path, on_bad_lines='warn') if self.file_path.suffix == '.csv' else pd.read_parquet(self.file_path, engine='pyarrow')
        Wmsg.good(self.df.head(1))
        grid = self.df.jp.ag_grid(a=self)
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

    
def df_submit(self, msg):
    sess = msg.session_id
    # create session directory, if not yet created
    pathlib.Path(msg.session_id).mkdir(exist_ok=True)
    # find the element contained the file and write it to the server
    for c in msg.form_data:
        if c.type == 'file':
            break
    for f in c.files:
        with open(f'{sess}/{f.name}', 'wb') as ff:
            ff.write(base64.b64decode(f.file_content))

    file_ls = os.listdir(sess)
    if len(file_ls):
        for f in file_ls:
            Wmsg.good(f'Showing uploaded df: {f}')
            DF(file_path=f'{sess}/{f}', a=self.df_div)
    else:
        jp.Div(text='No files uploaded yet.', a=self.df_div, classes='text--3xl')
        

def upload_home(request):
    wp = jp.WebPage()
    df_div = jp.Div(a=wp, classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start', style='height: 80vh')

    sess = request.session_id
    # show already uploaded files, if any.
    if os.path.isdir(sess):
        file_ls = os.listdir(sess)
        for f in file_ls:
            # df component: show a df grid.
            Wmsg.good(f'Showing already uploaded df: {f}')
            DF(file_path=f'{sess}/{f}', a=df_div)
    else:
        jp.Div(text='No files uploaded yet.', a=df_div, classes='text--3xl')

    ### Define form
    form = jp.Form(a=wp, method='post', enctype='multipart/form-data', submit=df_submit)
    form.df_div = df_div
    jp.Input(type='file', classes=jp.Styles.input_classes, a=form, multiple=True, accept='.csv, .parquet, .xls, .xlsx')
    jp.Button(type='submit', text='Upload', classes=jp.Styles.button_simple, a=form)
    return wp

def print_schema(df):
    wp = jp.WebPage(title='FG')
    grid = df.jp.ag_grid(a=wp)
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





def run_df_upload():
    jp.justpy(upload_home, port=5010, websocket=False)

def run_base_upload():
    jp.justpy(download_test, port=5010)
