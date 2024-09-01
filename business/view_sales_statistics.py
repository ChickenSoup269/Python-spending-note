from business import *

def calculate_sales_last_4_weeks():
    today = datetime.now().date()
    sales_last_4_weeks = []
    sales_details = {}

    for i in range(4):
        start_of_week = today - timedelta(days=today.weekday() + i * 7)
        end_of_week = start_of_week + timedelta(days=6)
        week_label = f"Tuần {start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m')}"

        total_sales = 0
        product_sales = defaultdict(int)

        for date_str, items in expenses.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print(f"Warning: Bỏ qua dữ liệu không hợp lệ {date_str}")
                continue

            if start_of_week <= date_obj <= end_of_week:
                for item in items:
                    if item['category'] == 'Doanh thu bán hàng':
                        total_sales += item['amount']
                        product_name = item['description'].split(" ")[1]  # Assuming product name is the second word
                        product_sales[product_name] += item['quantity']

        sales_last_4_weeks.append((week_label, total_sales))
        sales_details[week_label] = dict(product_sales)  # Convert defaultdict to regular dict

    # Reverse the list and maintain dictionary order
    sales_last_4_weeks = sales_last_4_weeks[::-1]
    sales_details = dict(reversed(list(sales_details.items())))

    return sales_last_4_weeks, sales_details

def find_best_selling_product(sales_details):
    product_sales_count = {}

    for week_sales in sales_details.values():
        for product_name, quantity_sold in week_sales.items():
            product_sales_count[product_name] = product_sales_count.get(product_name, 0) + quantity_sold

    # Check if product_sales_count is empty
    if not product_sales_count:
        return "Chưa có dữ liệu bán hàng", 0

    best_selling_product = max(product_sales_count, key=product_sales_count.get)
    return best_selling_product, product_sales_count[best_selling_product]

def view_sales_statistics():
    sales_last_4_weeks, sales_details = calculate_sales_last_4_weeks()

    table = Table(title="Doanh thu trong 4 tuần gần đây", title_style="bold blue")
    table.add_column("Tuần", style="bold green")
    table.add_column("Tổng doanh thu (VNĐ)", style="bold magenta")

    for week_label, total_sales in sales_last_4_weeks:
        table.add_row(week_label, f"{total_sales:,.0f}")

    console.print(table)

    best_selling_product, quantity_sold = find_best_selling_product(sales_details)
    console.print(f"Sản phẩm bán chạy nhất: [bold red]{best_selling_product}[/bold red] với [bold yellow]{quantity_sold}[/bold yellow] sản phẩm bán ra trong 4 tuần qua.")

    for week_label, product_sales in sales_details.items():
        console.print(f"\nChi tiết sản phẩm bán ra trong {week_label}:")
        if product_sales:
            for product, quantity in product_sales.items():
                console.print(f"{product}: {quantity} sản phẩm")
        else:
            console.print("Không có sản phẩm nào được bán trong tuần này.")
