from savings import *

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
