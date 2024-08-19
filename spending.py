import inquirer #
import json #
import uuid #
import termcharts #
import pyfiglet #
import termcharts.bar_chart
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Back, Style, init
# 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
# ================================================================================
# Dictionary to store expenses
expenses = {}
console = Console()
# Khởi tạo Colorama
init(autoreset=True)

# In ra lời chào đầu 
art = pyfiglet.figlet_format('Zero Spending', font='standard')
print(68*'=')
print(art)
print(68*'=')

chitieu = 'Chitieu.json'

# Lưu file
def save_expenses():
   with open(chitieu, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, indent=4, ensure_ascii=False)

# Tải file
def load_expenses():
    global expenses
    try:
        with open(chitieu, 'r', encoding='utf-8') as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = {}

# Load expenses when the script starts
load_expenses()


menu_file = "menu.json"

# Load menu from JSON file
def load_menu():
    try:
        with open(menu_file, "r", encoding='utf-8') as f:
            menu = json.load(f)
    except FileNotFoundError:
        menu = {}
    return menu

# Save menu to JSON file
def save_menu(menu):
    with open(menu_file, "w" , encoding='utf-8') as f:
        json.dump(menu, f, indent=4)

# Add a new product to the menu

# Menu cho người dùng chọn chức năng
def main_menu():
    while True:
        # Menu chính để chọn nhóm chức năng
        main_choices = [
            "Kinh doanh",
            "Kiểm soát chi tiêu",
            "Thoát"
        ]

        main_questions = [
            inquirer.List(
                'main_choice',
                message="Chọn nhóm chức năng bạn muốn thực hiện",
                choices=main_choices,
            )
        ]

        main_answer = inquirer.prompt(main_questions)

        if main_answer['main_choice'] == "Kinh doanh":
            business_menu()
        elif main_answer['main_choice'] == "Kiểm soát chi tiêu":
            expense_menu()
        elif main_answer['main_choice'] == "Thoát":
            print(20*'*' + " | Cảm ơn bạn đã sử dụng chương trình! | " + 20*'*')
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
                message="Chọn chức năng bạn muốn thực hiện",
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


