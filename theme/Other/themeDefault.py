# In ra lời chào đầu 
from imports import *

# Hàm tính số ngày còn lại đến ngày Quốc Khánh
def days_until_september_2():
    today = datetime.now()
    this_year_september_2 = datetime(today.year, 9, 2)
    
    if today > this_year_september_2:
        # Nếu hôm nay đã qua 2/9 của năm nay, tính đến 2/9 năm sau
        next_september_2 = datetime(today.year + 1, 9, 2)
    else:
        # Nếu chưa đến 2/9 của năm nay, tính đến 2/9 năm nay
        next_september_2 = this_year_september_2
    
    days_left = (next_september_2 - today).days
    return days_left

# Hàm menu theme
def theme_menu():
    # Các màu từ colorama
    theme_choices = [
        "Đỏ", "Xanh lá", "Xanh dương", "Vàng", "Tím", "Cyan", "Trắng", "Xám", "Ngẫu nhiên", "Quay lại"
    ]

    theme_colors = {
        "Đỏ": "Fore.LIGHTRED_EX",
        "Xanh lá": "Fore.LIGHTGREEN_EX",
        "Xanh dương": "Fore.LIGHTBLUE_EX",
        "Vàng": "Fore.LIGHTYELLOW_EX",
        "Tím": "Fore.LIGHTMAGENTA_EX",
        "Cyan": "Fore.LIGHTCYAN_EX",
        "Trắng": "Fore.LIGHTWHITE_EX",
        "Xám": "Fore.LIGHTBLACK_EX"
    }

    # Các kiểu chữ pyfiglet
    font_choices = [
        "standard", "slant", "banner3", "block", "bubble", "digital", "quay lại"
    ]

    # Các theme theo mùa (predefined themes)
    predefined_themes = {
        "Giáng Sinh": {"color": "Fore.LIGHTCYAN_EX", "font": "slant"},
        "Quốc Khánh": {"color": "Fore.LIGHTRED_EX", "font": "standard", "date_display": True},  # Thêm date_display
        "Tết": {"color": "Fore.LIGHTYELLOW_EX", "font": "bubble"},
        "Halloween": {"color": "Fore.LIGHTMAGENTA_EX", "font": "barbwire"},
    }

    # Thêm các lựa chọn theme
    theme_type_choices = ["Theme tùy chỉnh", "Giáng Sinh", "Quốc Khánh", "Tết", "Halloween", "Quay lại"]

    # Câu hỏi về lựa chọn loại theme
    theme_type_question = [
        inquirer.List(
            'theme_type',
            message="Chọn loại theme:",
            choices=theme_type_choices
        )
    ]

    # Nhận câu trả lời cho loại theme
    theme_type_answer = inquirer.prompt(theme_type_question)

    # Kiểm tra nếu người dùng chọn "Quay lại" ở bước chọn loại theme
    if theme_type_answer['theme_type'] == "Quay lại":
        print("Đã quay lại menu chính.")
        return  # Thoát khỏi hàm, quay lại menu chính

    # Nếu người dùng chọn theme theo mùa
    if theme_type_answer['theme_type'] != "Theme tùy chỉnh":
        selected_theme = predefined_themes[theme_type_answer['theme_type']]

        # Lưu theme vào file JSON
        settings = {
            "color": selected_theme['color'],
            "art_style": selected_theme['font'],
            "use_random_colors": False,
            "program_name": "Zero Spending",
            "show_time": False,
            "time_font_style": "banner3",
            "change_title_color": False,
            "title_color_choice": "Không đổi màu (trắng)"
        }
        save_theme_settings(settings)

        # Nếu là theme Quốc Khánh, hiển thị ngày 2/9/1945 và số ngày còn lại
        if theme_type_answer['theme_type'] == "Quốc Khánh" and selected_theme.get("date_display"):
            print("Ngày Quốc Khánh: 2/9/1945")
            days_left = days_until_september_2()
            print(f"Còn {days_left} ngày nữa đến ngày Quốc Khánh.")

        print(f"Theme {theme_type_answer['theme_type']} đã được áp dụng.")
        return  # Thoát ngay sau khi áp dụng theme

    # Nếu người dùng chọn theme tùy chỉnh
    elif theme_type_answer['theme_type'] == "Theme tùy chỉnh":
        # Các câu hỏi về cài đặt theme
        theme_questions = [
            inquirer.List(
                'color_choice',
                message="Chọn màu cho theme chung:",
                choices=theme_choices
            ),
            inquirer.List(
                'font_choice',
                message="Chọn font chữ:",
                choices=font_choices
            ),
            inquirer.Text(
                'program_name',
                message="Đổi tên chương trình (hoặc để trống nếu không muốn đổi)",
                default="Zero Spending"
            ),
            inquirer.Confirm(
                'use_random_colors',
                message="Bạn có muốn sử dụng màu ngẫu nhiên cho đường gạch?",
                default=False
            ),
            inquirer.Confirm(
                'show_time',
                message="Bạn có muốn hiển thị thời gian và ngày tháng?",
                default=True
            ),
            inquirer.Confirm(
                'change_title_color',
                message="Chỉnh sửa màu tiêu đề?",
                default=False
            )
        ]

        # Lấy câu trả lời từ người dùng
        theme_answer = inquirer.prompt(theme_questions)

        # Kiểm tra nếu người dùng chọn "Quay lại" ở câu hỏi về màu
        if theme_answer['color_choice'] == "Quay lại" or theme_answer['font_choice'] == "quay lại":
            print("Đã quay lại menu chính.")
            return  # Thoát khỏi hàm, quay lại menu chính

        # Kiểm tra nếu người dùng chọn hiển thị thời gian, hỏi thêm về font cho thời gian
        if theme_answer['show_time']:
            time_font_question = inquirer.List(
                'time_font_choice',
                message="Chọn style cho font chữ hiển thị thời gian:",
                choices=font_choices,
                default="banner3"  # Mặc định 'banner3' như ban đầu
            )
            time_font_answer = inquirer.prompt([time_font_question])
            if time_font_answer['time_font_choice'] == "quay lại":
                print("Đã quay lại menu chính.")
                return  # Thoát khỏi hàm, quay lại menu chính
            time_font_choice = time_font_answer['time_font_choice']
        else:
            time_font_choice = 'banner3'  # Mặc định là 'banner3' nếu không chọn hiển thị thời gian

        selected_color = theme_colors.get(theme_answer['color_choice'], "Fore.LIGHTRED_EX")
        selected_font = theme_answer['font_choice']
        program_name = theme_answer['program_name'] if theme_answer['program_name'] else "Zero Spending"
        use_random_colors = theme_answer['use_random_colors']
        show_time = theme_answer['show_time']
        change_title_color = theme_answer['change_title_color']

        # Nếu người dùng chọn đổi màu tiêu đề, tiếp tục hỏi về chi tiết đổi màu tiêu đề
        if change_title_color:
            title_color_questions = [
                inquirer.List(
                    'title_color_choice',
                    message="Bạn muốn đổi màu tiêu đề như thế nào?",
                    choices=["Không đổi màu (trắng)", "Sử dụng màu đại diện", "Sử dụng màu ngẫu nhiên"]
                )
            ]
            title_color_answer = inquirer.prompt(title_color_questions)
            if title_color_answer['title_color_choice'] == "Quay lại":
                print("Đã quay lại menu chính.")
                return  # Thoát khỏi hàm, quay lại menu chính
        else:
            title_color_answer = {'title_color_choice': 'Không đổi màu (trắng)'}

        # Lưu theme vào file JSON
        settings = {
            "color": selected_color,
            "art_style": selected_font,
            "use_random_colors": use_random_colors,
            "program_name": program_name,
            "show_time": show_time,
            "time_font_style": time_font_choice,  # Lưu font chữ thời gian
            "change_title_color": change_title_color,
            "title_color_choice": title_color_answer['title_color_choice']  # Lưu lựa chọn màu tiêu đề
        }
        save_theme_settings(settings)

        print(f"Theme đã được lưu với màu {theme_answer['color_choice']}, kiểu chữ {theme_answer['font_choice']}.")
    else:
        print("Đã quay lại menu chính.")


