from savings import *

# Cập nhật tiền tiết kiệm
def update_savings():
    if not savings:
        print(Fore.RED + "Không có tiền tiết kiệm nào để cập nhật." + Style.RESET_ALL)
        return

    # In danh sách các ngày có trong savings để người dùng chọn
    dates = list(savings.keys())
    date_question = [
        inquirer.List(
            'selected_date',
            message="Chọn ngày bạn muốn cập nhật số tiền tiết kiệm:",
            choices=dates,
        )
    ]

    date_answer = inquirer.prompt(date_question)
    selected_date = date_answer['selected_date']

    # Lấy số tiền mới từ người dùng
    new_amount = int(input(f"Nhập số tiền tiết kiệm mới cho ngày {selected_date} (VNĐ): "))

    # Cập nhật số tiền tiết kiệm
    savings[selected_date]["amount"] = new_amount

    # Lưu lại thay đổi
    save_expenses()

    print(Fore.GREEN + f"Số tiền tiết kiệm cho ngày {selected_date} đã được cập nhật thành {new_amount:,} VNĐ." + Style.RESET_ALL)
