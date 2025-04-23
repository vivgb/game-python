import flet as ft 
from flet import *

def main(page: ft.Page):
    page.title = "Dropdown"
    page.window_width=400
    page.window_height=400
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    
    
    dd = ft.Dropdown(
         width=300,
         #
         label="Color",
         hint_text="Choose",
         #texto
         
         options=[
             ft.dropdown.Option("Red"),
             ft.dropdown.Option("Green"),
             ft.dropdown.Option("Blue")
         ],
         #cor dos negocio e dos botoes
         filled=True,
         bgcolor="#28C468",
         color="#ABC428",
         
         #borda
         border=border.all(10,"3DA9C8")
         
         #outro tipo de borda mais aredondada
         #border_radius=border_radius.only(20,50,20,50)
         
         
         
         
     )
    page.add(dd)
    
    
    page.update()
    
ft.app(target=main)