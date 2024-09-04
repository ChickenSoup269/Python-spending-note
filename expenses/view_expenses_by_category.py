from expenses import *

# Phần thống kê tìm kế doanh mục đã chi tiêu riêng lẻ
def list_years_with_expenses():
    years = set()
    for user_expenses in expenses.values():
        for date_str in user_expenses.keys():
            year = date_str.split("-")[0]
            years.add(year)
    return list(years)

def list_months_in_year(selected_year):
    months = set()
    for user_expenses in expenses.values():
        for date_str in user_expenses.keys():
            if date_str.startswith(selected_year):
                month = date_str.split("-")[1]
                months.add(month)
    return list(months)

def list_categories_in_month(selected_year, selected_month):
    categories = set()
    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            if date_str.startswith(f"{selected_year}-{selected_month}"):
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and 'category' in item:
                            categories.add(item['category'])
    return list(categories)

def list_categories_in_year(selected_year):
    categories = set()
    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            if date_str.startswith(selected_year):
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and 'category' in item:
                            categories.add(item['category'])
    return list(categories)

def list_weekdays():
    return list(weekday_translation.values()) + ["Tất cả"]

def view_expenses_by_category():
    years = list_years_with_expenses()

    if not years:
        print("Không có dữ liệu chi tiêu nào.")
        return

    # Bước 1: Chọn năm
    year_question = [
        inquirer.List(
            'year',
            message="Chọn năm để xem các chi tiêu:",
            choices=years + ["Quay lại"]
        )
    ]
    year_answer = inquirer.prompt(year_question)
    selected_year = year_answer['year']

    if selected_year == "Quay lại":
        return

    # Hỏi người dùng có muốn lọc theo tháng không
    filter_by_month_question = [
        inquirer.Confirm(
            'filter_by_month',
            message="Bạn có muốn lọc theo tháng không?",
            default=True
        )
    ]
    filter_by_month_answer = inquirer.prompt(filter_by_month_question)
    
    if filter_by_month_answer['filter_by_month']:
        months = list_months_in_year(selected_year)
        if not months:
            print(f"Không có dữ liệu chi tiêu nào trong năm {selected_year}.")
            return

        month_question = [
            inquirer.List(
                'month',
                message=f"Chọn tháng để xem các chi tiêu trong năm {selected_year}:",
                choices=months + ["Quay lại"]
            )
        ]
        month_answer = inquirer.prompt(month_question)
        selected_month = month_answer['month']

        if selected_month == "Quay lại":
            return

        # Hỏi người dùng có muốn lọc theo ngày trong tuần không
        filter_by_weekday_question = [
            inquirer.Confirm(
                'filter_by_weekday',
                message="Bạn có muốn lọc theo ngày trong tuần không?",
                default=True
            )
        ]
        filter_by_weekday_answer = inquirer.prompt(filter_by_weekday_question)
        
        if filter_by_weekday_answer['filter_by_weekday']:
            weekdays = list_weekdays()
            weekday_question = [
                inquirer.List(
                    'weekday',
                    message="Chọn ngày trong tuần để lọc chi tiêu:",
                    choices=weekdays
                )
            ]
            weekday_answer = inquirer.prompt(weekday_question)
            selected_weekday = weekday_answer['weekday']
        else:
            selected_weekday = "Tất cả"
        
        # Hiển thị chi tiêu cho danh mục đã chọn với lọc theo tháng và ngày trong tuần
        display_expenses(selected_year, selected_month, selected_weekday)

    else:
        # Hiển thị chi tiêu cho toàn bộ năm đã chọn
        display_expenses(selected_year)

def display_expenses(selected_year, selected_month=None, selected_weekday="Tất cả"):
    categories = list_categories_in_month(selected_year, selected_month) if selected_month else list_categories_in_year(selected_year)

    if not categories:
        print(f"Không có danh mục chi tiêu nào trong tháng {selected_month} của năm {selected_year}.")
        return

    category_question = [
        inquirer.List(
            'category',
            message=f"Chọn danh mục để xem chi tiết trong tháng {selected_month} của năm {selected_year}:",
            choices=categories + ["Quay lại"]
        )
    ]
    category_answer = inquirer.prompt(category_question)
    selected_category = category_answer['category']

    if selected_category == "Quay lại":
        return

    print(f"\nChi tiêu cho danh mục: {selected_category} trong tháng {selected_month} của năm {selected_year} vào ngày {selected_weekday}\n")

    total_amount = 0
    count = 0
    filtered_expenses = []

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            if (not selected_month or date_str.startswith(f"{selected_year}-{selected_month}")):
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and 'category' in item:
                            item_date = datetime.strptime(date_str, "%Y-%m-%d")
                            item_weekday = weekday_translation.get(item_date.strftime("%A"))
                            if item['category'].lower() == selected_category.lower() and (selected_weekday == "Tất cả" or item_weekday == selected_weekday):
                                count += 1
                                total_amount += item['amount']
                                item['date'] = date_str
                                filtered_expenses.append(item)

    print(f"Đã chi tiêu {count} lần với tổng số tiền là {total_amount:,} VNĐ cho danh mục '{selected_category}' trong tháng {selected_month} của năm {selected_year} vào ngày {selected_weekday}.")

    # Hiển thị chi tiết các chi tiêu cho danh mục đã chọn
    formatted_table = format_expenses_table(filtered_expenses)
    print(formatted_table)