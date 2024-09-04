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

    # Hiển thị các khoản tiết kiệm trong ngày đã chọn
    savings_list = savings[selected_date]
    if len(savings_list) > 1:
        # Nếu có nhiều khoản tiết kiệm, cho người dùng chọn khoản cần cập nhật
        savings_choices = [
            f"[{i}] {entry['description']} - {entry['amount']} VNĐ"
            for i, entry in enumerate(savings_list)
        ] + ["Quay lại"]

        savings_question = [
            inquirer.List(
                'selected_savings',
                message="Chọn khoản tiết kiệm bạn muốn cập nhật:",
                choices=savings_choices,
            )
        ]

        savings_answer = inquirer.prompt(savings_question)
        if savings_answer['selected_savings'] == "Quay lại":
            return

        selected_index = int(savings_answer['selected_savings'].split(']')[0][1:])
        selected_savings = savings_list[selected_index]
    else:
        # Nếu chỉ có một khoản tiết kiệm, chọn khoản đó
        selected_savings = savings_list[0]

    # Cập nhật mô tả và số tiền mới từ người dùng
    new_description = input(f"Nhập mô tả mới cho mục '{selected_savings['description']}' (bỏ trống để giữ nguyên): ") or selected_savings['description']
    new_amount = int(input(f"Nhập số tiền tiết kiệm mới cho mục '{selected_savings['description']}' vào ngày {selected_date} (VNĐ): "))

    # Cập nhật mô tả và số tiền tiết kiệm
    selected_savings["description"] = new_description
    selected_savings["amount"] = new_amount

    # Lưu lại thay đổi
    save_expenses()

    print(Fore.GREEN + f"Mô tả và số tiền tiết kiệm cho mục '{selected_savings['description']}' vào ngày {selected_date} đã được cập nhật thành '{new_description}' và {new_amount:,} VNĐ." + Style.RESET_ALL)
