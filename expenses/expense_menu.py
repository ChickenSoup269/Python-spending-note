from expenses import *

def expense_menu():
    while True:
        expense_choices = [
            "Thêm chi tiêu",
            "Xóa chi tiêu",
            "Cập nhật chi tiêu",
            "Xem chi tiêu",
            "Quay lại"
        ]

        expense_questions = [
            inquirer.List(
                'choice',
                message="Chọn chức năng bạn muốn thực hiện",
                choices=expense_choices,
            )
        ]

        expense_answer = inquirer.prompt(expense_questions)

        if expense_answer['choice'] == "Thêm chi tiêu":
            print(40 * '=*=')
            add_expense()

        elif expense_answer['choice'] == "Xem chi tiêu":
            print(40 * '=*=')
            view_expenses_menu()

        elif expense_answer['choice'] == "Xóa chi tiêu":
            print(40 * '=*=')
            delete_expense()

        elif expense_answer['choice'] == "Cập nhật chi tiêu":
            print(40 * '=*=')
            edit_expense()

        elif expense_answer['choice'] == "Quay lại":
            break

# Menu xem chi tiêu
def view_expenses_menu():
    while True:
        view_expense_choices = [
            "Xem chi tiêu tuần",
            "Xem chi tiêu tháng",
            "Xem chi tiêu năm",
            "Xem chi tiêu theo năm",
            "Xem chi tiêu theo danh mục",
            "Tìm kiếm chi tiêu theo mô tả",
            "Quay lại"
        ]

        view_expense_questions = [
            inquirer.List(
                'choice',
                message="Chọn khoảng thời gian bạn muốn xem chi tiêu",
                choices=view_expense_choices,
            )
        ]

        view_expense_answer = inquirer.prompt(view_expense_questions)

        if view_expense_answer['choice'] == "Xem chi tiêu tuần":
            print(40 * '=*=')
            weekly_expenses()

        elif view_expense_answer['choice'] == "Xem chi tiêu tháng":
            print(40 * '=*=')
            monthly_expenses()

        elif view_expense_answer['choice'] == "Xem chi tiêu năm":
            print(40 * '=*=')
            yearly_expenses()

        elif view_expense_answer['choice'] == "Xem chi tiêu theo năm":
            print(40 * '=*=')
            select_yearly_expenses()

        elif view_expense_answer['choice'] == "Xem chi tiêu theo danh mục":
            print(40 * '=*=')
            view_expenses_by_category()
        
        elif view_expense_answer['choice'] == "Tìm kiếm chi tiêu theo mô tả":  # Mới thêm
            print(40 * '=*=')
            search_expenses_by_description()  # Gọi hàm tìm kiếm chi tiêu theo mô tả

        elif view_expense_answer['choice'] == "Quay lại":
            break

