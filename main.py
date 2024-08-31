import inquirer #
import json #
import requests #
import os #
import uuid #
import termcharts #
import pyfiglet #
import random #
import termcharts.bar_chart
from datetime import datetime, timedelta
from tabulate import tabulate
from collections import defaultdict
from colorama import Fore, Back, Style, init
# 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
# -*- coding: utf-8 -*-

# ================================================================================
# Dictionary to store expenses
expenses = {} # mục chi tiêu
savings = {} # mục tiết kiệm
console = Console()

# tính giờ để chào sáng, chiều ,tối
current_time = datetime.now()
dt_string = current_time.strftime("%H:%M:%S")
current_hour = current_time.hour

# Khởi tạo Colorama
init(autoreset=True)

chitieu = 'Chitieu.json' 
menu_file = "menu.json"
savings_file = 'saving.json'

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
    except FileNotFoundError:
        expenses = {}
        savings = {}

# Load expenses when the script starts
load_expenses()

# Đọc file menu kinh doanh
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


# In ra lời chào đầu 
art = pyfiglet.figlet_format('Zero Spending', font='standard')
dateTimes = pyfiglet.figlet_format(dt_string, font='banner3')
colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]

# Check giờ để in lời chào sáng, chiều, tối
def get_greeting():
    if 5 <= current_hour < 12:
        return 'Chào buổi sáng, chúc bạn buổi sáng tốt lành! 😆'
    elif 12 <= current_hour < 18:
        return 'Chào buổi chiều, chúc bạn buổi chiều vui vẻ! 😁'
    else:
        return 'Chào buổi tối, chúc bạn buổi tối thư giãn! 😮‍💨'
#  in =

colored_line = ''.join(random.choice(colors) + '=' for _ in range(68))
end_line = ''.join(random.choice(colors) + '*' for _ in range(68))

print(colored_line)

# In từng ký tự của chữ nghệ thuật với màu ngẫu nhiên
print(Style.BRIGHT + art)
print(dateTimes)
# In dòng cuối cùng với màu ngẫu nhiên
print(colored_line)
# In ra lời chào
print(get_greeting(), Fore.CYAN + dt_string + '\n')

# Dự báo thời tiết hoặc cái gì đó đại loại vậy 
# ==============================

# Menu cho người dùng chọn chức năng
def main_menu():
    while True:
        # Menu chính để chọn nhóm chức năng
        main_choices = [
            "💲 Kinh doanh",
            "💵 Kiểm soát chi tiêu",
            #🪙 "Giá vàng",
            "👛 Tiết kiệm",
            #☁️ "Thời tiết",
            "❌ Thoát"
        ]

        main_questions = [
            inquirer.List(
                'main_choice',
                message= 5*'*' + " Chọn chức năng bạn muốn thực hiện "  + 5*'*',
                choices=main_choices,
            )
        ]

        main_answer = inquirer.prompt(main_questions)

        if main_answer['main_choice'] == "💲 Kinh doanh":
            business_menu()
        elif main_answer['main_choice'] == "💵 Kiểm soát chi tiêu":
            expense_menu()
        elif main_answer['main_choice'] == "👛 Tiết kiệm":
            savings_menu()  
        elif main_answer['main_choice'] == "❌ Thoát":
            print(end_line)
            print(10*'=' + " | Cảm ơn bạn đã sử dụng chương trình! | " + 10*'=')
            print(end_line + '\n')
            break

def business_menu():
    while True:
        business_choices = [
            "Thêm sản phẩm vào menu",
            "Thêm số lượng sản phẩm",
            "Xem menu sản phẩm",
            "Ghi nhận bán hàng",
            "Thống kê doanh thu",
            "Quay lại"
        ]

        business_questions = [
            inquirer.List(
                'choice',
                message= 5*'*' + " Chọn chức năng bạn muốn thực hiện "  + 5*'*',
                choices=business_choices,
            )
        ]

        business_answer = inquirer.prompt(business_questions)

        if business_answer['choice'] == "Thêm sản phẩm vào menu":
            print(40*'=*=')
            add_product()
        elif business_answer['choice'] == "Thêm số lượng sản phẩm":
            print(40*'=*=')
            add_stock()
        elif business_answer['choice'] == "Xem menu sản phẩm":
            print(40*'=*=')
            view_menu()
        elif business_answer['choice'] == "Ghi nhận bán hàng":
            print(40*'=*=')
            record_sale()
        elif business_answer['choice'] == "Thống kê doanh thu":
            print(40*'=*=')
            view_sales_statistics()
        elif business_answer['choice'] == "Quay lại":
            break

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
            add_savings(amount)

        elif savings_answer['savings_choice'] == "Sử dụng tiền tiết kiệm":
            apply_savings()

        elif savings_answer['savings_choice'] == "Xem tổng tiền tiết kiệm":
            display_savings_book()

        elif savings_answer['savings_choice'] == "Cập nhật tiền tiết kiệm":
            update_savings()

        elif savings_answer['savings_choice'] == "Quay lại":
            break

