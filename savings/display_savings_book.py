from savings import *

def display_savings_book():
    if not savings:
        print(Fore.RED + "Không có dữ liệu tiết kiệm để hiển thị." + Style.RESET_ALL)
        return

    table_data = []

    # Thêm tiêu đề bảng
    headers = [Fore.GREEN + "Ngày" + Style.RESET_ALL, 
               Fore.BLUE + "Số Tiền (VNĐ)" + Style.RESET_ALL, 
               Fore.YELLOW + "Mô Tả" + Style.RESET_ALL,
               Fore.RED + "Ngày Trong Tuần" + Style.RESET_ALL]

    total_amount = 0

    for date, entries in savings.items():
        # Kiểm tra xem entries có phải là danh sách không
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict):
                    table_data.append([
                        date,
                        f"{entry['amount']:,}",
                        entry.get('description', 'Không mô tả'),
                        entry['weekday']
                    ])
                    total_amount += entry['amount']
                else:
                    print(Fore.RED + f"Lỗi: Mục tiết kiệm không phải là từ điển: {entry}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Lỗi: Dữ liệu cho ngày {date} không phải là danh sách: {entries}" + Style.RESET_ALL)

    # In bảng ra với màu sắc
    print(Fore.GREEN + tabulate(table_data, headers=headers, tablefmt="rounded_outline") + Style.RESET_ALL)

    # In tổng số tiền
    print(Fore.YELLOW + f"Tổng tiền tiết kiệm: {total_amount:,} VNĐ" + Style.RESET_ALL)