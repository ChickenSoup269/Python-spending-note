from imports import *

# Hàm tính số ngày còn lại đến sự kiện
def days_until_tet(event_date):
    today = datetime.now()
    this_year_event_date = datetime(today.year, event_date.month, event_date.day)
    
    if today > this_year_event_date:
        # Nếu hôm nay đã qua ngày sự kiện của năm nay, tính đến năm sau
        next_event_date = datetime(today.year + 1, event_date.month, event_date.day)
    else:
        # Nếu chưa đến ngày sự kiện của năm nay, tính đến ngày sự kiện năm nay
        next_event_date = this_year_event_date
    
    days_left = (next_event_date - today).days
    return days_left, next_event_date.year, this_year_event_date.strftime('%d/%m/%Y')


# Hàm tính số ngày còn lại đến Giáng Sinh
def days_until_christmas():
    today = datetime.now()
    christmas_date = datetime(today.year, 12, 25)  # Ngày Giáng Sinh

    if today > christmas_date:
        christmas_date = datetime(today.year + 1, 12, 25)  # Nếu đã qua Giáng Sinh, tính năm sau

    days_left = (christmas_date - today).days
    return days_left, christmas_date.year, christmas_date.strftime('%d/%m/%Y')

# Hàm tính số ngày còn lại đến Quốc Khánh
def days_until_independence_day():
    today = datetime.now()
    independence_day_date = datetime(today.year, 9, 2)  # Ngày Quốc Khánh

    if today > independence_day_date:
        independence_day_date = datetime(today.year + 1, 9, 2)  # Nếu đã qua Quốc Khánh, tính năm sau
    days_left = (independence_day_date - today).days
    
    return days_left, independence_day_date.year, independence_day_date.strftime('%d/%m/%Y')

# Hàm tính số ngày còn lại đến Halloween
def days_until_halloween():
    today = datetime.now()
    halloween_date = datetime(today.year, 10, 31)  # Ngày Halloween

    # Nếu hôm nay đã qua ngày 31 tháng 10, tính ngày Halloween của năm sau
    if today > halloween_date:
        halloween_date = datetime(today.year + 1, 10, 31)
    days_left = (halloween_date - today).days

    return days_left, halloween_date.year, halloween_date.strftime('%d/%m/%Y')



# Load cài đặt theme
theme_settings = load_theme_settings()
selected_color = eval(theme_settings.get("color", "Fore.LIGHTRED_EX"))  
selected_font = theme_settings.get("art_style", "standard")  
program_name = theme_settings.get("program_name", "Zero Spending") 
use_random_colors = theme_settings.get("use_random_colors", False)  
show_time = theme_settings.get("show_time", True) 
time_font_style = theme_settings.get("time_font_style", "banner3")  
change_title_color = theme_settings.get("change_title_color", False) 
title_color_choice = theme_settings.get("title_color_choice", "Không đổi màu (trắng)")  
time_format = theme_settings.get("time_format", "both")

# Tạo chữ ACII từ tên chương trình
art = pyfiglet.figlet_format(program_name, font=selected_font)
colored_message = ""

# Hàm để lấy định dạng thời gian dựa trên cài đặt
def get_formatted_time():
    now = datetime.now()
    if time_format == "time":
        return pyfiglet.figlet_format(now.strftime('%H:%M:%S'), font=time_font_style)
    elif time_format == "date":
        return pyfiglet.figlet_format(now.strftime('%d/%m/%Y'), font=time_font_style)
    elif time_format == "both":
        return pyfiglet.figlet_format(now.strftime('%d/%m/%Y %H:%M:%S'), font=time_font_style)
    return ""

dateTimes = get_formatted_time() if show_time else ""
# ====================


#  Ngày Tết Âm Lịch (ví dụ, 10/2/2024, bạn cần thay đổi tùy theo năm)
tet_date = datetime(2024, 2, 10)  


# ====================

