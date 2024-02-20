import flet as ft

def main(page: ft.Page):
    def add_clicked(e):
        tasks_view.controls.append(ft.Checkbox(label=Task_field.value))
        tasks_view.controls.append(ft.Checkbox(label=Task_field.value))
        Task_field.value = ""
        view.update()

    Task_field = ft.TextField(hint_text="Whats needs to be done?", expand=True)
    tasks_view = ft.Column()
    
    button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked)
   
    rowdata =  ft.Row(controls=[Task_field, button])

    view=ft.Column(
        width=600,
        controls=[
        rowdata,
        ft.Column(controls=[tasks_view])],
    )
    container = ft.Container(content=view, bgcolor=ft.colors.BLUE_GREY_900)

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(container)

ft.app(target=main)