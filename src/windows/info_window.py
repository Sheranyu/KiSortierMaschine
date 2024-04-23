

import flet as ft

table = """


        """



class Infoseite(ft.Column):
    def __init__(self):
        super().__init__()

               
        self.markdown = ft.Markdown(table,selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
        self.scroll = True
        
        self.controls = [self.markdown]    
    
    
    def did_mount(self):
        self.height = self.page.height
        self.update()