days_left_display = ""
# Kiểm tra theme và tính số ngày còn lại đến sự kiện
if theme_settings.get("program_name") == "Tet": 
    days_left, year,next_event = days_until_tet(tet_date)  # Tính số ngày còn lại đến Tết
    days_left_display = f"Ngày Tết: {tet_date.strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Tết Âm Lịch năm {year}! 🧧"
    new_year_message = pyfiglet.figlet_format("Nam Moi Binh An!", font="digital")  
    next_event_display = f"\nTết Nguyên Đán sẽ diễn ra vào ngày: {next_event}! 🎇"

    colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX]  # Đỏ và Vàng

    for i, char in enumerate(new_year_message):
        # Xen kẽ giữa hai màu
        colored_message += colors[i % 2] + char

    # Reset màu sau khi in
    colored_message += Style.RESET_ALL
    print(colored_message)

# Tính số ngày còn lại đến Giáng Sinh
elif theme_settings.get("program_name") == "Christmas":  
    days_left, year, next_event = days_until_christmas()  # Tính số ngày còn lại đến Giáng Sinh
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Giáng Sinh năm {year}! 🎄"
    christmas_message = pyfiglet.figlet_format("merry Chirsmarrk!", font="pyramid", width = 120 )  
    next_event_display = f"\nGiánh Sinh sẽ diễn ra vào ngày: {next_event}! ❄️"

    colors = [Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]  # xanh và trắng
    
    for i, char in enumerate(christmas_message):
        # Xen kẽ giữa hai màu
        colored_message += colors[i % 2] + char

    # Reset màu sau khi in
    colored_message += Style.RESET_ALL
    print(colored_message)


# Tính số ngày còn lại đến Quốc Khánh
elif theme_settings.get("program_name") == "Quoc Khanh":  
    days_left, year, next_event = days_until_independence_day()  # Tính số ngày còn lại đến Quốc Khánh
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Quốc Khánh năm {year}! 🎊"
    independence_day = pyfiglet.figlet_format("02/09/1945", font="larry3d", width = 120 )  
    next_event_display = f"\nQuốc Khánh sẽ diễn ra vào ngày: {next_event}! 🎉"

    colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX]  # Đỏ và Vàng

    for i, char in enumerate(independence_day):
        # Xen kẽ giữa hai màu
        colored_message += colors[i % 2] + char

    # Reset màu sau khi in
    colored_message += Style.RESET_ALL
    print(colored_message)

# Tính số ngày còn lại đến Halloween
elif theme_settings.get("program_name") == "Halloween":  
    days_left, year, next_event = days_until_halloween()
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Halloween năm {year}! 👻"
    halloween_message = pyfiglet.figlet_format("Happy Halloween", font="poison" , width = 120)  
    next_event_display = f"\nHalloween sẽ diễn ra vào ngày: {next_event}! 🎃"

    colored_message = ""
    colors = [Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX]  # tím và Vàng

    for i, char in enumerate(halloween_message):
        # Xen kẽ giữa hai màu
        colored_message += colors[i % 2] + char

    # Reset màu sau khi in
    colored_message += Style.RESET_ALL
    print(colored_message)


# Nếu sử dụng màu ngẫu nhiên, chọn ngẫu nhiên từ danh sách
if use_random_colors:
    colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
    colored_line = ''.join(random.choice(colors) + '=' for _ in range(68))
    end_line = ''.join(random.choice(colors) + '*' for _ in range(68))

# theme theo mùa 
elif len(colored_message) > 1:
    colored_line = ''.join(random.choice(colors)  + '=' for _ in range(68))
    end_line = ''.join(random.choice(colors) + '*' for _ in range(68))

# theme custom
else:
    colored_line = ''.join(selected_color  + '=' for _ in range(68))
    end_line = ''.join(selected_color  + '*' for _ in range(68))


print(colored_line)

# Kiểm tra user có chọn đổi màu tiêu đề không và thực hiện theo lựa chọn
if change_title_color:
    if title_color_choice == "Không đổi màu (trắng)":
        print(Fore.LIGHTWHITE_EX + art)
    elif title_color_choice == "Sử dụng màu đại diện":
        print(selected_color + art)  
    elif title_color_choice == "Sử dụng màu ngẫu nhiên":
        random_title_color = ''.join(random.choice(colors) + letter for letter in art)
        print(random_title_color)
else:
    print(selected_color + art)

if show_time:
    print(dateTimes)

if days_left_display:
    print(selected_color + days_left_display + next_event_display + Style.RESET_ALL)
    

print(colored_line)
