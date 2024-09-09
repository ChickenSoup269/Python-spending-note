from expenses import *

# Hàm tìm kiếm chi tiêu theo mô tả
def search_expenses_by_description():
    expenses = load_expenses()

    if not expenses:
        print(Fore.RED + "Không có chi tiêu nào để tìm kiếm." + Style.RESET_ALL)
        return

  
    search_keyword = input("Nhập từ khóa để tìm kiếm mô tả chi tiêu: ").strip()

    # Tìm các chi tiêu khớp với từ khóa trong mô tả
    matching_expenses = []
    total_amount = 0  # lưu tổng số tiền của các chi tiêu khớp

    for user, records in expenses.items():
        for date_str, items in records.items():
            for item in items:
                # Tìm các chi tiêu có mô tả chứa từ khóa (dùng regex không phân biệt hoa thường)
                if re.search(search_keyword, item.get('description', ''), re.IGNORECASE):
                    matching_expenses.append((user, date_str, item))
                    total_amount += item.get('amount', 0) * item.get('quantity', 1)  # Tính tổng

    if not matching_expenses:
        print(Fore.YELLOW + f"Không tìm thấy chi tiêu nào với mô tả chứa từ khóa '{search_keyword}'." + Style.RESET_ALL)
        return

    # Bước 3: Hiển thị danh sách chi tiêu khớp với từ khóa
    print(Fore.CYAN + f"Chi tiêu có chứa từ khóa '{search_keyword}':" + Style.RESET_ALL)
    table_data = []
    for user, date_str, item in matching_expenses:
        table_data.append([
            date_str,
            item.get('category', 'Không danh mục'),
            item.get('description', 'Không mô tả'),
            item.get('quantity', 'Không số lượng'),
            f"{item.get('amount', 0) * item.get('quantity', 1):,} VNĐ"
        ])

   
    table_data.append([
        Fore.GREEN + "Tổng" + Style.RESET_ALL,  # Dòng đầu tiên cho "Tổng"
        "",  # Các ô trống khác
        "",
        "",
        Fore.GREEN + f"{total_amount:,} VNĐ" + Style.RESET_ALL  # Tổng số tiền
    ])

    #  header và in bảng
    headers = [
        Fore.MAGENTA + "Ngày" + Style.RESET_ALL, 
        Fore.MAGENTA + "Loại chi tiêu" + Style.RESET_ALL, 
        Fore.MAGENTA + "Mô tả" + Style.RESET_ALL, 
        Fore.MAGENTA + "Số lượng" + Style.RESET_ALL, 
        Fore.MAGENTA + "Tổng tiền (VNĐ)" + Style.RESET_ALL
    ]
    
    print(Fore.LIGHTBLUE_EX + tabulate(table_data, headers=headers, tablefmt="rounded_outline") + Style.RESET_ALL)

    # Kết thúc tìm kiếm
    input(Fore.YELLOW + "Nhấn Enter để quay lại menu." + Style.RESET_ALL)