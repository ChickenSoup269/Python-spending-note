from business import *

# View the menu
def view_menu():
    menu = load_menu()

    if not menu:
        print("Menu hiện đang trống.")
        return

    # Tạo danh sách hàng cho bảng
    table = []
    for product_name, details in menu.items():
        table.append([
            f"{Fore.CYAN}{product_name}{Style.RESET_ALL}",
            f"{Fore.GREEN}{details['price']:,}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{details['stock']}{Style.RESET_ALL}"
        ])

    # Tạo tiêu đề cho bảng
    headers = [
        f"{Fore.MAGENTA}Tên sản phẩm{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Giá (VNĐ){Style.RESET_ALL}",
        f"{Fore.MAGENTA}Số lượng tồn kho{Style.RESET_ALL}"
    ]

    # Hiển thị bảng với tabulate
    print(tabulate(table, headers=headers, tablefmt='rounded_outline'))