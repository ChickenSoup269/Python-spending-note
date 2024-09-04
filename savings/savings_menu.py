from savings import *

# Menu tiết kiệm
def savings_menu():
    while True:
        savings_choices = [
            "Thêm tiền tiết kiệm",
            "Sử dụng tiền tiết kiệm",
            "Xem tổng tiền tiết kiệm",
            "Cập nhật tiền tiết kiệm",
            "Quay lại"
        ]

        savings_questions = [
            inquirer.List(
                'savings_choice',
                message=5 * '*' + " Chọn chức năng bạn muốn thực hiện " + 5 * '*',
                choices=savings_choices,
            )
        ]

        savings_answer = inquirer.prompt(savings_questions)

        if savings_answer['savings_choice'] == "Thêm tiền tiết kiệm":
            amount = int(input("Nhập số tiền tiết kiệm (VNĐ): "))
            description = input("Mô tả: ")
            add_savings(amount,description)

        elif savings_answer['savings_choice'] == "Sử dụng tiền tiết kiệm":
            apply_savings()

        elif savings_answer['savings_choice'] == "Xem tổng tiền tiết kiệm":
            display_savings_book()

        elif savings_answer['savings_choice'] == "Cập nhật tiền tiết kiệm":
            update_savings()

        elif savings_answer['savings_choice'] == "Quay lại":
            break
