import os
import pathlib
import base64

import justpy as jp

import pandas as pd


### BASE TEST
def run_base_test():
    def download_test():
        wp = jp.WebPage()
        in1 = jp.Input(type='file', classes=jp.Styles.input_classes, a=wp, multiple=True, change=file_input)
        in1.file_div = jp.Div(a=wp)
        return wp
    
    def file_input(self, msg):
        self.file_div.delete_components()
        for f in msg.files:
            jp.Div(text=f'{f.name} | {f.size} | {f.type} | {f.lastModified} | {f.file_content}', a=self.file_div, classes='font-mono m-1 p-2')

    jp.justpy(download_test, port=5010)


# class DF(jp.A):
#     """DataFrame component definition: """

#     def __init__(self, **kwargs):
#         self.src_file = ''
#         # if True, files are downloaded, if False, they are opened in new browser tab
#         self.files_downloaded = True
#         super().__init__(**kwargs)

#     def react(self, data):
#         self.src_file = self.src_file
#         self.href = self.src_file
#         if self.files_downloaded:
#             self.file_name = self.href.split('/')[-1]
#             df = pd.read_csv(self.src_file)
#             df.jp.ag_grid(a=self.df_div)
#         self.set_classes('inline-block')

# def df_submit(self, msg):
#     # if directory for the current session does not exist create one
#     # the name of the directory is the session_id
#     session_id_path = pathlib.Path(msg.session_id)
#     session_id_path.mkdir(exist_ok=True)
#     print(msg.session_id)
#     print(msg.form_data)
#     print(msg.files)
#     # # be sure to process just file content
#     # # for c in msg.form_data:
#     # #     if c.type != 'file':
#     # #         msg.error(f'{c.type} contents are not allowed.')
#     # #         break
#     # # write the content to a file after decoding the base64 content
#     # for i, f in enumerate(msg.files):
#     #     print(f'{i} --- processing {f.name} file ...')
#     #     with open(f'{msg.session_id}/{f.name}', 'wb') as ff:
#     #         ff.write(base64.b64decode(f.file_content))

#     self.df_div.delete_components()
#     for f in msg.files:
#         return jp.Div(text=f'{f.name} | {f.size} | {f.type} | {f.lastModified}', a=self.df_div, classes='font-mono m-1 p-2')
        

    
# def upload_home(request):
#     wp = jp.WebPage()
#     df_div = jp.Div(a=wp, classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start', style='height: 80vh')
#     jp.Div(text='No files uploaded yet', a=df_div, classes='text-3xl')
    
#     f = jp.Form(a=wp, enctype='multipart/form-data', submit=df_submit)
#     f.df_div = df_div
#     jp.Input(type='file', classes=jp.Styles.input_classes, a=f, multiple=True, accept='.csv,.parquet')
#     jp.Button(type='submit', text='Upload', classes=jp.Styles.button_simple, a=f)
#     return wp


# jp.justpy(upload_home, port=5010, websockets=False)


