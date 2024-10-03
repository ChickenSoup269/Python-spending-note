from imports import *
from utils import *
# -*- coding: utf-8 -*-
# from business.business_menu import business_menu
from expenses.expense_menu import expense_menu
from savings.savings_menu import savings_menu
from settings.setting_menu import settings_menu
# =================================THEME===============================================
from theme.changeThemes import *
# ================================================================================
from terminaltexteffects.effects.effect_wipe import Wipe


# Check giờ để in lời chào sáng, chiều, tối
def get_greeting():
    if 5 <= current_hour < 12:
        return 'Chào buổi sáng, chúc bạn buổi sáng tốt lành! ⛅ '
    elif 12 <= current_hour < 18:
        return 'Chào buổi chiều, chúc bạn buổi chiều vui vẻ! 🌄 '
    else:
        return 'Chào buổi tối, chúc bạn buổi tối thư giãn! 🌝 '


# In ra lời chào
# print('Ngày: ' + current_date + '\n')
if theme_settings.get("program_name") in seasonal_themes: 
    print(selected_color + get_greeting(), Fore.CYAN + dt_string + '\n')
else: 
    effect = Wipe(get_greeting() + dt_string )
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame + "\n")
  


# Dự báo thời tiết hoặc cái gì đó đại loại vậy 
# ==============================

# Menu cho người dùng chọn chức năng
def main_menu():
    while True:
        # Menu chính để chọn nhóm chức năng
        main_choices = [
            # "Tiết kiệm",
            # "Kinh doanh",
            "Kiểm soát chi tiêu",
            "Xem danh mục chi tiêu",
            #🪙 "Giá vàng",
            #☁️ "Thời tiết",
            "Cài đặt",
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

        # if main_answer['main_choice'] == "Kinh doanh":
        #     business_menu()
        # if main_answer['main_choice'] == "Tiết kiệm":
        #     savings_menu()  
        if main_answer['main_choice'] == "Kiểm soát chi tiêu":
            expense_menu()
        elif main_answer['main_choice'] == "Xem danh mục chi tiêu":
            expenses = load_expenses()
            give_spending_advice(expenses) 
        elif main_answer['main_choice'] == "Cài đặt":  # Gọi hàm thay đổi theme
            settings_menu()
        elif main_answer['main_choice'] == "❌ Thoát":
            print(end_line)
            print(10*'=' + " | Cảm ơn bạn đã sử dụng chương trình! | " + 10*'=')
            print(end_line + '\n')
            break

# Cho lời khuyên chi tiêu nếu không hợp lý thì sẽ thông báo
def give_spending_advice(expenses):
    # Tổng hợp chi tiêu theo từng loại và từng tháng
    monthly_category_totals = defaultdict(lambda: defaultdict(float))
    
    for user, dates in expenses.items():
        for date, expense_list in dates.items():
            year_month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')  # Chỉ lấy năm và tháng
            for expense in expense_list:
                category = expense['category']
                amount = expense['amount'] * expense.get('quantity', 1)  # Nhân với số lượng nếu có
                monthly_category_totals[year_month][category] += amount

    advice = []
    table_data = []  

    # Mức chi tiêu đưa ra 
    reasonable_limits = {
        "Đi chợ siêu thị": 3000000,
        "Nhà hàng": 500000,
        "Chi trả hóa đơn": 1000000,
        "Tiền nhà": 2500000,
        "Đi lại": 1000000,
        "Vui chơi giải trí": 500000,
        "Mua sắm": 1000000,
        "Giáo dục": 2000000,
        "Y tế": 1000000,
        "Bảo hiểm": 2000000,
        "Tiết kiệm": 0,  
        "Chứng khoán": 0,
        "Bất động sản": 0,
        "Quỹ": 0,
        "Sự kiện": 1000000,
        "Biếu tặng": 500000,
        "Dịch vụ công": 500000,
        "Đồ gia dụng": 1000000,
        "Khác": 500000,
    }

    # Tạo dữ liệu cho bảng
    for year_month, category_totals in monthly_category_totals.items():
        for category, total in category_totals.items():
            limit = reasonable_limits.get(category, 0)
            
            if limit != 0 and total > limit:
                advice_text = Fore.RED + "Vượt mức"
                advice.append(
                    Fore.RED + f"Tháng {year_month} - Chi tiêu cho {category} ({total:,} VNĐ) vượt mức hợp lý ({limit:,} VNĐ)."
                )
            elif limit == 0 and total > 0:
                advice_text = Fore.YELLOW + "Không giới hạn"
            else:
                advice_text = Fore.GREEN + "Hợp lý"

            # Thêm dữ liệu vào bảng
            table_data.append([
                year_month, 
                category, 
                f"{total:,} VNĐ", 
                f"{limit:,} VNĐ" if limit != 0 else "Không giới hạn", 
                advice_text + Style.RESET_ALL  # Reset màu sau mỗi dòng
            ])

    # Bảng tổng hợp
    headers = [
        Fore.CYAN + "Tháng" + Style.RESET_ALL,
        Fore.CYAN + "Danh mục" + Style.RESET_ALL,
        Fore.CYAN + "Chi tiêu" + Style.RESET_ALL,
        Fore.CYAN + "Mức hợp lý" + Style.RESET_ALL,
        Fore.CYAN + "Trạng thái" + Style.RESET_ALL
    ]

    print(Fore.LIGHTBLUE_EX + "Bảng tổng chi tiêu theo danh mục và tháng:" + Style.RESET_ALL)
    print(tabulate(table_data, headers=headers, tablefmt="rounded_outline"))

    # In ra lời khuyên
    print("\n" + Fore.LIGHTBLUE_EX + "Lời khuyên chi tiêu:" + Style.RESET_ALL)
    if not advice:
        print(Fore.GREEN + "Chi tiêu của bạn trong các hạng mục hiện tại đang hợp lý. Tiếp tục duy trì!" + Style.RESET_ALL + "\n" )
    else:
        for line in advice:
            print(line + Style.RESET_ALL + "\n" )

# Chạy menu chính
main_menu()

