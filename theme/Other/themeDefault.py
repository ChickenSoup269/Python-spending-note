# In ra lời chào đầu 
from imports import *

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
# bigchief
    # Các theme theo mùa (predefined themes)
    
    predefined_themes = {
        "Quốc Khánh": {"color": "Fore.LIGHTRED_EX", "font": "starwars", "width" : "120", "program_name": "Quốc Khánh"},
        "Christmas": {"color": "Fore.LIGHTCYAN_EX", "font": "isometric1","width": "250", "program_name": "Christmas"},
        "Tết": {"color": "Fore.LIGHTYELLOW_EX", "font": "epic","width" : "120",  "program_name": "Tết"},
        "Halloween": {"color": "Fore.LIGHTMAGENTA_EX", "font": "doom", "width" : "120", "program_name": "Halloween"},
        "Mặc định": {
            "color": "Fore.LIGHTWHITE_EX",
            "font": "standard",
            "width" : "120",
            "program_name": "Zero Spending",
            "use_random_colors": True,
            "show_time": True,
            "time_font_style": "banner3",
            "change_title_color": False,
            "title_color_choice": "Không đổi màu (trắng)",
            "time_format": "time"
        }
    }

    # Thêm các lựa chọn theme
    theme_type_choices = ["Theme tùy chỉnh","Quốc Khánh", "Christmas", "Tết", "Halloween", "Mặc định", "Quay lại"]

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

    # Nếu người dùng chọn theme theo mùa hoặc theme mặc định
    if theme_type_answer['theme_type'] in predefined_themes:
        selected_theme = predefined_themes[theme_type_answer['theme_type']]

        # Lưu theme vào file JSON
        settings = {
            "color": selected_theme['color'],
            "art_style": selected_theme['font'],
            "width" : selected_theme['width'],
            "use_random_colors": selected_theme.get('use_random_colors', False),
            "program_name": unidecode(selected_theme['program_name']),  
            "show_time": selected_theme.get('show_time', False),
            "time_font_style": selected_theme.get('time_font_style', "banner3"),
            "change_title_color": selected_theme.get('change_title_color', False),
            "title_color_choice": selected_theme.get('title_color_choice', "Không đổi màu (trắng)"),
            "time_format": selected_theme.get('time_format', "none")  
        }
        save_theme_settings(settings)
        print(f"Theme '{theme_type_answer['theme_type']}' đã được lưu.")
      
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
            ),
            inquirer.Text(
                'width_choice',  # Thêm câu hỏi width
                message="Nhập độ rộng (width) của chương trình (mặc định là 120):",
                default="120"
            )
        ]

        # Lấy câu trả lời từ người dùng
        theme_answer = inquirer.prompt(theme_questions)

        if theme_answer['color_choice'] == "Ngẫu nhiên" or theme_answer['font_choice'] == "quay lại":
            print("Đã quay lại menu chính.")
            return  

        # Kiểm tra nếu người dùng chọn hiển thị thời gian, hỏi thêm về kiểu hiển thị thời gian
        if theme_answer['show_time']:
            time_display_choice = [
                inquirer.List(
                    'time_format',
                    message="Bạn muốn hiển thị gì?",
                    choices=[
                        ('Chỉ giờ (HH:MM:SS)', 'time'),
                        ('Chỉ ngày (dd/mm/yyyy)', 'date'),
                        ('Cả ngày và giờ (dd/mm/yyyy HH:MM:SS)', 'both')
                    ]
                )
            ]
            time_display_answer = inquirer.prompt(time_display_choice)

            time_font_question = inquirer.List(
                'time_font_choice',
                message="Chọn style cho font chữ hiển thị thời gian:",
                choices=font_choices,
                default="banner3"  
            )
            time_font_answer = inquirer.prompt([time_font_question])

            if time_font_answer['time_font_choice'] == "quay lại":
                print("Đã quay lại menu chính.")
                return  
            time_font_choice = time_font_answer['time_font_choice']
        else:
            time_font_choice = 'banner3' 
            time_display_answer = {'time_format': 'none'}

        selected_color = theme_colors.get(theme_answer['color_choice'], "Fore.LIGHTRED_EX")
        selected_font = theme_answer['font_choice']
        selected_width = theme_answer['width_choice']
        program_name = unidecode(theme_answer['program_name']) if theme_answer['program_name'] else "Zero Spending"
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
            "width": selected_width,
            "use_random_colors": use_random_colors,
            "program_name": program_name,  # Tên chương trình do người dùng tùy chỉnh
            "show_time": show_time,
            "time_font_style": time_font_choice,  # Lưu font chữ thời gian
            "change_title_color": change_title_color,
            "title_color_choice": title_color_answer['title_color_choice'],  # Lưu lựa chọn màu tiêu đề
            "time_format": time_display_answer['time_format']  # Lưu lựa chọn hiển thị giờ/ngày/cả hai
        }
        save_theme_settings(settings)

        print(f"Theme đã được lưu với màu {theme_answer['color_choice']}, kiểu chữ {theme_answer['font_choice']}.")
    else:
        print("Đã quay lại menu chính.")
