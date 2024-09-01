from expenses import *

def yearly_expenses(year=None):
    if year is None:
        year = datetime.now().year

    today = datetime.now().date()
    total_yearly = 0
    yearly_expenses_list = []
    categories = []
    amounts = []

    # Xác định số ngày trong năm tính đến ngày hôm nay
    days_in_year = (today - datetime(year, 1, 1).date()).days + 1

    last_year = year - 1
    total_last_year = 0
    last_year_expenses = {}

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.year == year:
                if date_obj <= today:  
                    for item in items:
                        total_yearly += item['amount']
                        yearly_expenses_list.append({
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

            # Tính chi tiêu năm trước
            if date_obj.year == last_year:
                for item in items:
                    total_last_year += item['amount']
                    if item['category'] not in last_year_expenses:
                        last_year_expenses[item['category']] = item['amount']
                    else:
                        last_year_expenses[item['category']] += item['amount']
    print(f"Chi tiêu trong năm {year}:")

    if yearly_expenses_list:
        print(format_expenses_table(yearly_expenses_list))
        plot_expenses(categories, amounts, f'Chi tiêu trong năm {year}')
        compare_years_expenses()
    else:
        print(f"Không có chi tiêu nào trong năm {year}.")
    
    # Tính trung bình chi tiêu một ngày trong năm
    average_daily_spending = total_yearly / days_in_year
    print(f"Tổng chi tiêu năm: {total_yearly:,} VNĐ")
    print(Fore.LIGHTMAGENTA_EX + f"Chi tiêu trung bình mỗi ngày trong năm: {average_daily_spending:,.0f} VNĐ\n")

    # So sánh chi tiêu năm trước với năm hiện tại
    difference = total_yearly - total_last_year
    if difference > 0:
        print(Fore.RED + f"Bạn đã chi tiêu nhiều hơn năm trước {difference:,} VNĐ.")
    elif difference < 0:
        print(Fore.GREEN + f"Bạn đã chi tiêu ít hơn năm trước {abs(difference):,} VNĐ.")
    else:
        print(Fore.GREEN + "Chi tiêu năm này không đổi so với năm trước.")

    print(Fore.CYAN + f"Tổng chi tiêu năm trước: {total_last_year:,} VNĐ\n")

def yearly_expenses_by_day(year):
    start_date = datetime(year, 1, 1).date()
    end_date = datetime(year, 12, 31).date()
    daily_expenses = {}
    total_yearly = 0

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date_obj <= end_date:
                if date_str not in daily_expenses:
                    daily_expenses[date_str] = 0
                for item in items:
                    daily_expenses[date_str] += item['amount']
                    total_yearly += item['amount']

    dates = []
    amounts = []

    for date_str in sorted(daily_expenses.keys()):
        dates.append(date_str)
        amounts.append(daily_expenses[date_str])

    if not dates:
        print(f"Không có chi tiêu nào trong năm {year}.")
        return

    # Apply color to the table title
    table = Table(title=f'[bold blue]Chi tiêu hàng ngày trong năm {year}[/bold blue]', title_style="bold blue")
    table.add_column("[bold green]Ngày[/bold green]", style="bold green")
    table.add_column("[bold cyan]Thứ[/bold cyan]", style="bold cyan")
    table.add_column("[bold magenta]Chi tiêu (VNĐ)[/bold magenta]", style="bold magenta")

    for date, amount in zip(dates, amounts):
        day_name_vn = weekday_translation.get(datetime.strptime(date, "%Y-%m-%d").strftime('%A'), "")
        table.add_row(date, day_name_vn, f"{amount:,.0f}")

    console.print(table)

    plot_data = {date: amount for date, amount in zip(dates, amounts)}
    
    max_value = max(amounts) if amounts else 0
    bar_chart = ""
    # Fix (ngày và thứ) có cùng độ dài
    max_label_length = max(len(f"{date} ({weekday_translation[datetime.strptime(date, '%Y-%m-%d').strftime('%A')]})") for date in dates)

    color = "yellow"  # Chọn màu cho cột

    if max_value > 0:
        for date in dates:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            weekday_str = weekday_translation[date_obj.strftime('%A')]  # Lấy tên thứ trong tuần
            label = f"{date} - {weekday_str}".ljust(max_label_length)  # Canh lề trái bằng cách thêm khoảng trắng

            value = plot_data[date]
            bar_length = int((value / max_value) * 50)
            bar_chart += f"{label} | [bold {color}]{'█' * bar_length}[/bold {color}] {value:,.0f} VNĐ\n"
    else:
        bar_chart = "Không có dữ liệu chi tiêu để hiển thị."

    # Sử dụng màu sắc cho biểu đồ
    bar_chart_colored = Text.from_markup(bar_chart)

    # Apply color to the panel title
    console.print(Panel(bar_chart_colored, title=f"[bold cyan]Biểu đồ cột chi tiêu hàng ngày {year}[/bold cyan]", title_align="left"))

    note = f"Ghi chú: Biểu đồ thể hiện tổng chi tiêu hàng ngày trong năm {year}."
    console.print(f"\n[italic yellow]{note}[/italic yellow]") 

def compare_years_expenses(year=None):
    if year is None:
        year = datetime.now().year

    previous_year = year - 1
    next_year = year + 1

    years_to_check = [previous_year, year, next_year]

    for y in years_to_check:
        print(f"\nChi tiêu trong năm {y}:")
        yearly_expenses_by_day(y)

    def get_yearly_totals(year):
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        total = 0
        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_date <= date_obj <= end_date:
                    for item in items:
                        total += item['amount']
        return total

    totals = {y: get_yearly_totals(y) for y in years_to_check}

    totals = {y: total for y, total in totals.items() if total > 0}

    if not totals:
        print("Không có chi tiêu nào trong các năm gần đây.")
        return

    table = Table(title=f"So sánh chi tiêu hàng năm", title_style="bold blue")
    table.add_column("Năm", style="bold green")
    table.add_column("Tổng chi tiêu (VNĐ)", style="bold magenta")

    for y, total in totals.items():
        table.add_row(str(y), f"{total:,.0f}")

    console.print(table)

    max_value = max(totals.values()) if totals.values() else 0
    bar_chart = ""
    max_label_length = max(len(str(y)) for y in totals.keys())
    
    color = "cyan"  # Chọn màu cho cột

    if max_value > 0:
        for y, total in totals.items():
            bar_length = int((total / max_value) * 40)
            bar_chart += f"{str(y).ljust(max_label_length)} | {'█' * bar_length} {total:,.0f}\n"
    else:
        bar_chart = "Không có dữ liệu chi tiêu để hiển thị."

    # Sử dụng màu sắc cho biểu đồ
    bar_chart_colored = Text.from_markup(f"[{color}] {bar_chart}[/]", style="bold")

    console.print(Panel(bar_chart_colored, title="Biểu đồ cột so sánh chi tiêu hàng năm", title_align="left"))

    note = "Ghi chú: Biểu đồ so sánh tổng chi tiêu hàng năm giữa ba năm gần nhất."
    console.print(f"\n[note] {note}")


