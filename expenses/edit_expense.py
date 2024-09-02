from expenses import *
from common.categories import categories


# Chỉnh sửa chi tiêu
def edit_expense():
    expenses = load_expenses()

    if not expenses:
        print("Không có chi tiêu nào để chỉnh sửa.")
        return

    # Step 1: Chọn năm
    while True:
        years = get_years(expenses)
        year_question = [
            inquirer.List(
                'selected_year',
                message="Chọn năm bạn muốn chỉnh sửa:",
                choices=[str(year) for year in years] + ["Quay lại"]
            )
        ]
        year_answer = inquirer.prompt(year_question)
        if year_answer['selected_year'] == "Quay lại":
            return

        year = int(year_answer['selected_year'])

        # Step 2: Chọn tháng
        while True:
            months = get_months(expenses, year)
            month_question = [
                inquirer.List(
                    'selected_month',
                    message="Chọn tháng bạn muốn chỉnh sửa:",
                    choices=[f"{month:02d}" for month in months] + ["Quay lại"]
                )
            ]
            month_answer = inquirer.prompt(month_question)
            if month_answer['selected_month'] == "Quay lại":
                break  # Return to the year selection

            month = int(month_answer['selected_month'])

            # Step 3: Chọn tuần
            while True:
                weeks = get_weeks(expenses, year, month)
                week_question = [
                    inquirer.List(
                        'selected_week',
                        message="Chọn tuần bạn muốn chỉnh sửa:",
                        choices=weeks + ["Quay lại"]
                    )
                ]
                week_answer = inquirer.prompt(week_question)
                if week_answer['selected_week'] == "Quay lại":
                    break  # Return to the month selection

                week_label = week_answer['selected_week']

                # Step 4: Lấy danh sách chi tiêu cho tuần được chọn
                expense_list = get_expenses_for_week(expenses, year, month, week_label)

                if not expense_list:
                    print("Không có chi tiêu nào để chỉnh sửa trong tuần này.")
                    break  # Return to the week selection

                # Step 5: Hiển thị danh sách chi tiêu để chọn
                while True:
                    choices = [
                        f"[{i}] {item.get('description', 'Không mô tả')} - {item.get('category', 'Không danh mục')} - {item.get('amount', 'Không số tiền')} VNĐ - {item.get('quantity', 'Không số lượng')} ({date_str})"
                        for i, (user, date_str, item) in enumerate(expense_list)
                    ] + ["Quay lại"]

                    edit_question = [
                        inquirer.List(
                            'selected_expense',
                            message="Chọn chi tiêu bạn muốn chỉnh sửa:",
                            choices=choices
                        )
                    ]

                    answer = inquirer.prompt(edit_question)
                    if answer['selected_expense'] == "Quay lại":
                        break  # Return to the week selection

                    # Extract the selected expense
                    selected_index = int(answer['selected_expense'].split(']')[0][1:])
                    user, selected_date, selected_expense = expense_list[selected_index]

                    # Allow the user to edit fields
                    new_description = input(f"Nhập mô tả mới (hiện tại: {selected_expense.get('description', 'Không mô tả')}): ") or selected_expense.get('description', 'Không mô tả')
                    
                    # Chọn danh mục từ danh sách có sẵn
                    categories_list = [cat for sublist in categories.values() for cat in sublist]
                    new_category = inquirer.prompt([
                        inquirer.List(
                            'category',
                            message=f"Nhập danh mục mới (hiện tại: {selected_expense.get('category', 'Không danh mục')}):",
                            choices=categories_list
                        )
                    ])['category'] or selected_expense.get('category', 'Không danh mục')

                    while True:
                        try:
                            new_amount = float(input(f"Nhập số tiền mới (hiện tại: {selected_expense.get('amount', 'Không số tiền')}): ") or selected_expense.get('amount', 0))
                            break
                        except ValueError:
                            print("Số tiền không hợp lệ. Vui lòng nhập lại.")

                    while True:
                        try:
                            new_quantity = int(input(f"Nhập số lượng mới (hiện tại: {selected_expense.get('quantity', 'Không số lượng')}): ") or selected_expense.get('quantity', 0))
                            break
                        except ValueError:
                            print("Số lượng không hợp lệ. Vui lòng nhập lại.")

                    # Update the selected expense
                    selected_expense['description'] = new_description
                    selected_expense['category'] = new_category
                    selected_expense['amount'] = new_amount
                    selected_expense['quantity'] = new_quantity

                    # Update expenses in the dictionary
                    expenses[user][selected_date] = [item if item['id'] != selected_expense['id'] else selected_expense for item in expenses[user][selected_date]]

                    # Save the updated expenses
                    save_expenses()
                    print("Chi tiêu đã được cập nhật thành công.")
                    break  # Return to the week selection