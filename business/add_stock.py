from business import *

# Add stock to existing products
def add_stock():
    menu = load_menu()
    
    if not menu:
        print("Menu hiện đang trống. Vui lòng thêm sản phẩm trước.")
        return

    questions = [
        inquirer.List(
            'product',
            message="Chọn sản phẩm bạn muốn thêm số lượng",
            choices=list(menu.keys()),
        )
    ]
    answer = inquirer.prompt(questions)
    product_name = answer['product']

    quantity = int(input(f"Nhập số lượng thêm vào cho {product_name}: "))
    menu[product_name]['stock'] += quantity

    save_menu(menu)
    print(f"Đã thêm {quantity} vào số lượng của {product_name}. Số lượng hiện tại: {menu[product_name]['stock']}")
