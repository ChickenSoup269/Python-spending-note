from imports import *

#  Tính năng đang phát triển
def language_menu():
    languages = [
        "Tiếng Việt",
        "English",
        "Quay lại"
    ]

    language_question = [
        inquirer.List(
            'language_choice',
            message="Chọn ngôn ngữ:",
            choices=languages
        )
    ]

    language_answer = inquirer.prompt(language_question)

    if language_answer['language_choice'] == "Quay lại":
        print("Quay lại menu cài đặt.")
   
    else:
        selected_language = language_answer['language_choice']
        print(f"Đã chuyển sang ngôn ngữ: {selected_language}")

        # save_language_settings(selected_language)