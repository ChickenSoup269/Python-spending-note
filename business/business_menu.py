from business import *


def business_menu():
    while True:
        business_choices = [
            "Thêm sản phẩm vào menu",
            "Thêm số lượng sản phẩm",
            "Xem menu sản phẩm",
            "Ghi nhận bán hàng",
            "Thống kê doanh thu",
            "Quay lại"
        ]

        business_questions = [
            inquirer.List(
                'choice',
                message= 5*'*' + " Chọn chức năng bạn muốn thực hiện "  + 5*'*',
                choices=business_choices,
            )
        ]

        business_answer = inquirer.prompt(business_questions)

        if business_answer['choice'] == "Thêm sản phẩm vào menu":
            print(40*'=*=')
            add_product()
        elif business_answer['choice'] == "Thêm số lượng sản phẩm":
            print(40*'=*=')
            add_stock()
        elif business_answer['choice'] == "Xem menu sản phẩm":
            print(40*'=*=')
            view_menu()
        elif business_answer['choice'] == "Ghi nhận bán hàng":
            print(40*'=*=')
            record_sale()
        elif business_answer['choice'] == "Thống kê doanh thu":
            print(40*'=*=')
            view_sales_statistics()
        elif business_answer['choice'] == "Quay lại":
            break
