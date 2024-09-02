from expenses import *
from common.categories import categories

# Thêm chi tiêu 
def add_expense():
    while True:
        questions = [
            inquirer.List(
                'main_category',
                message="Chọn loại chi tiêu:",
                choices=list(categories.keys()) + ["Bỏ qua"],
            ),
        ]
        answers = inquirer.prompt(questions)

        if answers['main_category'] == "Bỏ qua":
            print("Đã hủy thêm chi tiêu.")
            return

        # Giá trị mặc định cho các trường nhập vào
        sub_answers = {
            'subcategory': '',
            'description': '',
            'amount': '',
            'quantity': '1'
        }

        while True:
            # Nếu các trường đã có giá trị, sử dụng chúng làm mặc định
            sub_questions = [
                inquirer.List(
                    'subcategory',
                    message="Chọn chi tiêu cụ thể:",
                    choices=categories[answers['main_category']] + ["Bỏ qua"],
                    default=sub_answers['subcategory']  # Giữ lại giá trị đã nhập
                ),
                inquirer.Text('description', message="Mô tả chi tiêu", default=sub_answers['description']),  # Giá trị mặc định
                inquirer.Text('amount', message="Số tiền (VNĐ)", default=sub_answers['amount'], validate=lambda _, x: x.isdigit() or x == ""),
                inquirer.Text('quantity', message="Số lượng", default=sub_answers['quantity'], validate=lambda _, x: x.isdigit())
            ]

            sub_answers = inquirer.prompt(sub_questions)

            if sub_answers['subcategory'] == "Bỏ qua":
                print("Đã hủy thêm chi tiêu.")
                return

            # Tính toán tổng tiền
            total_amount = int(sub_answers['amount']) * int(sub_answers['quantity'])

            # Tạo dữ liệu cho bảng
            table_data = [
                [Fore.CYAN + "Loại chi tiêu" + Style.RESET_ALL, sub_answers['subcategory']],
                [Fore.CYAN + "Mô tả" + Style.RESET_ALL, sub_answers['description']],
                [Fore.CYAN + "Số lượng" + Style.RESET_ALL, sub_answers['quantity']],
                [Fore.CYAN + "Tổng tiền (VNĐ)" + Style.RESET_ALL, f"{total_amount:,}"]
            ]

            # In bảng ra với màu sắc
            print(Fore.GREEN + tabulate(table_data, headers=["Thông tin", "Chi tiết"], tablefmt="rounded_outline") + Style.RESET_ALL)

            # Hỏi người dùng có muốn chỉnh sửa chi tiêu này không
            edit_question = [
                inquirer.List(
                    'edit',
                    message="Bạn có muốn chỉnh sửa chi tiêu này không?",
                    choices=["Xác nhận", "Cập nhật", "Hủy"],
                )
            ]
            edit_answer = inquirer.prompt(edit_question)

            if edit_answer['edit'] == "Xác nhận":
                break  # Thoát khỏi vòng lặp chỉnh sửa và tiếp tục xác nhận
            elif edit_answer['edit'] == "Hủy":
                print("Đã hủy chi tiêu này.")
                return

            # Nếu người dùng chọn chỉnh sửa, sẽ quay lại và giữ các giá trị vừa nhập để chỉnh sửa tiếp

        # Sau khi xác nhận, lưu chi tiêu
        today = datetime.now()
        date = today.strftime('%Y-%m-%d')
        weekday_name = today.strftime('%A')  # Lấy tên thứ trong tuần
        weekday_name_vn = weekday_translation.get(weekday_name, weekday_name)  # Dịch sang tiếng Việt

        user = "TranPhuocThien-2003"  # Giả định ID người dùng

        if user not in expenses:
            expenses[user] = {}
        if date not in expenses[user]:
            expenses[user][date] = []

        expense_id = str(uuid.uuid4())  # Tạo ID duy nhất cho mỗi chi tiêu

        expenses[user][date].append({
            "id": expense_id,
            "category": sub_answers['subcategory'],
            "description": sub_answers['description'],
            "amount": total_amount,
            "quantity": int(sub_answers['quantity']),
            "weekday": weekday_name_vn  # Thêm tên thứ vào thông tin chi tiêu
        })

        save_expenses()
        print(Fore.YELLOW + f"Đã thêm chi tiêu: {sub_answers['subcategory']} - {sub_answers['description']} - Số lượng: {sub_answers['quantity']} - Tổng tiền: {total_amount:,} VNĐ - Ngày: {weekday_name_vn}" + Style.RESET_ALL)

        # Hỏi người dùng có muốn thêm chi tiêu khác trong cùng danh mục
        continue_question = [
            inquirer.Confirm('continue', message="Bạn có muốn thêm chi tiêu khác trong cùng danh mục không?", default=False)
        ]
        continue_answer = inquirer.prompt(continue_question)

        if not continue_answer['continue']:
            break  # Thoát khỏi vòng lặp danh mục con và quay lại menu chính

    # Hỏi người dùng có muốn quay lại menu chính
    more_expense_question = [
        inquirer.Confirm('more', message="Bạn có muốn quay lại menu chính không?", default=True)
    ]
    more_expense_answer = inquirer.prompt(more_expense_question)

    if not more_expense_answer['more']:
        return