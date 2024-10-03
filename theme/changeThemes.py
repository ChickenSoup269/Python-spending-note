from imports import *
# from theme.LunarNewYear import *
# from theme.Halloween import *
# from theme.QuocKhanh import *
# from theme.Christmas import *
# from terminaltexteffects.effects.effect_decrypt import Decrypt

next_year = datetime.now().year + 1


 # Các theme theo mùa (predefined themes)
predefined_themes = {
    "Quốc Khánh": {"color": "Fore.LIGHTRED_EX", "font": "starwars", "width": "120", "program_name": "Quốc Khánh"},
    "Christmas": {"color": "Fore.LIGHTCYAN_EX", "font": "isometric1", "width": "250", "program_name": "Christmas"},
    "Halloween": {"color": "Fore.LIGHTMAGENTA_EX", "font": "doom", "width": "120", "program_name": "Halloween"},
    f"Tết {next_year}": {"color": "Fore.LIGHTYELLOW_EX", "font": "doom", "width": "120", "program_name": f"Lunar New Year {next_year}"},
    f"New Year {next_year}": {"color": "Fore.LIGHTCYAN_EX", "font": "larry3d", "width": "120", "program_name": f"New Year {next_year}"},
}

def get_seasonal_theme():
    today = datetime.now()
    
    # Define seasonal events and their corresponding themes
    seasonal_events = {
        "Quốc Khánh": (datetime(today.year, 9, 2), "Quốc Khánh"),
        # "Tết": (tet_dates.get(str(year)), f"Tết {next_year}"),
        "Halloween": (datetime(today.year, 10, 31), "Halloween"),
        "Christmas": (datetime(today.year, 12, 25), "Christmas"),
        "New Year": (datetime(today.year, 1, 1), f"New Year {next_year}"),
    }
    
    for event, (event_date, theme_name) in seasonal_events.items():
        if today.date() == event_date.date():
            return predefined_themes[theme_name]
    
    return None


def apply_seasonal_theme():
    # Đường dẫn đầy đủ để lưu backup
    backup_theme_file = 'json/theme_backup.json'
    current_theme = load_theme_settings()  # Lấy theme hiện tại

    # Tạo thư mục nếu không tồn tại
    os.makedirs(os.path.dirname(backup_theme_file), exist_ok=True)

    seasonal_theme = get_seasonal_theme()

    # Nếu có theme sự kiện
    if seasonal_theme:
        # Lưu theme hiện tại vào file backup
        if current_theme:
            with open(backup_theme_file, 'w') as backup_file:
                json.dump(current_theme, backup_file)  # Lưu theme hiện tại vào file backup

        settings = {
            "color": seasonal_theme['color'],
            "art_style": seasonal_theme['font'],
            "width": seasonal_theme['width'],
            "program_name": unidecode(seasonal_theme['program_name']),
            "use_random_colors": seasonal_theme.get('use_random_colors', False),
            "show_time": seasonal_theme.get('show_time', False),
            "time_font_style": seasonal_theme.get('time_font_style', "banner3"),
            "change_title_color": seasonal_theme.get('change_title_color', False),
            "title_color_choice": seasonal_theme.get('title_color_choice', "Không đổi màu (trắng)"),
            "time_format": seasonal_theme.get('time_format', "none"),
        }
        save_theme_settings(settings)  # Áp dụng theme sự kiện
        print(f"Theme '{seasonal_theme['program_name']}' đã được áp dụng tự động.")


apply_seasonal_theme()


# Hàm tính số ngày còn lại đến sự kiện
def days_until_tet(event_date):
    if not event_date:
        return None  # Nếu không có ngày, trả về None

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


# Hàm tính số ngày còn lại đến Giáng Sinh
def days_until_new_year():
    today = datetime.now()
    new_year_date = datetime(today.year + 1, 1, 1)  # Ngày Tết Dương lịch của năm sau

    days_left = (new_year_date - today).days
    return days_left, new_year_date.year, new_year_date.strftime('%d/%m/%Y')

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
time_color =  eval(theme_settings.get("time_color", "Fore.LIGHTWHITE_EX"))  

# Tạo chữ ACII từ tên chương trình
art = pyfiglet.figlet_format(program_name, font=selected_font)
colored_message = ""

# Hàm để lấy định dạng thời gian dựa trên cài đặt
def get_formatted_time_with_color():
    now = datetime.now()
    time_str = ""

    if time_format == "time":
        time_str = pyfiglet.figlet_format(now.strftime('%H:%M:%S'), font=time_font_style)
    elif time_format == "date":
        time_str = pyfiglet.figlet_format(now.strftime('%d/%m/%Y'), font=time_font_style)
    elif time_format == "both":
        time_str = pyfiglet.figlet_format(now.strftime('%d/%m/%Y %H:%M:%S'), font=time_font_style)
    
    return time_color + time_str + Style.RESET_ALL  # Áp dụng màu cho thời gian

dateTimes = get_formatted_time_with_color() if show_time else ""
# ====================================


