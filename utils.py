from imports import *

expenses = {} 
savings = {} 
console = Console()

chitieu = 'Chitieu.json' 
savings_file = 'saving.json'
menu_file = "menu.json"

# tính giờ để chào sáng, chiều ,tối
current_time = datetime.now()
dt_string = current_time.strftime("%H:%M:%S")
current_hour = current_time.hour

# Khởi tạo Colorama
init(autoreset=True)

# Chuyển đổi ngày Anh -> Việt
weekday_translation = {
    "Monday": "Thứ Hai",
    "Tuesday": "Thứ Ba",
    "Wednesday": "Thứ Tư",
    "Thursday": "Thứ Năm",
    "Friday": "Thứ Sáu",
    "Saturday": "Thứ Bảy",
    "Sunday": "Chủ Nhật"
}

#  ===================================
# Load menu from JSON file
def load_menu():
    try:
        with open('./json/'+ menu_file, "r", encoding='utf-8') as f:
            menu = json.load(f)
    except FileNotFoundError:
        menu = {}
    return menu

# Save menu to JSON file
def save_menu(menu):
    with open('./json/'+ menu_file, "w" , encoding='utf-8') as f:
        json.dump(menu, f, indent=4)

# Lưu file chi tiêu và tiết kiệm cùng một file json
def save_expenses():
    with open('./json/' + chitieu, 'w', encoding='utf-8') as f:
        json.dump({"expenses": expenses, "savings": savings}, f, indent=4, ensure_ascii=False)

# Tải file chi tiêu
def load_expenses():
    global expenses, savings
    try:
        with open('./json/' + chitieu, 'r', encoding='utf-8') as f:
            data = json.load(f)
            expenses = data.get("expenses", {})
            savings = data.get("savings", {})
            return expenses  
    except FileNotFoundError:
        expenses = {}
        savings = {}
        return expenses 

# In ra bảng chi tiêu tất cả các mục điều sử dụng bảng này
def format_expenses_table(expenses_list):
    if not expenses_list:
        return "Không có chi tiêu nào trong khoảng thời gian này."

    # Tiêu đề từng hàng
    headers = ["STT", "Ngày", "Thứ trong tuần", "Danh mục", "Mô tả", "Đơn giá (VNĐ)", "Số lượng", "Số tiền (VNĐ)"]
    table = []

    # Chi tiết danh sách từng hàng
    total_expense = 0
    for idx, expense in enumerate(expenses_list, start=1):
        date = expense['date']
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday_name = date_obj.strftime('%A')  # Lấy tên ngày trong tuần (ví dụ: Monday)
        weekday_vn = weekday_translation.get(weekday_name, weekday_name)  # Dịch sang tiếng Việt
        
        category = expense['category']
        description = expense['description']
        quantity = expense['quantity']
        amount = expense['amount']
        
        unit_price = amount / quantity  # Tính giá gốc
        total_expense += amount
        
        table.append([idx, date, weekday_vn, category, description, f"{unit_price:,.0f}", quantity, f"{amount:,.0f}"])
    
    table.append(["", "Tổng chi tiêu", "****", "****", "****", "****", "****", f"{total_expense:,} VNĐ"])
    
    table_str = tabulate(table, headers=headers, tablefmt='rounded_outline')

    # Áp dụng màu sắc
    table_str_colored = table_str.replace(
        'STT', Fore.LIGHTMAGENTA_EX + 'STT' + Style.RESET_ALL
    ).replace(
        'Ngày', Fore.MAGENTA + 'Ngày' + Style.RESET_ALL
    ).replace(
        'Thứ trong tuần', Fore.BLUE + 'Thứ trong tuần' + Style.RESET_ALL
    ).replace(
        'Danh mục', Fore.CYAN + 'Danh mục' + Style.RESET_ALL
    ).replace(
        'Mô tả', Fore.YELLOW + 'Mô tả' + Style.RESET_ALL
    ).replace(
        'Đơn giá (VNĐ)', Fore.GREEN + 'Đơn giá (VNĐ)' + Style.RESET_ALL
    ).replace(
        'Số lượng', Fore.CYAN + 'Số lượng' + Style.RESET_ALL
    ).replace(
        'Số tiền (VNĐ)', Fore.GREEN + 'Số tiền (VNĐ)' + Style.RESET_ALL
    ).replace(
        'Tổng chi tiêu', Fore.GREEN + 'Tổng chi tiêu' + Style.RESET_ALL
    )

    return table_str_colored

# ==========================================================

