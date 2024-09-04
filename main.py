from imports import *
from utils import *
# -*- coding: utf-8 -*-
from business.business_menu import business_menu
from expenses.expense_menu import expense_menu
from savings.savings_menu import savings_menu

# ================================================================================
# Dictionary to store expenses

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
            "Kinh doanh",
            "Kiểm soát chi tiêu [BEST]",
            #🪙 "Giá vàng",
            "Tiết kiệm",
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

        if main_answer['main_choice'] == "Kinh doanh":
            business_menu()
        elif main_answer['main_choice'] == "Kiểm soát chi tiêu [BEST]":
            expense_menu()
        elif main_answer['main_choice'] == "Tiết kiệm":
            savings_menu()  
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
                amount = expense['amount']
                monthly_category_totals[year_month][category] += amount

    # Đưa ra lời khuyên dựa trên chi tiêu
    advice = []

    # Giả sử các mức chi tiêu hợp lý (VNĐ) cho mỗi tháng
    reasonable_limits = {
        "Đi chợ siêu thị": 2000000,
        "Nhà hàng": 1000000,
        "Chi trả hóa đơn": 1000000,
        "Tiền nhà": 2500000,
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

