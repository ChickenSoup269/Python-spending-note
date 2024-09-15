from imports import *
from theme.Other.themeDefault import theme_menu
# from settings.language_menu import language_menu
from settings.reset_terminal import reset_terminal

def settings_menu():
    settings_options = [
        "Cài đặt theme",
        # "Ngôn ngữ",
        "Reset terminal",
        "Quay lại"
    ]

    settings_question = [
        inquirer.List(
            'settings_choice',
            message="Chọn cài đặt:",
            choices=settings_options
        )
    ]

    settings_answer = inquirer.prompt(settings_question)

    if settings_answer['settings_choice'] == "Cài đặt theme":
        theme_menu()
    # elif settings_answer['settings_choice'] == "Ngôn ngữ":
    #     language_menu() 
    elif settings_answer['settings_choice'] == "Reset terminal":
        reset_terminal() 
    else:
        print("Quay lại menu chính.")