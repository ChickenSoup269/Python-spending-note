from savings import *

def display_savings_book():
    if not savings:
        print(Fore.RED + "Không có dữ liệu tiết kiệm để hiển thị." + Style.RESET_ALL)
        return
    
    table_data = []
    
    # Thêm tiêu đề bảng
    headers = [Fore.CYAN + "Ngày" + Style.RESET_ALL, 
               Fore.CYAN + "Số Tiền (VNĐ)" + Style.RESET_ALL, 
               Fore.CYAN + "Ngày Trong Tuần" + Style.RESET_ALL]

    total_amount = 0
    
    for date, details in savings.items():
        table_data.append([
            date,
            f"{details['amount']:,}",
            details['weekday']
        ])
        total_amount += details['amount']

    # In bảng ra với màu sắc
    print(Fore.GREEN + tabulate(table_data, headers=headers, tablefmt="rounded_outline") + Style.RESET_ALL)
    
    # In tổng số tiền
    print(Fore.YELLOW + f"Tổng tiền tiết kiệm: {total_amount:,} VNĐ" + Style.RESET_ALL)
