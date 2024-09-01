from business import *

# Tính toán trong kinh doanh
def add_product():
    menu = load_menu()

    while True:
        product_name = input("Nhập tên sản phẩm: ")
       
        product_price = input("Nhập giá sản phẩm (VNĐ): ")
        try:
            product_price = float(product_price)
            if product_price <= 0:
                print("Giá sản phẩm phải lớn hơn 0. Vui lòng nhập lại.")
                continue
        except ValueError:
            print("Giá sản phẩm không hợp lệ. Vui lòng nhập lại.")
            continue

        break

    menu[product_name] = {
        "price": product_price,
        "stock": 0  # Initial stock is set to 0
    }

    save_menu(menu)
    print(f"Đã thêm sản phẩm: {product_name} với giá {product_price:,} VNĐ vào menu.")