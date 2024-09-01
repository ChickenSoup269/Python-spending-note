from expenses import *
from .yearly_expenses import yearly_expenses

# Xem chi tiêu theo năm
def select_yearly_expenses():
    # Lấy danh sách các năm từ file JSON
    years = set()
    for user_expenses in expenses.values():
        for date_str in user_expenses.keys():
            year = datetime.strptime(date_str, "%Y-%m-%d").year
            years.add(year)

    if not years:
        print("Không có chi tiêu nào trong file.")
        return

    years = sorted(years, reverse=True)  # Sắp xếp các năm theo thứ tự giảm dần

    # Sử dụng Inquirer để người dùng chọn năm
    year_choices = [str(year) for year in years] + ["Quay lại"]
    year_question = [
        inquirer.List(
            'selected_year',
            message="Chọn năm bạn muốn xem chi tiêu:",
            choices=year_choices,
        )
    ]

    year_answer = inquirer.prompt(year_question)
    selected_year = year_answer['selected_year']

    if selected_year == "Quay lại":
        return

    print(40 * '=*=')
    yearly_expenses(int(selected_year))
    