def expense_menu():
    while True:
        expense_choices = [
            "Thêm chi tiêu",
            "Xem chi tiêu",
            "Xem chi tiêu theo năm",
            "Xem chi tiêu theo danh mục",
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
        elif expense_answer['choice'] == "Xem chi tiêu theo năm":
            print(40 * '=*=')
            select_yearly_expenses()
        elif expense_answer['choice'] == "Xem chi tiêu theo danh mục":
            print(40 * '=*=')
            view_expenses_by_category()

        elif expense_answer['choice'] == "Quay lại":
            break

def view_expenses_menu():
    while True:
        view_expense_choices = [
            "Xem chi tiêu tuần",
            "Xem chi tiêu tháng",
            "Xem chi tiêu năm",
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

        elif view_expense_answer['choice'] == "Quay lại":
            break

# Menu categories
categories = {
    "Chi tiêu thiết yếu": [
        "Đi chợ siêu thị", "Nhà hàng", "Chi trả hóa đơn", "Tiền nhà", "Đi lại", "Giúp việc", "Khác"
    ],
    "Mua sắm giải trí": [
        "Vui chơi giải trí", "Mua sắm", 'Đồ gia dụng', "Làm đẹp thể thao", "Khác"
    ],
    "Giáo dục và y tế": [
        "Giáo dục", "Y tế", "Bảo hiểm", "Khác"
    ],
    "Tiết kiệm": [
        "Tiết kiệm"
    ],
    "Đầu tư": [
        "Sự kiện", "Chứng khoán", "Bất động sản", "Quỹ", "Khác"
    ],
    "Chi khác": [
        "Biếu tặng", "Dịch vụ công", "Khác"
    ],
    "Tiền vay": [
       "Tiền vay"  ,"Khác"
    ]
}

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

# Function to add savings
def add_savings(amount):
    today = datetime.now()
    date = today.strftime('%Y-%m-%d')
    weekday_name = today.strftime('%A')  # Lấy tên thứ (ví dụ: "Monday")

    # Kiểm tra nếu ngày hôm nay chưa có trong savings
    if date not in savings:
        savings[date] = {"amount": 0, "weekday": weekday_translation.get(weekday_name)}
    
    # Cộng số tiền tiết kiệm vào ngày hiện tại
    savings[date]["amount"] += amount

    # Lưu dữ liệu
    save_expenses()

    # Thông báo cho người dùng  
    print(display_savings_book())
    print(Fore.GREEN + f"Đã thêm tiết kiệm: {amount:,} VNĐ vào ngày {date} ({weekday_translation.get(weekday_name)}) \n" + Style.RESET_ALL)

# Cập nhật tiền tiết kiệm
def update_savings():
    if not savings:
        print(Fore.RED + "Không có tiền tiết kiệm nào để cập nhật." + Style.RESET_ALL)
        return

    # In danh sách các ngày có trong savings để người dùng chọn
    dates = list(savings.keys())
    date_question = [
        inquirer.List(
            'selected_date',
            message="Chọn ngày bạn muốn cập nhật số tiền tiết kiệm:",
            choices=dates,
        )
    ]

    date_answer = inquirer.prompt(date_question)
    selected_date = date_answer['selected_date']

    # Lấy số tiền mới từ người dùng
    new_amount = int(input(f"Nhập số tiền tiết kiệm mới cho ngày {selected_date} (VNĐ): "))

    # Cập nhật số tiền tiết kiệm
    savings[selected_date]["amount"] = new_amount

    # Lưu lại thay đổi
    save_expenses()

    print(Fore.GREEN + f"Số tiền tiết kiệm cho ngày {selected_date} đã được cập nhật thành {new_amount:,} VNĐ." + Style.RESET_ALL)

# Function to apply savings to current expenses
def apply_savings():
    if not savings:
        print(Fore.RED + "Không có tiền tiết kiệm nào để sử dụng." + Style.RESET_ALL)
        return

    date = input("Nhập ngày của khoản tiết kiệm cần sử dụng (YYYY-MM-DD): ")
    if date not in savings:
        print(Fore.RED + "Ngày tiết kiệm không hợp lệ." + Style.RESET_ALL)
        return
    
    amount = int(input("Nhập số tiền cần sử dụng (VNĐ): "))
    if amount > savings[date]["amount"]:
        print(Fore.RED + "Số tiền yêu cầu vượt quá số tiền tiết kiệm hiện có." + Style.RESET_ALL)
        return
    
    # Deduct savings and add to expenses
    # Trước khi thực hiện điều này, gọi hàm add_expense_from_savings
 
    add_expense_from_savings(amount, "Chi tiêu từ tiết kiệm")

# Function to add an expense directly from savings
def get_savings_balance():
    today = datetime.now().strftime('%Y-%m-%d')
    return savings.get(today, {"amount": 0})["amount"]

def update_savings_balance(amount_spent):
    today = datetime.now().strftime('%Y-%m-%d')
    if today in savings:
        savings[today]["amount"] -= amount_spent
        if savings[today]["amount"] <= 0:
            del savings[today]  # Xóa ngày nếu số dư không còn
    else:
        print(Fore.RED + "Không có số dư tiết kiệm cho ngày hôm nay!" + Style.RESET_ALL)

def add_expense_from_savings(amount, category):
    savings_balance = get_savings_balance()
    
    if amount > savings_balance:
        print(Fore.RED + "Số tiền chi tiêu vượt quá số dư tiết kiệm hiện có!" + Style.RESET_ALL)
        return
    
    # Thực hiện chi tiêu từ tiết kiệm
    # Giảm số dư tiết kiệm trước khi thêm chi tiêu
    update_savings_balance(amount)

    # Tiến hành thêm chi tiêu
    while True:
        add_expense(amount, category)
        
        # Hỏi người dùng có muốn xác nhận chi tiêu không
        confirm_question = [
            inquirer.Confirm('confirm', message="Bạn có muốn xác nhận chi tiêu này không?", default=True)
        ]
        confirm_answer = inquirer.prompt(confirm_question)

        if confirm_answer['confirm']:
            print(Fore.GREEN + f"Chi tiêu được xác nhận. Đã trừ {amount:,} VNĐ từ số dư tiết kiệm." + Style.RESET_ALL)
            break
        else:
            # Nếu không xác nhận, khôi phục số dư tiết kiệm
            print(Fore.YELLOW + "Chi tiêu đã bị hủy. Không trừ số tiền từ số dư tiết kiệm." + Style.RESET_ALL)
            # Hoàn lại số tiền vào số dư tiết kiệm
            add_savings(amount)
            break

def display_savings_book():
    if not savings:
        print(Fore.RED + "Không có dữ liệu tiết kiệm để hiển thị." + Style.RESET_ALL)
        return
    
    table_data = []
    
    # Thêm tiêu đề bảng
    headers = [Fore.CYAN + "Ngày" + Style.RESET_ALL, 
               Fore.CYAN + "Số Tiền (VNĐ)" + Style.RESET_ALL, 
               Fore.CYAN + "Ngày Trong Tuần" + Style.RESET_ALL]

    total_amount = 0
    
    for date, details in savings.items():
        table_data.append([
            date,
            f"{details['amount']:,}",
            details['weekday']
        ])
        total_amount += details['amount']

    # In bảng ra với màu sắc
    print(Fore.GREEN + tabulate(table_data, headers=headers, tablefmt="rounded_outline") + Style.RESET_ALL)
    
    # In tổng số tiền
    print(Fore.YELLOW + f"Tổng tiền tiết kiệm: {total_amount:,} VNĐ" + Style.RESET_ALL)

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


# Tính chiêu tiêu trong tuần
def weekly_expenses():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    total_weekly = 0
    daily_spendings = [0] * 7  # Create a list with 7 zeros to hold daily spending
    weekly_expenses_list = []
    categories = []
    amounts = []

    # Prepare data to compare with the previous week
    last_week_start = start_of_week - timedelta(days=7)
    last_week_end = end_of_week - timedelta(days=7)
    last_week_expenses = {}
    total_last_week = 0

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Calculate expenses for the current week
            if start_of_week <= date_obj <= today:
                day_index = (date_obj - start_of_week).days  # Calculate the day index (0 for Monday, 6 for Sunday)
                for item in items:
                    total_weekly += item['amount']
                    daily_spendings[day_index] += item['amount']  # Add amount to the correct day
                    weekly_expenses_list.append({
                        'date': date_str,
                        'category': item['category'],
                        'description': item['description'],
                        'quantity': item['quantity'],
                        'amount': item['amount']
                    })
                    if item['category'] not in categories:
                        categories.append(item['category'])
                        amounts.append(item['amount'])
                    else:
                        index = categories.index(item['category'])
                        amounts[index] += item['amount']

            # Calculate expenses for the previous week
            if last_week_start <= date_obj <= last_week_end:
                for item in items:
                    total_last_week += item['amount']  # Add to the total for last week
                    if item['category'] not in last_week_expenses:
                        last_week_expenses[item['category']] = item['amount']
                    else:
                        last_week_expenses[item['category']] += item['amount']

    start_day_vn = weekday_translation.get(start_of_week.strftime('%A'), start_of_week.strftime('%A'))
    end_day_vn = weekday_translation.get(today.strftime('%A'), today.strftime('%A'))

    print(f"Chi tiêu từ {start_day_vn} (ngày {start_of_week.strftime('%d/%m/%Y')}) đến {end_day_vn} (ngày {today.strftime('%d/%m/%Y')}):")

    if weekly_expenses_list:
        print(format_expenses_table(weekly_expenses_list))
        plot_expenses(categories, amounts, 'Chi tiêu trong tuần')
        plot_weekly_comparison(4)
    else:
        print("Không có chi tiêu nào trong tuần này.")
    
    # Tính số chi tiêu trong bình hằng ngày trong tuấn
    days_in_week = (today - start_of_week).days + 1  # tổng ngày trong tuần (including today)
    average_daily_spending = total_weekly / days_in_week
    print(f"Tổng chi tiêu tuần này: {total_weekly:,} VNĐ")
    print(Fore.LIGHTMAGENTA_EX + f"Chi tiêu trung bình mỗi ngày trong tuần: {average_daily_spending:,.0f} VNĐ\n") 

    # So sánh chi tiêu tuần trước
    difference = total_weekly - total_last_week
    if difference > 0:
        print(Fore.RED + f"Bạn đã chi tiêu nhiều hơn tuần trước {difference:,} VNĐ.")
    elif difference < 0:
        print(Fore.GREEN + f"Bạn đã chi tiêu ít hơn tuần trước {abs(difference):,} VNĐ.")
    else:
        print(Fore.BLUE + "Chi tiêu tuần này không đổi so với tuần trước.")

    print(Fore.YELLOW + f"Tổng chi tiêu tuần trước: {total_last_week:,} VNĐ\n")

def calculate_weekly_totals(num_weeks=4):
    today = datetime.now().date()
    weekly_totals = []
    week_labels = []

    for i in range(num_weeks):
        start_of_week = today - timedelta(days=today.weekday() + i * 7)
        end_of_week = start_of_week + timedelta(days=6)

        # Xác định tuần thứ mấy trong tháng
        week_of_month = (start_of_week.day - 1) // 7 + 1

        # Nếu tuần này nằm trong tháng trước, sử dụng nhãn tháng trước
        if start_of_week.month != today.month:
            week_label = f"Tuần {week_of_month} tháng {start_of_week.strftime('%m')}"
        else:
            week_label = f"Tuần {week_of_month} tháng {start_of_week.strftime('%m')}"

        total_weekly = 0
        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_of_week <= date_obj <= end_of_week:
                    for item in items:
                        total_weekly += item['amount']

        weekly_totals.append(total_weekly)
        week_labels.append(week_label)

    return weekly_totals[::-1], week_labels[::-1]  # Đảo ngược để tuần gần nhất lên đầu
def plot_weekly_comparison(num_weeks=4):
    weekly_totals, week_labels = calculate_weekly_totals(num_weeks)
    weekly_expenses = {label: [] for label in week_labels}

    today = datetime.now().date()
    current_week_label = week_labels[-1]  # Lấy nhãn của tuần hiện tại (tuần đầu tiên trong danh sách sau khi đảo ngược)

    for i in range(num_weeks):
        start_of_week = today - timedelta(days=today.weekday() + i * 7)
        end_of_week = start_of_week + timedelta(days=6)

        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_of_week <= date_obj <= end_of_week:
                    for item in items:
                        weekly_expenses[week_labels[i]].append({
                            'date': date_str,
                            'category': item['category'],
                            'description': item['description'],
                            'quantity': item['quantity'],
                            'amount': item['amount']
                        })

    # Tạo bảng dữ liệu cho rich
    table = Table(title=f'Chi tiêu trong {num_weeks} tuần gần đây', title_style="bold blue")
    table.add_column("Tuần", style="bold green")
    table.add_column("Tổng chi tiêu (VNĐ)", style="bold magenta")

    for week_label, total in zip(week_labels, weekly_totals):
        # Đổi màu tuần hiện tại
        if week_label == current_week_label:
            week_label = f"[bold red]{week_label}[/bold red]"
            total_str = f"[bold red]{total:,.0f}[/bold red]"
        else:
            total_str = f"{total:,.0f}"
        table.add_row(week_label, total_str)

    # Hiển thị bảng với rich
    console.print(table)

    # Vẽ biểu đồ cột với rich
    max_label_length = max(len(label) for label in week_labels)
    max_value = max(weekly_totals) if weekly_totals else 1

    bar_chart = ""
    for week_label in week_labels:
        value = weekly_totals[week_labels.index(week_label)]
        bar_length = int((value / max_value) * 40)  # Quy định chiều dài cột
        
        # Đổi màu tuần hiện tại trong biểu đồ
        if week_label.strip("[/bold red]") == current_week_label.strip("[/bold red]"):
            bar_chart += f"[bold red]{week_label.ljust(max_label_length)} | {'█' * bar_length} {value:,.0f} VNĐ[/bold red]\n"
        else:
            bar_chart += f"{week_label.ljust(max_label_length)} | {'[yellow]' + '█' * bar_length + '[/]'} {value:,.0f} VNĐ\n"

    # Hiển thị biểu đồ cột
    console.print(Panel(bar_chart, title="Biểu đồ cột chi tiêu", title_align="left"))

    # Hiển thị chi tiết cho từng tuần
    for week_label in week_labels:
        console.print(f"\nChi tiết cho {week_label}:")
        week_expenses = weekly_expenses[week_label.strip("[/bold red]")]
        if week_expenses:
            print(format_expenses_table(week_expenses))
        else:
            print("Không có chi tiêu nào trong tuần này.")

    # Thêm ghi chú dưới biểu đồ tổng hợp
    note = "Ghi chú: Biểu đồ và bảng chi tiết cho chi tiêu mỗi tuần trong 4 tuần gần đây."
    console.print(f"\n[note] {note}")

def calculate_monthly_totals(num_months=12):
    today = datetime.now().date()
    monthly_totals = []
    month_labels = []

    for i in range(num_months):
        # Xác định tháng bắt đầu và kết thúc
        start_of_month = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        total_monthly = 0
        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_of_month <= date_obj <= end_of_month:
                    for item in items:
                        total_monthly += item['amount']
        
        monthly_totals.append(total_monthly)
        month_labels.append(start_of_month.strftime('%m/%Y'))

    return monthly_totals[::-1], month_labels[::-1]  # Đảo ngược để tháng gần nhất lên đầu
def plot_monthly_comparison(num_months=12):
    monthly_totals, month_labels = calculate_monthly_totals(num_months)
    
    # Tạo bảng dữ liệu cho rich
    table = Table(title=f'Chi tiêu trong {num_months} tháng gần đây', title_style="bold blue")

    table.add_column("Tháng", style="bold green")
    table.add_column("Tổng chi tiêu (VNĐ)", style="bold magenta")

    # Xác định tháng hiện tại
    current_month = datetime.now().strftime('%m/%Y')

    for month, total in zip(month_labels, monthly_totals):
        if month == current_month:
            table.add_row(f"[bold yellow]{month}[/bold yellow]", f"[bold yellow]{total:,.0f} VNĐ[/bold yellow]")
        else:
            table.add_row(month, f"{total:,.0f}")

    # Hiển thị bảng với rich
    console.print(table)

    # Vẽ biểu đồ cột với rich
    plot_data = {month: total for month, total in zip(month_labels, monthly_totals)}

    # Tạo biểu đồ cột với rich
    bar_chart = ""
    max_label_length = max(len(label) for label in month_labels)
    max_value = max(monthly_totals)
    
    for month in month_labels:
        value = plot_data[month]
        bar_length = int((value / max_value) * 40)  # Quy định chiều dài cột

        if month == current_month:
            bar_chart += f"[bold yellow]{month.ljust(max_label_length)}[/bold yellow] | [bold yellow]{'█' * bar_length}[/bold yellow] [bold yellow]{value:,.0f} VNĐ[/bold yellow]\n"
        else:
            bar_chart += f"{month.ljust(max_label_length)} | {'█' * bar_length} {value:,.0f}\n"
    
    # Hiển thị biểu đồ cột
    console.print(Panel(bar_chart, title="Biểu đồ cột chi tiêu", title_align="left"))

    # Thêm ghi chú dưới biểu đồ
    note = "Ghi chú: Biểu đồ thể hiện tổng chi tiêu mỗi tháng trong 12 tháng gần đây."
    console.print(f"\n[note] {note}")


# Tính chi tiêu trong tháng
def monthly_expenses():
    today = datetime.now().date()
    total_monthly = 0
    monthly_expenses_list = []
    categories = []
    amounts = []

    # Xác định số ngày trong tháng hiện tại tính đến hôm nay
    days_in_month = today.day

    # Tính ngày bắt đầu và ngày kết thúc của tháng trước
    first_day_this_month = today.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    total_last_month = 0
    last_month_expenses = {}

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Tính chi tiêu cho tháng hiện tại
            if date_obj.year == today.year and date_obj.month == today.month:
                if date_obj <= today:  
                    for item in items:
                        total_monthly += item['amount']
                        monthly_expenses_list.append({
                            'date': date_str,
                            'category': item['category'],
                            'description': item['description'],
                            'quantity': item['quantity'],
                            'amount': item['amount']
                        })
                        if item['category'] not in categories:
                            categories.append(item['category'])
                            amounts.append(item['amount'])
                        else:
                            index = categories.index(item['category'])
                            amounts[index] += item['amount']

            # Tính chi tiêu tháng trước
            if first_day_previous_month <= date_obj <= last_day_previous_month:
                for item in items:
                    total_last_month += item['amount']
                    if item['category'] not in last_month_expenses:
                        last_month_expenses[item['category']] = item['amount']
                    else:
                        last_month_expenses[item['category']] += item['amount']

    print(f"Chi tiêu tháng {today.strftime('%m/%Y')}:")

    if monthly_expenses_list:
        print(format_expenses_table(monthly_expenses_list))
        plot_expenses(categories, amounts, 'Chi tiêu trong tháng')
        plot_monthly_comparison(12)
    else:
        print("Không có chi tiêu nào trong tháng này.")
    
    # Tính chi tiêu trung bình một ngày trong 1 tháng
    average_daily_spending = total_monthly / days_in_month
    print(f"Tổng chi tiêu tháng này: {total_monthly:,} VNĐ")
    print(Fore.LIGHTMAGENTA_EX + f"Chi tiêu trung bình mỗi ngày trong tháng: {average_daily_spending:,.0f} VNĐ\n")

    # So sánh chi tiêu tháng trước và tháng hiện tại
    difference = total_monthly - total_last_month
    if difference > 0:
        print(Fore.RED + f"Bạn đã chi tiêu nhiều hơn tháng trước {difference:,} VNĐ.")
    elif difference < 0:
        print(Fore.GREEN + f"Bạn đã chi tiêu ít hơn tháng trước {abs(difference):,} VNĐ.")
    else:
        print(Fore.BLUE + "Chi tiêu tháng này không đổi so với tháng trước.")

    print(Fore.CYAN + f"Tổng chi tiêu tháng trước: {total_last_month:,} VNĐ\n")

# =================================================================
def yearly_expenses_by_day(year):
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()
    daily_expenses = {}
    total_yearly = 0

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date_obj <= end_date:
                if date_str not in daily_expenses:
                    daily_expenses[date_str] = 0
                for item in items:
                    daily_expenses[date_str] += item['amount']
                    total_yearly += item['amount']

    dates = []
    amounts = []

    for date_str in sorted(daily_expenses.keys()):
        dates.append(date_str)
        amounts.append(daily_expenses[date_str])

    if not dates:
        print(f"Không có chi tiêu nào trong năm {year}.")
        return

    # Apply color to the table title
    table = Table(title=f'[bold blue]Chi tiêu hàng ngày trong năm {year}[/bold blue]', title_style="bold blue")
    table.add_column("[bold green]Ngày[/bold green]", style="bold green")
    table.add_column("[bold cyan]Thứ[/bold cyan]", style="bold cyan")
    table.add_column("[bold magenta]Chi tiêu (VNĐ)[/bold magenta]", style="bold magenta")

    for date, amount in zip(dates, amounts):
        day_name_vn = weekday_translation.get(datetime.strptime(date, "%Y-%m-%d").strftime('%A'), "")
        table.add_row(date, day_name_vn, f"{amount:,.0f}")

    console.print(table)

    plot_data = {date: amount for date, amount in zip(dates, amounts)}
    
    max_value = max(amounts) if amounts else 0
    bar_chart = ""
    # Fix (ngày và thứ) có cùng độ dài
    max_label_length = max(len(f"{date} ({weekday_translation[datetime.strptime(date, '%Y-%m-%d').strftime('%A')]})") for date in dates)

    color = "yellow"  # Chọn màu cho cột

    if max_value > 0:
        for date in dates:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            weekday_str = weekday_translation[date_obj.strftime('%A')]  # Lấy tên thứ trong tuần
            label = f"{date} - {weekday_str}".ljust(max_label_length)  # Canh lề trái bằng cách thêm khoảng trắng

            value = plot_data[date]
            bar_length = int((value / max_value) * 50)
            bar_chart += f"{label} | [bold {color}]{'█' * bar_length}[/bold {color}] {value:,.0f} VNĐ\n"
    else:
        bar_chart = "Không có dữ liệu chi tiêu để hiển thị."

    # Sử dụng màu sắc cho biểu đồ
    bar_chart_colored = Text.from_markup(bar_chart)

    # Apply color to the panel title
    console.print(Panel(bar_chart_colored, title=f"[bold cyan]Biểu đồ cột chi tiêu hàng ngày {year}[/bold cyan]", title_align="left"))

    note = f"Ghi chú: Biểu đồ thể hiện tổng chi tiêu hàng ngày trong năm {year}."
    console.print(f"\n[italic yellow]{note}[/italic yellow]") 

def compare_years_expenses(year=None):
    if year is None:
        year = datetime.now().year

    previous_year = year - 1
    next_year = year + 1

    years_to_check = [previous_year, year, next_year]

    for y in years_to_check:
        print(f"\nChi tiêu trong năm {y}:")
        yearly_expenses_by_day(y)

    def get_yearly_totals(year):
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        total = 0
        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date_obj <= end_date:
                    for item in items:
                        total += item['amount']
        return total

    totals = {y: get_yearly_totals(y) for y in years_to_check}

    totals = {y: total for y, total in totals.items() if total > 0}

    if not totals:
        print("Không có chi tiêu nào trong các năm gần đây.")
        return

    table = Table(title=f"So sánh chi tiêu hàng năm", title_style="bold blue")
    table.add_column("Năm", style="bold green")
    table.add_column("Tổng chi tiêu (VNĐ)", style="bold magenta")

    for y, total in totals.items():
        table.add_row(str(y), f"{total:,.0f}")

    console.print(table)

    max_value = max(totals.values()) if totals.values() else 0
    bar_chart = ""
    max_label_length = max(len(str(y)) for y in totals.keys())
    
    color = "cyan"  # Chọn màu cho cột

    if max_value > 0:
        for y, total in totals.items():
            bar_length = int((total / max_value) * 40)
            bar_chart += f"{str(y).ljust(max_label_length)} | {'█' * bar_length} {total:,.0f}\n"
    else:
        bar_chart = "Không có dữ liệu chi tiêu để hiển thị."

    # Sử dụng màu sắc cho biểu đồ
    bar_chart_colored = Text.from_markup(f"[{color}] {bar_chart}[/]", style="bold")

    console.print(Panel(bar_chart_colored, title="Biểu đồ cột so sánh chi tiêu hàng năm", title_align="left"))

    note = "Ghi chú: Biểu đồ so sánh tổng chi tiêu hàng năm giữa ba năm gần nhất."
    console.print(f"\n[note] {note}")

def yearly_expenses(year=None):
    if year is None:
        year = datetime.now().year

    today = datetime.now().date()
    total_yearly = 0
    yearly_expenses_list = []
    categories = []
    amounts = []

    # Xác định số ngày trong năm tính đến ngày hôm nay
    days_in_year = (today - datetime(year, 1, 1).date()).days + 1

    last_year = year - 1
    total_last_year = 0
    last_year_expenses = {}

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year == year:
                if date_obj <= today:  
                    for item in items:
                        total_yearly += item['amount']
                        yearly_expenses_list.append({
                            'date': date_str,
                            'category': item['category'],
                            'description': item['description'],
                            'quantity': item['quantity'],
                            'amount': item['amount']
                        })
                        if item['category'] not in categories:
                            categories.append(item['category'])
                            amounts.append(item['amount'])
                        else:
                            index = categories.index(item['category'])
                            amounts[index] += item['amount']

            # Tính chi tiêu năm trước
            if date_obj.year == last_year:
                for item in items:
                    total_last_year += item['amount']
                    if item['category'] not in last_year_expenses:
                        last_year_expenses[item['category']] = item['amount']
                    else:
                        last_year_expenses[item['category']] += item['amount']
    print(f"Chi tiêu trong năm {year}:")

    if yearly_expenses_list:
        print(format_expenses_table(yearly_expenses_list))
        plot_expenses(categories, amounts, f'Chi tiêu trong năm {year}')
        compare_years_expenses()
    else:
        print(f"Không có chi tiêu nào trong năm {year}.")
    
    # Tính trung bình chi tiêu một ngày trong năm
    average_daily_spending = total_yearly / days_in_year
    print(f"Tổng chi tiêu năm: {total_yearly:,} VNĐ")
    print(Fore.LIGHTMAGENTA_EX + f"Chi tiêu trung bình mỗi ngày trong năm: {average_daily_spending:,.0f} VNĐ\n")

    # So sánh chi tiêu năm trước với năm hiện tại
    difference = total_yearly - total_last_year
    if difference > 0:
        print(Fore.RED + f"Bạn đã chi tiêu nhiều hơn năm trước {difference:,} VNĐ.")
    elif difference < 0:
        print(Fore.GREEN + f"Bạn đã chi tiêu ít hơn năm trước {abs(difference):,} VNĐ.")
    else:
        print(Fore.GREEN + "Chi tiêu năm này không đổi so với năm trước.")

    print(Fore.CYAN + f"Tổng chi tiêu năm trước: {total_last_year:,} VNĐ\n")


# Tính toán trong kinh doanh
def add_product():
    menu = load_menu()

    while True:
        product_name = input("Nhập tên sản phẩm: ")
        if not product_name.isalpha():
            print("Tên sản phẩm không hợp lệ. Vui lòng nhập lại.")
            continue

        product_price = input("Nhập giá sản phẩm (VNĐ): ")
        try:
            product_price = float(product_price)
            if product_price <= 0:
                print("Giá sản phẩm phải lớn hơn 0. Vui lòng nhập lại.")
                continue
        except ValueError:
            print("Giá sản phẩm không hợp lệ. Vui lòng nhập lại.")
            continue

        break

    menu[product_name] = {
        "price": product_price,
        "stock": 0  # Initial stock is set to 0
    }

    save_menu(menu)
    print(f"Đã thêm sản phẩm: {product_name} với giá {product_price:,} VNĐ vào menu.")
# Add stock to existing products
def add_stock():
    menu = load_menu()
    
    if not menu:
        print("Menu hiện đang trống. Vui lòng thêm sản phẩm trước.")
        return

    questions = [
        inquirer.List(
            'product',
            message="Chọn sản phẩm bạn muốn thêm số lượng",
            choices=list(menu.keys()),
        )
    ]
    answer = inquirer.prompt(questions)
    product_name = answer['product']

    quantity = int(input(f"Nhập số lượng thêm vào cho {product_name}: "))
    menu[product_name]['stock'] += quantity

    save_menu(menu)
    print(f"Đã thêm {quantity} vào số lượng của {product_name}. Số lượng hiện tại: {menu[product_name]['stock']}")
# View the menu
def view_menu():
    menu = load_menu()

    if not menu:
        print("Menu hiện đang trống.")
        return

    # Tạo danh sách hàng cho bảng
    table = []
    for product_name, details in menu.items():
        table.append([
            f"{Fore.CYAN}{product_name}{Style.RESET_ALL}",
            f"{Fore.GREEN}{details['price']:,}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{details['stock']}{Style.RESET_ALL}"
        ])

    # Tạo tiêu đề cho bảng
    headers = [
        f"{Fore.MAGENTA}Tên sản phẩm{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Giá (VNĐ){Style.RESET_ALL}",
        f"{Fore.MAGENTA}Số lượng tồn kho{Style.RESET_ALL}"
    ]

    # Hiển thị bảng với tabulate
    print(tabulate(table, headers=headers, tablefmt='rounded_outline'))
# Record a sale
def record_sale():
    menu = load_menu()

    if not menu:
        print("Menu hiện đang trống. Vui lòng thêm sản phẩm trước.")
        return

    questions = [
        inquirer.List(
            'product',
            message="Chọn sản phẩm bạn muốn bán",
            choices=list(menu.keys()),
        )
    ]
    answer = inquirer.prompt(questions)
    product_name = answer['product']

    available_stock = menu[product_name]['stock']
    if available_stock <= 0:
        print(f"Sản phẩm {product_name} hiện đã hết hàng.")
        return

    quantity_sold = int(input(f"Nhập số lượng bán ra (tồn kho hiện tại: {available_stock}): "))
    
    if quantity_sold > available_stock:
        print("Số lượng bán ra không đủ tồn kho. Vui lòng nhập lại.")
        return
    
    # Update the stock
    menu[product_name]['stock'] -= quantity_sold
    total_sale = quantity_sold * menu[product_name]['price']
    
    save_menu(menu)
    print(f"Đã bán {quantity_sold} {product_name} với tổng số tiền {total_sale:,.0f} VNĐ.")
    
    # Add sale information to the expense record
    date_str = datetime.now().strftime("%Y-%m-%d")
    if date_str not in expenses:
        expenses[date_str] = []

    expenses[date_str].append({
        'category': 'Doanh thu bán hàng',
        'description': f"Bán {quantity_sold} {product_name}",
        'quantity': quantity_sold,
        'amount': total_sale
    })
    print(f"Đã ghi nhận doanh thu vào chi tiêu ngày {date_str}.")
def calculate_sales_last_4_weeks():
    today = datetime.now().date()
    sales_last_4_weeks = []
    sales_details = {}

    for i in range(4):
        start_of_week = today - timedelta(days=today.weekday() + i * 7)
        end_of_week = start_of_week + timedelta(days=6)
        week_label = f"Tuần {start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m')}"

        total_sales = 0
        product_sales = {}

        for date_str, items in expenses.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(f"Warning: Bỏ qua dữ liệu không hợp lệ {date_str}")
                continue

            if start_of_week <= date_obj <= end_of_week:
                for item in items:
                    if item['category'] == 'Doanh thu bán hàng':
                        total_sales += item['amount']
                        product_name = item['description'].split(" ")[1]
                        product_sales[product_name] = product_sales.get(product_name, 0) + item['quantity']

        sales_last_4_weeks.append((week_label, total_sales))
        sales_details[week_label] = product_sales

    # Reverse the list and maintain dictionary order
    sales_last_4_weeks = sales_last_4_weeks[::-1]
    sales_details = dict(reversed(list(sales_details.items())))

    return sales_last_4_weeks, sales_details
def find_best_selling_product(sales_details):
    product_sales_count = {}

    for week_sales in sales_details.values():
        for product_name, quantity_sold in week_sales.items():
            product_sales_count[product_name] = product_sales_count.get(product_name, 0) + quantity_sold

    # Check if product_sales_count is empty
    if not product_sales_count:
        return "Chưa có dữ liệu bán hàng", 0

    best_selling_product = max(product_sales_count, key=product_sales_count.get)
    return best_selling_product, product_sales_count[best_selling_product]
def view_sales_statistics():
    sales_last_4_weeks, sales_details = calculate_sales_last_4_weeks()

    table = Table(title="Doanh thu trong 4 tuần gần đây", title_style="bold blue")
    table.add_column("Tuần", style="bold green")
    table.add_column("Tổng doanh thu (VNĐ)", style="bold magenta")

    for week_label, total_sales in sales_last_4_weeks:
        table.add_row(week_label, f"{total_sales:,.0f}")

    console.print(table)

    # Tìm sản phẩm bán chạy nhất
    best_selling_product, quantity_sold = find_best_selling_product(sales_details)
    console.print(f"Sản phẩm bán chạy nhất: [bold red]{best_selling_product}[/bold red] với [bold yellow]{quantity_sold}[/bold yellow] sản phẩm bán ra trong 4 tuần qua.")
    
    # Thêm chi tiết sản phẩm bán ra trong từng tuần
    for week_label, product_sales in sales_details.items():
        console.print(f"\nChi tiết sản phẩm bán ra trong {week_label}:")
        if product_sales:
            for product, quantity in product_sales.items():
                print(f"{product}: {quantity} sản phẩm")
        else:
            print("Không có sản phẩm nào được bán trong tuần này.")


# Cho lời khuyên chi tiêu nếu không hợp lý thì sẽ thông báo
def give_spending_advice(expenses):
    # Tổng hợp chi tiêu theo từng loại và từng tháng
    monthly_category_totals = defaultdict(lambda: defaultdict(float))
    
    for user, dates in expenses.items():
        for date, expense_list in dates.items():
            year_month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')  # Chỉ lấy năm và tháng
            for expense in expense_list:
                category = expense['category']
                amount = expense['amount']
                monthly_category_totals[year_month][category] += amount

    # Đưa ra lời khuyên dựa trên chi tiêu
    advice = []

    # Giả sử các mức chi tiêu hợp lý (VNĐ) cho mỗi tháng
    reasonable_limits = {
        "Đi chợ siêu thị": 2000000,
        "Nhà hàng": 1000000,
        "Chi trả hóa đơn": 1000000,
        "Tiền nhà": 2000000,
        "Đi lại": 1000000,
        "Vui chơi giải trí": 500000,
        "Mua sắm": 1000000,
        "Giáo dục": 2000000,
        "Y tế": 1000000, # không xác định được
        "Bảo hiểm": 2000000,
        "Tiết kiệm": 0,  # Không có giới hạn, nên tiết kiệm càng nhiều càng tốt
        "Chứng khoán": 0,  # Không có giới hạn cụ thể
        "Bất động sản": 0,  # Không có giới hạn cụ thể
        "Quỹ": 0,  # Không có giới hạn cụ thể
        "Sự kiện": 1000000,
        "Biếu tặng": 500000,
        "Dịch vụ công": 500000,
    }

    for year_month, category_totals in monthly_category_totals.items():
        for category, total in category_totals.items():
            if category in reasonable_limits:
                limit = reasonable_limits[category]
                if total > limit and limit != 0:
                    advice.append(
                        Fore.RED + f"Tháng {year_month} - Chi tiêu cho {category} ({total:,} VNĐ) vượt mức hợp lý ({limit:,} VNĐ). Bạn nên cân nhắc giảm chi tiêu ở hạng mục này."
                    )
                elif limit == 0 and total > 0:
                    advice.append(
                       Fore.YELLOW + f"Tháng {year_month} - Bạn đã chi tiêu {total:,} VNĐ cho {category}. Hãy đảm bảo rằng các khoản chi này là cần thiết."
                    )

    if not advice:
        advice.append(Fore.GREEN + "Chi tiêu của bạn trong các hạng mục hiện tại đang hợp lý. Tiếp tục duy trì!")

    return advice

# In ra lời khuyên
advice = give_spending_advice(expenses)
for line in advice:
    print(line + "\n")

# Chạy menu chính
main_menu()