# =================

# Hiệu ứng nhập chữ (typing effect) với điều kiện theo theme
def typing_effect(message):
    # Tùy thuộc vào chương trình, cài đặt thời gian trễ
    if theme_settings.get("program_name") == f"Lunar New Year {next_year}":
        delay = 0.015  
    elif theme_settings.get("program_name") == "Christmas":
        delay = 0.015 
    elif theme_settings.get("program_name") == "Quoc Khanh":
        delay = 0.005  
    elif theme_settings.get("program_name") == "Halloween":
        delay = 0.005  
    elif theme_settings.get("program_name") == "Zero Hacker":
        delay = 0.001  
    elif theme_settings.get("program_name") == f"New Year {next_year}":
        delay = 0.015  
    else:
        delay = 0    # Các theme khác - không có hiệu ứng nhập chữ

    colored_message = ""
    skip_effect = False   

    for i, char in enumerate(message):
        if keyboard.is_pressed('enter'): 
            skip_effect = True  
            break  
 
        colored_message += colors[i % 2] + char
   
        print(colors[i % 2] + char, end='', flush=True)
        # Tạo độ trễ giữa các ký tự để có hiệu ứng nhập
        time.sleep(delay)
    
    # Nếu người dùng nhấn Enter, in ra toàn bộ thông điệp ngay lập tức
    if skip_effect:
        print(message)  # In thông điệp đầy đủ

    # Reset màu sau khi in
    print(Style.RESET_ALL)


#  Cầu vòng typing
# def rainbow_typing_effect(message, delay=0.005):
#     colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
#     skip_effect = False

#     for i, char in enumerate(message):
#         if keyboard.is_pressed('enter'):  # Nhấn Enter để bỏ qua hiệu ứng
#             skip_effect = True
#             break

#         print(colors[i % len(colors)] + char, end='', flush=True)
#         time.sleep(delay)

#     if skip_effect:
#         # In ra toàn bộ thông điệp nếu nhấn Enter
#         print(Fore.RESET + message)

#     # Reset lại màu sau khi in
#     print(Style.RESET_ALL)


# =========================

days_left_display = ""


#  ==========================================

# Kiểm tra theme và tính số ngày còn lại đến sự kiện
if theme_settings.get("program_name") == f"Lunar New Year {next_year}":
    # Lấy ngày Tết từ dữ liệu JSON cho năm tiếp theo
    tet_date_str = tet_dates.get(str(next_year))
    if tet_date_str:
        event_date = datetime.strptime(tet_date_str, '%d/%m/%Y')
        days_left, year, next_event = days_until_tet(event_date)  # Tính số ngày còn lại đến Tết
        days_left_display = f"Ngày Tết: {event_date.strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Tết Âm Lịch năm {year}! 🧧"
        
        new_year_message = pyfiglet.figlet_format("Nam Moi Binh An!\nPhat Tai Phat Loc", font="digital")
        next_event_display = f"\nTết Nguyên Đán sẽ diễn ra vào ngày: {tet_dates.get(str(year))}! 🎇"

        colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX]  # Đỏ và Vàng
        typing_effect(new_year_message)  # Hiệu ứng gõ chữ

     
    else: 
        print(f"Không có thông tin ngày Tết cho năm {next_year}.")


# Tính số ngày còn lại đến Giáng Sinh
elif theme_settings.get("program_name") == "Christmas":  
    days_left, year, next_event = days_until_christmas()  # Tính số ngày còn lại đến Giáng Sinh
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Giáng Sinh năm {year}! 🎄"
    christmas_message = pyfiglet.figlet_format("merry Chirsmarrk!", font="pyramid", width = 120 )  
    next_event_display = f"\nGiánh Sinh sẽ diễn ra vào ngày: {next_event}! ❄️"

    colors = [Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]  # xanh và trắng
    effect = Rain(christmas_message)

    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


# Tính số ngày còn lại đến Quốc Khánh
elif theme_settings.get("program_name") == "Quoc Khanh":  
    days_left, year, next_event = days_until_independence_day()  # Tính số ngày còn lại đến Quốc Khánh
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Quốc Khánh năm {year}! 🎊"
    independence_day = pyfiglet.figlet_format("02/09/1945", font="larry3d", width = 120 )  
    next_event_display = f"\nQuốc Khánh sẽ diễn ra vào ngày: {next_event}! 🎉"

    colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX]  # Đỏ và Vàng
    typing_effect(independence_day)


# Tính số ngày còn lại đến Halloween
elif theme_settings.get("program_name") == "Halloween":  
    days_left, year, next_event = days_until_halloween()
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến Halloween năm {year}! 👻"
    halloween_message = pyfiglet.figlet_format("Happy Halloween", font="poison" , width = 120)  
    next_event_display = f"\nHalloween sẽ diễn ra vào ngày: {next_event}! 🎃"

    colors = [Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX]  # tím và Vàng
    effect = Scattered(halloween_message)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

