

import flet as ft

table = """
## Programm 

### Versionsnummer: 0.2.

## Entwickler Credits:
---
### Frontend-Design:
- name
- name

### Ki-Logic:

- name

### MCR:

- name


        """

# ist nur als reminder wie github warning oder einbettungen gehen
#| :exclamation:  This is very important   |
#|-----------------------------------------|

class Infoseite(ft.Column):
    def __init__(self):
        super().__init__()

               
        self.markdown = ft.Markdown(table,selectable=True,extension_set="gitHubWeb")
        self.scroll = True
        
        self.controls = [self.markdown]    
    
    
    def did_mount(self):
        self.height = self.page.height
        self.update()