from expenses import *

# Phần thống kê tìm kế doanh mục đã chi tiêu riêng lẻ
def list_categories_with_expenses():
    categories = set()
    for user_expenses in expenses.values():  # Lặp qua từng người dùng
        for date_str, items in user_expenses.items():  # Lặp qua từng ngày
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'category' in item:
                        categories.add(item['category'])
    return list(categories)

# Tìm kiếm danh mục đã chi tiêu 
def view_expenses_by_category():
    categories = list_categories_with_expenses()
    
    if not categories:
        print("Không có danh mục chi tiêu nào.")
        return

    # Hiển thị danh sách danh mục để người dùng chọn
    category_question = [
        inquirer.List(
            'category',
            message="Chọn danh mục để xem chi tiết",
            choices=categories + ["Quay lại"]
        )
    ]

    category_answer = inquirer.prompt(category_question)
    selected_category = category_answer['category']

    if selected_category == "Quay lại":
        return

    print(f"Chi tiêu cho danh mục: {selected_category}")

    total_amount = 0
    count = 0
    filtered_expenses = []

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'category' in item:
                        if item['category'].lower() == selected_category.lower():
                            count += 1
                            total_amount += item['amount']
                            item['date'] = date_str  # Thêm ngày vào từng mục chi tiêu
                            filtered_expenses.append(item)

    print(f"Đã chi tiêu {count} lần với tổng số tiền là {total_amount:,} VNĐ cho danh mục '{selected_category}'.")

    # Hiển thị chi tiết các chi tiêu cho danh mục đã chọn
    formatted_table = format_expenses_table(filtered_expenses)
    print(formatted_table)
