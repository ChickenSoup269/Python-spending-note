from expenses import *
from common.categories import categories

# Thêm chi tiêu 
def quick_entry(main_category):
    sub_questions = [
        inquirer.List(
            'subcategory',
            message="Chọn chi tiêu cụ thể:",
            choices=categories[main_category] + ["Bỏ qua"],
        ),
        inquirer.Text('description', message="Mô tả chi tiêu", default=""),
        inquirer.Text('amount', message="Số tiền (VNĐ)", default="", validate=lambda _, x: x.isdigit() or x == ""),
        inquirer.Text('quantity', message="Số lượng", default="1", validate=lambda _, x: x.isdigit())
    ]

    return inquirer.prompt(sub_questions)

def batch_entry(main_category, num_entries):
    entries = []
    for _ in range(num_entries):
        sub_answers = quick_entry(main_category)

        if sub_answers['subcategory'] == "Bỏ qua":
            continue  # Bỏ qua nếu chọn "Bỏ qua"

        total_amount = int(sub_answers['amount']) * int(sub_answers['quantity'])
        entries.append({
            "subcategory": sub_answers['subcategory'],
            "description": sub_answers['description'],
            "amount": total_amount,
            "quantity": int(sub_answers['quantity']),
            "total_amount": total_amount
        })

    return entries

