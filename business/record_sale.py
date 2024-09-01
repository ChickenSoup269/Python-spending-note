from business import *

# Record a sale
def record_sale():
    menu = load_menu()

    if not menu:
        print("Menu hiện đang trống. Vui lòng thêm sản phẩm trước.")
        return

    questions = [
        inquirer.List(
            'product',
            message="Chọn sản phẩm bạn muốn bán",
            choices=list(menu.keys()),
        )
    ]
    answer = inquirer.prompt(questions)
    product_name = answer['product']

    available_stock = menu[product_name]['stock']
    if available_stock <= 0:
        print(f"Sản phẩm {product_name} hiện đã hết hàng.")
        return

    quantity_sold = int(input(f"Nhập số lượng bán ra (tồn kho hiện tại: {available_stock}): "))
    
    if quantity_sold > available_stock:
        print("Số lượng bán ra không đủ tồn kho. Vui lòng nhập lại.")
        return
    
    # Update the stock
    menu[product_name]['stock'] -= quantity_sold
    total_sale = quantity_sold * menu[product_name]['price']
    
    save_menu(menu)
    print(f"Đã bán {quantity_sold} {product_name} với tổng số tiền {total_sale:,.0f} VNĐ.")
    
    # Add sale information to the expense record
    date_str = datetime.now().strftime("%Y-%m-%d")
    if date_str not in expenses:
        expenses[date_str] = []

    expenses[date_str].append({
        'category': 'Doanh thu bán hàng',
        'description': f"Bán {quantity_sold} {product_name}",
        'quantity': quantity_sold,
        'amount': total_sale
    })
    print(f"Đã ghi nhận doanh thu vào chi tiêu ngày {date_str}.")