def expense_menu():
    while True:
        expense_choices = [
            "Thêm chi tiêu",
            "Xem chi tiêu tuần này",
            "Xem chi tiêu tháng này",
            "Xem chi tiêu năm này",
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
            print(40*'=*=')
            add_expense()
        elif expense_answer['choice'] == "Xem chi tiêu tuần này":
            print(40*'=*=')
            weekly_expenses()
        elif expense_answer['choice'] == "Xem chi tiêu tháng này":
            print(40*'=*=')
            monthly_expenses()
        elif expense_answer['choice'] == "Xem chi tiêu năm này":
            print(40*'=*=')
            yearly_expenses()
        elif expense_answer['choice'] == "Quay lại":
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
        "Tiết kiệm", "Khác"
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

# Function to format expenses table
def format_expenses_table(expenses_list):
    if not expenses_list:
        return "Không có chi tiêu nào trong khoảng thời gian này."

    # Tiêu đề từng hàng
    headers = ["Ngày", "Thứ trong tuần", "Danh mục", "Mô tả", "Đơn giá (VNĐ)", "Số lượng", "Số tiền (VNĐ)"]
    table = []

    # Chi tiết danh sách từng hàng
    total_expense = 0
    for expense in expenses_list:
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
        
        table.append([date, weekday_vn, category, description, f"{unit_price:,.0f}", quantity, f"{amount:,.0f}"])
    
    table.append(["Tổng chi tiêu", "****", "****", "****", "****", "****", f"{total_expense:,} VNĐ"])
    
    table_str = tabulate(table, headers=headers, tablefmt='rounded_outline')

    # Áp dụng màu sắc
    table_str_colored = table_str.replace(
        'Ngày', Fore.MAGENTA + 'Ngày' + Style.RESET_ALL
    ).replace(
        'Thứ trong tuần', Fore.BLUE  + 'Thứ trong tuần' + Style.RESET_ALL
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
    
def plot_expenses(categories, amounts, title):
    # Tạo dữ liệu cho biểu đồ
    data = dict(zip(categories, amounts))
    
    # Sắp xếp dữ liệu theo thứ tự danh mục
    sorted_categories = sorted(data.keys())
    sorted_amounts = [data[cat] for cat in sorted_categories]
    
    # Vẽ biểu đồ dạng bar chart
    try:
        # Tạo biểu đồ cột nằm nghiên
        bar_chart = termcharts.bar(
            dict(zip(sorted_categories, sorted_amounts)),
            title=title,
        )  
        
        # Biểu đồ pie chart
        pie_chart = termcharts.pie(
            dict(zip(sorted_categories, sorted_amounts)),
            title=title,
        )

        # In biểu đồ 
        print("\n" + bar_chart)
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

        while True:
            sub_questions = [
                inquirer.List(
                    'subcategory',
                    message="Chọn chi tiêu cụ thể:",
                    choices=categories[answers['main_category']] + ["Bỏ qua"],
                ),
                inquirer.Text('description', message="Mô tả chi tiêu (có thể bỏ qua)", default=""),
                inquirer.Text('amount', message="Số tiền (VNĐ, có thể bỏ qua)", default="0", validate=lambda _, x: x.isdigit()),
                inquirer.Text('quantity', message="Số lượng (có thể bỏ qua)", default="1", validate=lambda _, x: x.isdigit())
            ]
            
            sub_answers = inquirer.prompt(sub_questions)

            if sub_answers['subcategory'] == "Bỏ qua" or sub_answers['amount'] == "0":
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

            # Xác nhận từ người dùng
            confirm_question = [
                inquirer.Confirm('confirm', message="Bạn có muốn xác nhận chi tiêu này không?", default=True)
            ]
            confirm_answer = inquirer.prompt(confirm_question)

            if confirm_answer['confirm']:
                # Lấy ngày hiện tại và tên thứ trong tuần
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
            else:
                print("Đã hủy chi tiêu này.")

        # Hỏi người dùng có muốn quay lại menu chính
        more_expense_question = [
            inquirer.Confirm('more', message="Bạn có muốn quay lại menu chính không?", default=True)
        ]
        more_expense_answer = inquirer.prompt(more_expense_question)

        if not more_expense_answer['more']:
            break


# Tính chiêu tiêu trong tuần
def weekly_expenses():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    total_weekly = 0
    weekly_expenses_list = []
    categories = []
    amounts = []

    # Chuẩn bị dữ liệu để so sánh với tuần trước
    last_week_start = start_of_week - timedelta(days=7)
    last_week_end = end_of_week - timedelta(days=7)
    last_week_expenses = {}

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Tính toán chi tiêu trong tuần hiện tại
            if start_of_week <= date_obj <= today:
                for item in items:
                    total_weekly += item['amount']
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

            # Tính toán chi tiêu trong tuần trước
            if last_week_start <= date_obj <= last_week_end:
                for item in items:
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
    print(f"Tổng chi tiêu tuần: {total_weekly:,} VNĐ\n")


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
            bar_chart += f"[bold red]{week_label.ljust(max_label_length)} | {'█' * bar_length} {value:,.0f}[/bold red]\n"
        else:
            bar_chart += f"{week_label.ljust(max_label_length)} | {'[yellow]' + '█' * bar_length + '[/]'} {value:,.0f}\n"

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
            table.add_row(f"[bold yellow]{month}[/bold yellow]", f"[bold yellow]{total:,.0f}[/bold yellow]")
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
            bar_chart += f"[bold yellow]{month.ljust(max_label_length)}[/bold yellow] | [bold yellow]{'█' * bar_length}[/bold yellow] [bold yellow]{value:,.0f}[/bold yellow]\n"
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

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year == today.year and date_obj.month == today.month:
                if date_obj <= today:  # Include up to today's date
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

    print(f"Chi tiêu tháng {today.strftime('%m/%Y')}:")
    
    if monthly_expenses_list:
        print(format_expenses_table(monthly_expenses_list))
        plot_expenses(categories, amounts, 'Chi tiêu trong tháng')
        plot_monthly_comparison(12)
    else:
        print("Không có chi tiêu nào trong tháng này.")
    print(f"Tổng chi tiêu tháng: {total_monthly:,} VNĐ\n")


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

    table = Table(title=f'Chi tiêu hàng ngày trong năm {year}', title_style="bold blue")
    table.add_column("Ngày", style="bold green")
    table.add_column("Chi tiêu (VNĐ)", style="bold magenta")

    for date, amount in zip(dates, amounts):
        table.add_row(date, f"{amount:,.0f}")

    console.print(table)

    plot_data = {date: amount for date, amount in zip(dates, amounts)}
    
    max_value = max(amounts) if amounts else 0
    bar_chart = ""
    max_label_length = max(len(label) for label in dates)
    
    color = "yellow"  # Chọn màu cho cột

    if max_value > 0:
        for date in dates:
            value = plot_data[date]
            bar_length = int((value / max_value) * 40)
            bar_chart += f"{date.ljust(max_label_length)} | {'█' * bar_length} {value:,.0f}\n"
    else:
        bar_chart = "Không có dữ liệu chi tiêu để hiển thị."

    # Sử dụng màu sắc cho biểu đồ
    bar_chart_colored = Text.from_markup(f"[{color}] {bar_chart}[/]", style="bold")

    console.print(Panel(bar_chart_colored, title=f"Biểu đồ cột chi tiêu hàng ngày {year}", title_align="left"))

    note = f"Ghi chú: Biểu đồ thể hiện tổng chi tiêu hàng ngày trong năm {year}."
    console.print(f"\n[note] {note}")

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

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year == year:
                if date_obj <= today:  # Include up to today's date
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

    print(f"Chi tiêu trong năm {year}:")
    
    if yearly_expenses_list:
        print(format_expenses_table(yearly_expenses_list))
        plot_expenses(categories, amounts, f'Chi tiêu trong năm {year}')
        compare_years_expenses()
    else:
        print(f"Không có chi tiêu nào trong năm {year}.")
    print(f"Tổng chi tiêu năm: {total_yearly:,} VNĐ\n")



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

# Chạy menu chính
main_menu()

