from expenses import *


# Tính chi tiêu trong tháng
def calculate_monthly_totals(num_months=12):
    today = datetime.now().date()
    monthly_totals = []
    month_labels = []

    for i in range(num_months):
        # Xác định tháng bắt đầu và kết thúc
        start_of_month = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        total_monthly = 0
        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_of_month <= date_obj <= end_of_month:
                    for item in items:
                        total_monthly += item['amount']
        
        monthly_totals.append(total_monthly)
        month_labels.append(start_of_month.strftime('%m/%Y'))

    return monthly_totals[::-1], month_labels[::-1]  # Đảo ngược để tháng gần nhất lên đầu
def plot_monthly_comparison(num_months=12):
    monthly_totals, month_labels = calculate_monthly_totals(num_months)
    
    # Tạo bảng dữ liệu cho rich
    table = Table(title=f'Chi tiêu trong {num_months} tháng gần đây', title_style="bold blue")

    table.add_column("Tháng", style="bold green")
    table.add_column("Tổng chi tiêu (VNĐ)", style="bold magenta")

    # Xác định tháng hiện tại
    current_month = datetime.now().strftime('%m/%Y')

    for month, total in zip(month_labels, monthly_totals):
        if month == current_month:
            table.add_row(f"[bold yellow]{month}[/bold yellow]", f"[bold yellow]{total:,.0f} VNĐ[/bold yellow]")
        else:
            table.add_row(month, f"{total:,.0f}")

    # Hiển thị bảng với rich
    console.print(table)

    # Vẽ biểu đồ cột với rich
    plot_data = {month: total for month, total in zip(month_labels, monthly_totals)}

    # Tạo biểu đồ cột với rich
    bar_chart = ""
    max_label_length = max(len(label) for label in month_labels)
    max_value = max(monthly_totals)
    
    for month in month_labels:
        value = plot_data[month]
        bar_length = int((value / max_value) * 40)  # Quy định chiều dài cột

        if month == current_month:
            bar_chart += f"[bold yellow]{month.ljust(max_label_length)}[/bold yellow] | [bold yellow]{'█' * bar_length}[/bold yellow] [bold yellow]{value:,.0f} VNĐ[/bold yellow]\n"
        else:
            bar_chart += f"{month.ljust(max_label_length)} | {'█' * bar_length} {value:,.0f}\n"
    
    # Hiển thị biểu đồ cột
    console.print(Panel(bar_chart, title="Biểu đồ cột chi tiêu", title_align="left"))

    # Thêm ghi chú dưới biểu đồ
    note = "Ghi chú: Biểu đồ thể hiện tổng chi tiêu mỗi tháng trong 12 tháng gần đây."
    console.print(f"\n[note] {note}")


# Tính chi tiêu trong tháng
def monthly_expenses():
    today = datetime.now().date()
    total_monthly = 0
    monthly_expenses_list = []
    categories = []
    amounts = []

    # Xác định số ngày trong tháng hiện tại tính đến hôm nay
    days_in_month = today.day

    # Tính ngày bắt đầu và ngày kết thúc của tháng trước
    first_day_this_month = today.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    total_last_month = 0
    last_month_expenses = {}

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Tính chi tiêu cho tháng hiện tại
            if date_obj.year == today.year and date_obj.month == today.month:
                if date_obj <= today:  
                    for item in items:
                        total_monthly += item['amount']
                        monthly_expenses_list.append({
                            'date': date_str,
                            'category': item['category'],
                            'description': item['description'],
                            'quantity': item['quantity'],
                            'amount': item['amount']
                        })
                        if item['category'] not in categories:
                            categories.append(item['category'])
                            amounts.append(item['amount'])
                        else:
                            index = categories.index(item['category'])
                            amounts[index] += item['amount']

            # Tính chi tiêu tháng trước
            if first_day_previous_month <= date_obj <= last_day_previous_month:
                for item in items:
                    total_last_month += item['amount']
                    if item['category'] not in last_month_expenses:
                        last_month_expenses[item['category']] = item['amount']
                    else:
                        last_month_expenses[item['category']] += item['amount']

    print(f"Chi tiêu tháng {today.strftime('%m/%Y')}:")

    if monthly_expenses_list:
        print(format_expenses_table(monthly_expenses_list))
        plot_expenses(categories, amounts, 'Chi tiêu trong tháng')
        plot_monthly_comparison(12)
    else:
        print("Không có chi tiêu nào trong tháng này.")
    
    # Tính chi tiêu trung bình một ngày trong 1 tháng
    average_daily_spending = total_monthly / days_in_month
    print(f"Tổng chi tiêu tháng này: {total_monthly:,} VNĐ")
    print(Fore.LIGHTMAGENTA_EX + f"Chi tiêu trung bình mỗi ngày trong tháng: {average_daily_spending:,.0f} VNĐ\n")

    # So sánh chi tiêu tháng trước và tháng hiện tại
    difference = total_monthly - total_last_month
    if difference > 0:
        print(Fore.RED + f"Bạn đã chi tiêu nhiều hơn tháng trước {difference:,} VNĐ.")
    elif difference < 0:
        print(Fore.GREEN + f"Bạn đã chi tiêu ít hơn tháng trước {abs(difference):,} VNĐ.")
    else:
        print(Fore.BLUE + "Chi tiêu tháng này không đổi so với tháng trước.")

    print(Fore.CYAN + f"Tổng chi tiêu tháng trước: {total_last_month:,} VNĐ\n")

# =================================================================