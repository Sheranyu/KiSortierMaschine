import flet as ft


def main(page: ft.Page):
    def handle_change(e):
        print("on_change data : " + str(e.data))
        print(e.data)

    page.add(
        ft.SegmentedButton(
            on_change=handle_change,
            selected_icon=ft.Icon(ft.icons.ONETWOTHREE),
            selected={"1", "4"},
            allow_multiple_selection=True,
            segments=[
                ft.Segment(
                    value="1",
                    label=ft.Text("1"),
                    icon=ft.Icon(ft.icons.LOOKS_ONE),
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("2"),
                    icon=ft.Icon(ft.icons.LOOKS_TWO),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("3"),
                    icon=ft.Icon(ft.icons.LOOKS_3),
                ),
                ft.Segment(
                    value="4",
                    label=ft.Text("4"),
                    icon=ft.Icon(ft.icons.LOOKS_4),
                ),
            ],
        )
    )


ft.app(target=main)