def plot_expenses(categories, amounts, title):
    # Tạo dữ liệu cho biểu đồ
    data = dict(zip(categories, amounts))
    
    # Sắp xếp dữ liệu theo thứ tự danh mục
    sorted_categories = sorted(data.keys())
    sorted_amounts = [data[cat] for cat in sorted_categories]
    
    # Vẽ biểu đồ dạng bar chart
    try:
        # Tạo biểu đồ cột nằm nghiên
        # bar_chart = termcharts.bar(
        #     dict(zip(sorted_categories, sorted_amounts)),
        #     title=title,
        # )  
        
        # Biểu đồ pie chart
        pie_chart = termcharts.pie(
            dict(zip(sorted_categories, sorted_amounts)),
            title=title,
        )

        # In biểu đồ 
        table = Table(title="Danh sách chi tiêu")
        table.add_column("Danh mục", style="cyan", no_wrap=True)
        table.add_column("Số tiền (VNĐ)", style="magenta")

        for category, amount in zip(sorted_categories, sorted_amounts):
            table.add_row(category, f"[bold green]{amount:,}[/bold green] VNĐ")
        
        # In bảng dữ liệu
        console.print(table)

         # ==============================================
        # Tạo biểu đồ dạng thanh
        console.print("\n" + title, style="bold underline")
        max_length = 50  # Độ dài tối đa của thanh

        # Sắp xếp các hạng mục và số tiền chi tiêu từ nhỏ đến lớn
        sorted_items = sorted(zip(sorted_categories, sorted_amounts), key=lambda x: x[1])

        # Tách lại danh sách sau khi sắp xếp
        sorted_categories, sorted_amounts = zip(*sorted_items)

        max_amount = max(sorted_amounts) if sorted_amounts else 1
        console.print("\nBiểu đồ Thanh:")
        for category, amount in zip(sorted_categories, sorted_amounts):
            bar_length = int(amount / max_amount * max_length)
            bar = "█" * bar_length
            bar = f"[bold orange1]{bar.ljust(max_length)}[/bold orange1]"  # Trang trí thanh biểu đồ
            console.print(f"{category.ljust(20)} | {bar} [bold green]{amount:,} [/bold green][bold orchid]VNĐ [/bold orchid]")

        # ==============================================
        print(pie_chart)
        console.print("\nBiểu đồ tròn:")
        total_amount = sum(sorted_amounts)
        pie_chart_text = ""
        for category, amount in zip(sorted_categories, sorted_amounts):
            percentage = (amount / total_amount) * 100
            pie_chart_text += f"[bold bright_magenta]{category}:[/bold bright_magenta] [bold green]{amount:,} VNĐ [/bold green] ({percentage:.2f}%)\n"
        console.print(pie_chart_text)

        # Tạo dữ liệu cho bảng
        table_data = [[category, f"{amount:,} VNĐ"] for category, amount in data.items()]

        # In bảng
        print(f"\nDanh sách chi tiêu:")
        print(tabulate(table_data, headers=["Danh mục", "Số tiền (VNĐ)"], tablefmt='rounded_grid'))

    except TypeError as e:
        print(f"Error generating charts: {e}")

# ============================================

# DÙNG TRONG CHỈNH SỬA VÀ XÓA CHI TIÊU
# lấy năm
def get_years(expenses):
    years = set()
    for user_expenses in expenses.values():
        for date_str in user_expenses.keys():
            year = datetime.strptime(date_str, "%Y-%m-%d").year
            years.add(year)
    return sorted(years, reverse=True)

#  Lấy tháng
def get_months(expenses, year):
    months = set()
    for user_expenses in expenses.values():
        for date_str in user_expenses.keys():
            if datetime.strptime(date_str, "%Y-%m-%d").year == year:
                month = datetime.strptime(date_str, "%Y-%m-%d").month
                months.add(month)
    return sorted(months)

# Lấy tuần
def get_weeks(expenses, year, month):
    weeks = set()
    for user_expenses in expenses.values():
        for date_str in user_expenses.keys():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year == year and date_obj.month == month:
                week_start = date_obj - timedelta(days=date_obj.weekday())
                week_label = week_start.strftime("%d/%m")
                weeks.add(week_label)
    return sorted(weeks)

# Lấy tuần sử dụng trong tuần
def get_expenses_for_week(expenses, year, month, week_label):
    week_start = datetime.strptime(week_label, "%d/%m")
    week_start = week_start.replace(year=year, month=month)
    week_end = week_start + timedelta(days=6)
    expense_list = []
    for user, user_expenses in expenses.items():
        for date_str, expense_items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if week_start <= date_obj <= week_end:
                if isinstance(expense_items, list):
                    for item in expense_items:
                        if isinstance(item, dict):
                            expense_list.append((user, date_str, item))
                        else:
                            print(f"Unexpected item format: {item}")
                else:
                    print(f"Unexpected expenses format for date {date_str}: {expense_items}")
    return expense_list
# ============================================

# Load expenses when the script starts
load_expenses()