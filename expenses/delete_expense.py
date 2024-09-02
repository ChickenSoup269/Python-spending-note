from expenses import *
from common.categories import categories

def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("Không có chi tiêu nào để xóa.")
        return

    # Step 1: Chọn năm
    while True:
        years = get_years(expenses)
        year_question = [
            inquirer.List(
                'selected_year',
                message="Chọn năm bạn muốn xóa chi tiêu:",
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
                    message="Chọn tháng bạn muốn xóa chi tiêu:",
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
                        message="Chọn tuần bạn muốn xóa chi tiêu:",
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
                    print("Không có chi tiêu nào để xóa trong tuần này.")
                    break  # Return to the week selection

                # Step 5: Hiển thị danh sách chi tiêu để chọn xóa
                while True:
                    choices = [
                        f"[{i}] {item.get('description', 'Không mô tả')} - {item.get('category', 'Không danh mục')} - {item.get('amount', 'Không số tiền')} VNĐ - {item.get('quantity', 'Không số lượng')} ({date_str})"
                        for i, (user, date_str, item) in enumerate(expense_list)
                    ] + ["Quay lại"]

                    delete_question = [
                        inquirer.List(
                            'selected_expense',
                            message="Chọn chi tiêu bạn muốn xóa:",
                            choices=choices
                        )
                    ]

                    delete_answer = inquirer.prompt(delete_question)
                    if delete_answer['selected_expense'] == "Quay lại":
                        break  # Return to the week selection

                    # Extract the selected expense to delete
                    selected_index = int(delete_answer['selected_expense'].split(']')[0][1:])
                    user, selected_date, selected_expense = expense_list[selected_index]

                    # Xác nhận xóa
                    confirm_delete_question = [
                        inquirer.List(
                            'confirm_delete',
                            message=f"Bạn có chắc chắn muốn xóa chi tiêu này không? (Mô tả: {selected_expense.get('description', 'Không mô tả')})",
                            choices=["Có", "Không"]
                        )
                    ]

                    confirm_delete_answer = inquirer.prompt(confirm_delete_question)
                    if confirm_delete_answer['confirm_delete'] == "Có":
                        # Remove the selected expense
                        expenses[user][selected_date] = [item for item in expenses[user][selected_date] if item['id'] != selected_expense['id']]

                        # Remove the date entry if no expenses left for that date
                        if not expenses[user][selected_date]:
                            del expenses[user][selected_date]

                        # Remove the user entry if no dates left
                        if not expenses[user]:
                            del expenses[user]

                        # Save the updated expenses
                        save_expenses()
                        print("Chi tiêu đã được xóa thành công.")
                        break  # Return to the week selection