def add_expense():
    while True:
        # Hỏi người dùng cách nhập chi tiêu
        entry_type_question = [
            inquirer.List(
                'entry_type',
                message="Bạn muốn nhập chi tiêu theo cách nào?",
                choices=["Nhập liên tiếp", "Nhập từng đơn vị", "Bỏ qua"],
            ),
        ]
        entry_type_answer = inquirer.prompt(entry_type_question)

        if entry_type_answer['entry_type'] == "Bỏ qua":
            print("Đã hủy thêm chi tiêu.")
            return

        if entry_type_answer['entry_type'] == "Nhập liên tiếp":
            # Hỏi người dùng số lượng sản phẩm muốn nhập
            num_entries_question = [
                inquirer.Text('num_entries', message="Nhập số lượng sản phẩm muốn thêm:", validate=lambda _, x: x.isdigit() and int(x) > 0)
            ]
            num_entries_answer = inquirer.prompt(num_entries_question)
            num_entries = int(num_entries_answer['num_entries'])

            # Hỏi người dùng chọn loại chi tiêu
            category_question = [
                inquirer.List(
                    'main_category',
                    message="Chọn loại chi tiêu:",
                    choices=list(categories.keys()) + ["Bỏ qua"],
                ),
            ]
            category_answer = inquirer.prompt(category_question)
            main_category = category_answer['main_category']

            if main_category == "Bỏ qua":
                print("Đã hủy thêm chi tiêu.")
                return

            entries = batch_entry(main_category, num_entries)

            if not entries:
                print("Không có chi tiêu nào để lưu.")
                continue

            # Hiển thị thông tin chi tiêu đã nhập
            table_data = []
            for entry in entries:
                table_data.append([
                    entry['subcategory'],
                    entry['description'],
                    entry['quantity'],
                    f"{entry['total_amount']:,}"
                ])

            headers = [Fore.CYAN + "Loại chi tiêu" + Style.RESET_ALL,
                       Fore.CYAN + "Mô tả" + Style.RESET_ALL,
                       Fore.CYAN + "Số lượng" + Style.RESET_ALL,
                       Fore.CYAN + "Tổng tiền (VNĐ)" + Style.RESET_ALL]

            print(Fore.GREEN + tabulate(table_data, headers=headers, tablefmt="rounded_outline") + Style.RESET_ALL)

            # Xác nhận lưu các chi tiêu
            confirm_save_question = [
                inquirer.Confirm('confirm_save', message="Bạn có muốn lưu các chi tiêu này không?", default=True)
            ]
            confirm_save_answer = inquirer.prompt(confirm_save_question)

            if confirm_save_answer['confirm_save']:
                today = datetime.now()
                date = today.strftime('%Y-%m-%d')
                weekday_name = today.strftime('%A')
                weekday_name_vn = weekday_translation.get(weekday_name, weekday_name)
                user = "TranPhuocThien-2003"  # Giả định ID người dùng

                if user not in expenses:
                    expenses[user] = {}
                if date not in expenses[user]:
                    expenses[user][date] = []

                for entry in entries:
                    expense_id = str(uuid.uuid4())
                    expenses[user][date].append({
                        "id": expense_id,
                        "category": entry['subcategory'],
                        "description": entry['description'],
                        "amount": entry['total_amount'],
                        "quantity": int(entry['quantity']),
                        "weekday": weekday_name_vn
                    })

                save_expenses()
                print(Fore.YELLOW + "Đã lưu các chi tiêu." + Style.RESET_ALL)
            else:
                print("Đã hủy lưu các chi tiêu.")

        else:  # Nhập từng đơn vị
            while True:
                # Hỏi người dùng chọn loại chi tiêu
                category_question = [
                    inquirer.List(
                        'main_category',
                        message="Chọn loại chi tiêu:",
                        choices=list(categories.keys()) + ["Bỏ qua"],
                    ),
                ]
                category_answer = inquirer.prompt(category_question)
                main_category = category_answer['main_category']

                if main_category == "Bỏ qua":
                    print("Đã hủy thêm chi tiêu.")
                    return

                sub_answers = {
                    'subcategory': '',
                    'description': '',
                    'amount': '',
                    'quantity': '1'
                }

                while True:
                    sub_questions = [
                        inquirer.List(
                            'subcategory',
                            message="Chọn chi tiêu cụ thể:",
                            choices=categories[main_category] + ["Bỏ qua"],
                            default=sub_answers['subcategory']
                        ),
                        inquirer.Text('description', message="Mô tả chi tiêu", default=sub_answers['description']),
                        inquirer.Text('amount', message="Số tiền (VNĐ)", default=sub_answers['amount'], validate=lambda _, x: x.isdigit() or x == ""),
                        inquirer.Text('quantity', message="Số lượng", default=sub_answers['quantity'], validate=lambda _, x: x.isdigit())
                    ]

                    sub_answers = inquirer.prompt(sub_questions)

                    if sub_answers['subcategory'] == "Bỏ qua":
                        print("Đã hủy thêm chi tiêu.")
                        return

                    total_amount = int(sub_answers['amount']) * int(sub_answers['quantity'])

                    table_data = [
                        [Fore.CYAN + "Loại chi tiêu" + Style.RESET_ALL, sub_answers['subcategory']],
                        [Fore.CYAN + "Mô tả" + Style.RESET_ALL, sub_answers['description']],
                        [Fore.CYAN + "Số lượng" + Style.RESET_ALL, sub_answers['quantity']],
                        [Fore.CYAN + "Tổng tiền (VNĐ)" + Style.RESET_ALL, f"{total_amount:,}"]
                    ]

                    print(Fore.GREEN + tabulate(table_data, headers=["Thông tin", "Chi tiết"], tablefmt="rounded_outline") + Style.RESET_ALL)

                    edit_question = [
                        inquirer.List(
                            'edit',
                            message="Bạn có muốn chỉnh sửa chi tiêu này không?",
                            choices=["Xác nhận", "Cập nhật", "Hủy"],
                        )
                    ]
                    edit_answer = inquirer.prompt(edit_question)

                    if edit_answer['edit'] == "Xác nhận":
                        break
                    elif edit_answer['edit'] == "Hủy":
                        print("Đã hủy chi tiêu này.")
                        return

                today = datetime.now()
                date = today.strftime('%Y-%m-%d')
                weekday_name = today.strftime('%A')
                weekday_name_vn = weekday_translation.get(weekday_name, weekday_name)
                user = "TranPhuocThien-2003"  # Giả định ID người dùng

                if user not in expenses:
                    expenses[user] = {}
                if date not in expenses[user]:
                    expenses[user][date] = []

                expense_id = str(uuid.uuid4())
                expenses[user][date].append({
                    "id": expense_id,
                    "category": sub_answers['subcategory'],
                    "description": sub_answers['description'],
                    "amount": total_amount,
                    "quantity": int(sub_answers['quantity']),
                    "weekday": weekday_name_vn
                })

                save_expenses()
                print(Fore.YELLOW + f"Đã thêm chi tiêu: {sub_answers['subcategory']} - {sub_answers['description']} - Số lượng: {sub_answers['quantity']} - Tổng tiền: {total_amount:,} VNĐ - Ngày: {weekday_name_vn}" + Style.RESET_ALL)

                continue_question = [
                    inquirer.Confirm('continue', message="Bạn có muốn thêm chi tiêu khác trong cùng danh mục không?", default=False)
                ]
                continue_answer = inquirer.prompt(continue_question)

                if not continue_answer['continue']:
                    break

        more_expense_question = [
            inquirer.Confirm('more', message="Bạn có muốn quay lại menu chính không?", default=True)
        ]
        more_expense_answer = inquirer.prompt(more_expense_question)

        if not more_expense_answer['more']:
            return