# Tính ngày còn lại đến năm mới
elif theme_settings.get("program_name") == f"New Year {next_year}":  
    days_left, year, next_event = days_until_new_year()
    days_left_display = f"Hôm nay là: {datetime.now().strftime('%d/%m/%Y')}\nCòn {days_left} ngày nữa đến năm mới {year}! 🎇"
    new_year_message = pyfiglet.figlet_format("Happy New Year", font="big" , width = 120)  
    next_event_display = f"\nTết tây sẽ diễn ra vào ngày: {next_event}! 🎉"

    colors = [Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX]  # xanh và xanh trời
    effect = Scattered(new_year_message)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


#  =====================================================


elif theme_settings.get("program_name") == "Zero Hacker":
    for i in range(10, 101, 10):
        text = Text(f"Loading... {i}%")
        text.stylize(f"bold green")
        console.print(text, end="\r")
        time.sleep(0.10)

    hacking_message = "\nHacking complete!"
    effect = Print(hacking_message)
    # hacker_message = pyfiglet.figlet_format("Happy Hacking", font="binary" , width = 120)  
    # effect2 = Blackhole(hacker_message)
    colors = [Fore.LIGHTGREEN_EX, Fore.GREEN] # trắng và xanh lá

    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

    # with effect2.terminal_output() as terminal:
    #     for frame in effect2:
    #         terminal.print(frame)


# elif theme_settings.get("program_name") == "DOOM 1993":  
#     colors = [Fore.LIGHTGREEN_EX, Fore.GREEN] # trắng và xanh lá


#  =====================================================


# Nếu sử dụng màu ngẫu nhiên, chọn ngẫu nhiên từ danh sách
if use_random_colors:
    colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
    colored_line = ''.join(random.choice(colors) + '=' for _ in range(68))
    end_line = ''.join(random.choice(colors) + '*' for _ in range(68))

# theme custom
else:
    colored_line = ''.join(selected_color  + '=' for _ in range(68))
    end_line = ''.join(selected_color  + '*' for _ in range(68))

plain_colored_line = colored_line.replace(selected_color, "")


# Các theme theo mùa
seasonal_themes = [f"Lunar New Year {next_year}", "Christmas", "Quoc Khanh", "Halloween", "Zero Hacker", f"New Year {next_year}","DOOM 1993"]

# In dòng kẻ với hiệu ứng hoặc không, tùy thuộc vào theme
if theme_settings.get("program_name") in seasonal_themes: 
    if theme_settings.get("program_name") == f"Lunar New Year {next_year}":
        typing_effect(plain_colored_line)    

    if theme_settings.get("program_name") == 'Christmas':
         typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Quoc Khanh':
        typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Halloween':
        typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Zero Hacker':
        effect = Print(plain_colored_line)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame) 

    if theme_settings.get("program_name") == f"New Year {next_year}": 
        effect = Beams(plain_colored_line)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)

    if theme_settings.get("program_name") == "DOOM 1993":
        effect = Print(plain_colored_line)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)  
else:
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

# ======================================================

# In tiêu đề với hiệu ứng typing hoặc không, tùy thuộc vào theme
if theme_settings.get("program_name") in seasonal_themes: 
    if theme_settings.get("program_name") == f"Lunar New Year {next_year}":
        effect = Slide(art)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)
 
    if theme_settings.get("program_name") == 'Christmas':
        effect = Rain(art)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)  

    if theme_settings.get("program_name") == 'Quoc Khanh': 
         typing_effect(art)    

    if theme_settings.get("program_name") == 'Halloween':
        effect = Scattered(art)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)       

    if theme_settings.get("program_name") == 'Zero Hacker':
        effect = Unstable(art)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame) 

    if theme_settings.get("program_name") == f"New Year {next_year}": 
        effect = Blackhole(art)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame) 

    if theme_settings.get("program_name") == "DOOM 1993":
        effect = Burn(art)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)  

                          
else:
    print(selected_color + art)  # Custom hoặc mặc định sẽ in ra bình thường

# In thời gian nếu có
if show_time:
    dateTimes = get_formatted_time_with_color()
    print(dateTimes)


if days_left_display:
    print(selected_color + days_left_display + next_event_display + Style.RESET_ALL)


# In dòng kẻ với hiệu ứng hoặc không, tùy thuộc vào theme
if theme_settings.get("program_name") in seasonal_themes: 
    if theme_settings.get("program_name") == f"Lunar New Year {next_year}":
        typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Christmas':
        typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Quoc Khanh':
        typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Halloween':
        typing_effect(plain_colored_line)  

    if theme_settings.get("program_name") == 'Zero Hacker':
        effect = Print(plain_colored_line)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame) 

    if theme_settings.get("program_name") == f"New Year {next_year}": 
        effect = Beams(plain_colored_line)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame) 

    if theme_settings.get("program_name") == "DOOM 1993":
        effect = Print(plain_colored_line)
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)  
else:
    print(colored_line)  

