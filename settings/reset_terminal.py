from imports import *

def reset_terminal():
    confirm_reset = [
        inquirer.Confirm(
            'confirm',
            message="Bạn có muốn reset?",
            default=False
        )
    ]

    answer = inquirer.prompt(confirm_reset)

    if answer['confirm']:
        if os.name == 'nt':  
            os.system('cls')
            os.system('python3 main.py')

        print("Terminal đã được reset. Chương trình sẽ khởi động lại...")
        exit()

    else:
        print("Reset đã bị hủy.")