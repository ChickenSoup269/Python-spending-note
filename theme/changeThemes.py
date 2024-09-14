from imports import *

# Hàm tính số ngày còn lại đến Giáng Sinh (25/12) của năm hiện tại
def days_until_christmas():
    today = datetime.now()
    this_year_christmas = datetime(today.year, 12, 25)
    
    if today > this_year_christmas:
        # Nếu hôm nay đã qua Giáng Sinh của năm nay, tính đến Giáng Sinh năm sau
        next_christmas = datetime(today.year + 1, 12, 25)
    else:
        # Nếu chưa đến Giáng Sinh của năm nay, tính đến Giáng Sinh năm nay
        next_christmas = this_year_christmas
    
    days_left = (next_christmas - today).days
    return days_left, next_christmas.year


# Hàm tính số ngày còn lại đến Quốc Khánh (2/9) của năm hiện tại
def days_until_independence_day():
    today = datetime.now()
    this_year_independence_day = datetime(today.year, 9, 2)
    
    if today > this_year_independence_day:
        # Nếu hôm nay đã qua Quốc Khánh của năm nay, tính đến Quốc Khánh năm sau
        next_independence_day = datetime(today.year + 1, 9, 2)
    else:
        # Nếu chưa đến Quốc Khánh của năm nay, tính đến Quốc Khánh năm nay
        next_independence_day = this_year_independence_day
    
    days_left = (next_independence_day - today).days
    return days_left, next_independence_day.year

# Load cài đặt theme
theme_settings = load_theme_settings()
selected_color = eval(theme_settings.get("color", "Fore.LIGHTRED_EX"))  # Lấy màu đã lưu, mặc định đỏ
selected_font = theme_settings.get("art_style", "standard")  # Lấy font đã lưu, mặc định 'standard'
program_name = theme_settings.get("program_name", "Zero Spending")  # Mặc định tên chương trình là 'Zero Spending'
use_random_colors = theme_settings.get("use_random_colors", False)  # Mặc định không dùng màu ngẫu nhiên
show_time = theme_settings.get("show_time", True)  # Mặc định hiển thị thời gian
time_font_style = theme_settings.get("time_font_style", "banner3")  # Lấy font thời gian, mặc định 'banner3'
change_title_color = theme_settings.get("change_title_color", False)  # Mặc định không đổi màu tiêu đề
title_color_choice = theme_settings.get("title_color_choice", "Không đổi màu (trắng)")  # Mặc định không đổi màu tiêu đề

# Tạo chữ nghệ thuật từ tên chương trình
art = pyfiglet.figlet_format(program_name, font=selected_font)

# Nếu theme là "Giáng Sinh", tính số ngày còn lại đến 25/12 và hiển thị nó
days_left_display = ""
if theme_settings.get("color") == "Fore.LIGHTCYAN_EX":
    days_left, year = days_until_christmas()
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Giáng Sinh năm {year}!"


# Nếu theme là "Quốc Khánh", tính số ngày còn lại đến 2/9 và hiển thị nó
if theme_settings.get("color") == "Fore.LIGHTRED_EX":
    days_left, year = days_until_independence_day()
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Quốc Khánh năm {year}!"


# Hiển thị thời gian nếu được bật
dateTimes = pyfiglet.figlet_format(datetime.now().strftime('%d/%m/%Y'), font=time_font_style) if show_time else ""  # Áp dụng font cho thời gian

# Nếu sử dụng màu ngẫu nhiên, chọn ngẫu nhiên từ danh sách
if use_random_colors:
    colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
    colored_line = ''.join(random.choice(colors) + '=' for _ in range(68))
    end_line = ''.join(random.choice(colors) + '*' for _ in range(68))
else:
    # Nếu không sử dụng màu ngẫu nhiên, dùng màu đã chọn
    colored_line = ''.join(selected_color + '=' for _ in range(68))
    end_line = ''.join(selected_color + '*' for _ in range(68))

# In ra các dòng đã format với màu sắc và chữ nghệ thuật
print(colored_line)

# Kiểm tra xem người dùng có chọn đổi màu tiêu đề không và thực hiện theo lựa chọn
if change_title_color:
    if title_color_choice == "Không đổi màu (trắng)":
        print(Fore.LIGHTWHITE_EX + art)  # In tiêu đề với màu trắng
    elif title_color_choice == "Sử dụng màu đại diện":
        print(selected_color + art)  # In tiêu đề với màu đại diện đã chọn
    elif title_color_choice == "Sử dụng màu ngẫu nhiên":
        # In tiêu đề với màu ngẫu nhiên cho từng ký tự
        random_title_color = ''.join(random.choice(colors) + letter for letter in art)
        print(random_title_color)
else:
    # Nếu không đổi màu, in tiêu đề với màu đã chọn cho theme chung
    print(selected_color + art)

print(colored_line)



