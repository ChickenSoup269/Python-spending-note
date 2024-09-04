from savings import *
from .display_savings_book import display_savings_book

# Function to add savings
def add_savings(amount, description):
    today = datetime.now()
    date = today.strftime('%Y-%m-%d')
    weekday_name = today.strftime('%A')  # Lấy tên thứ (ví dụ: "Monday")

    # Kiểm tra nếu ngày hôm nay chưa có trong savings
    if date not in savings:
        savings[date] = []

    # Thêm thông tin tiết kiệm vào danh sách
    savings[date].append({
        "amount": amount,
        "description": description,
        "weekday": weekday_translation.get(weekday_name)
    })

    # Lưu dữ liệu
    save_expenses()

    # Thông báo cho người dùng
    print(display_savings_book())
    print(Fore.GREEN + f"Đã thêm tiết kiệm: {amount:,} VNĐ vào ngày {date} ({weekday_translation.get(weekday_name)}) \n" + Style.RESET_ALL)
