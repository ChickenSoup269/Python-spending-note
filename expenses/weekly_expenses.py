from expenses import *

# Tính chiêu tiêu trong tuần
def weekly_expenses():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    total_weekly = 0
    daily_spendings = [0] * 7  # Create a list with 7 zeros to hold daily spending
    weekly_expenses_list = []
    categories = []
    amounts = []

    # Prepare data to compare with the previous week
    last_week_start = start_of_week - timedelta(days=7)
    last_week_end = end_of_week - timedelta(days=7)
    last_week_expenses = {}
    total_last_week = 0

    for user_expenses in expenses.values():
        for date_str, items in user_expenses.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Calculate expenses for the current week
            if start_of_week <= date_obj <= today:
                day_index = (date_obj - start_of_week).days  # Calculate the day index (0 for Monday, 6 for Sunday)
                for item in items:
                    total_weekly += item['amount']
                    daily_spendings[day_index] += item['amount']  # Add amount to the correct day
                    weekly_expenses_list.append({
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

            # Calculate expenses for the previous week
            if last_week_start <= date_obj <= last_week_end:
                for item in items:
                    total_last_week += item['amount']  # Add to the total for last week
                    if item['category'] not in last_week_expenses:
                        last_week_expenses[item['category']] = item['amount']
                    else:
                        last_week_expenses[item['category']] += item['amount']

    start_day_vn = weekday_translation.get(start_of_week.strftime('%A'), start_of_week.strftime('%A'))
    end_day_vn = weekday_translation.get(today.strftime('%A'), today.strftime('%A'))

    print(f"Chi tiêu từ {start_day_vn} (ngày {start_of_week.strftime('%d/%m/%Y')}) đến {end_day_vn} (ngày {today.strftime('%d/%m/%Y')}):")

    if weekly_expenses_list:
        print(format_expenses_table(weekly_expenses_list))
        plot_expenses(categories, amounts, 'Chi tiêu trong tuần')
        plot_weekly_comparison(4)
    else:
        print("Không có chi tiêu nào trong tuần này.")
    
    # Tính số chi tiêu trong bình hằng ngày trong tuấn
    days_in_week = (today - start_of_week).days + 1  # tổng ngày trong tuần (including today)
    average_daily_spending = total_weekly / days_in_week
    print(f"Tổng chi tiêu tuần này: {total_weekly:,} VNĐ")
    print(Fore.LIGHTMAGENTA_EX + f"Chi tiêu trung bình mỗi ngày trong tuần: {average_daily_spending:,.0f} VNĐ\n") 

    # So sánh chi tiêu tuần trước
    difference = total_weekly - total_last_week
    if difference > 0:
        print(Fore.RED + f"Bạn đã chi tiêu nhiều hơn tuần trước {difference:,} VNĐ.")
    elif difference < 0:
        print(Fore.GREEN + f"Bạn đã chi tiêu ít hơn tuần trước {abs(difference):,} VNĐ.")
    else:
        print(Fore.BLUE + "Chi tiêu tuần này không đổi so với tuần trước.")

    print(Fore.YELLOW + f"Tổng chi tiêu tuần trước: {total_last_week:,} VNĐ\n")

def calculate_weekly_totals(num_weeks=4):
    today = datetime.now().date()
    weekly_totals = []
    week_labels = []

    for i in range(num_weeks):
        start_of_week = today - timedelta(days=today.weekday() + i * 7)
        end_of_week = start_of_week + timedelta(days=6)

        # Xác định tuần thứ mấy trong tháng
        week_of_month = (start_of_week.day - 1) // 7 + 1

        # Nếu tuần này nằm trong tháng trước, sử dụng nhãn tháng trước
        if start_of_week.month != today.month:
            week_label = f"Tuần {week_of_month} tháng {start_of_week.strftime('%m')}"
        else:
            week_label = f"Tuần {week_of_month} tháng {start_of_week.strftime('%m')}"

        total_weekly = 0
        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_of_week <= date_obj <= end_of_week:
                    for item in items:
                        total_weekly += item['amount']

        weekly_totals.append(total_weekly)
        week_labels.append(week_label)

    return weekly_totals[::-1], week_labels[::-1]  # Đảo ngược để tuần gần nhất lên đầu

def plot_weekly_comparison(num_weeks=4):
    weekly_totals, week_labels = calculate_weekly_totals(num_weeks)
    weekly_expenses = {label: [] for label in week_labels}

    today = datetime.now().date()
    current_week_label = week_labels[-1]  # Lấy nhãn của tuần hiện tại (tuần đầu tiên trong danh sách sau khi đảo ngược)

    for i in range(num_weeks):
        start_of_week = today - timedelta(days=today.weekday() + i * 7)
        end_of_week = start_of_week + timedelta(days=6)

        for user_expenses in expenses.values():
            for date_str, items in user_expenses.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if start_of_week <= date_obj <= end_of_week:
                    for item in items:
                        weekly_expenses[week_labels[i]].append({
                            'date': date_str,
                            'category': item['category'],
                            'description': item['description'],
                            'quantity': item['quantity'],
                            'amount': item['amount']
                        })

    # Tạo bảng dữ liệu cho rich
    table = Table(title=f'Chi tiêu trong {num_weeks} tuần gần đây', title_style="bold blue")
    table.add_column("Tuần", style="bold green")
    table.add_column("Tổng chi tiêu (VNĐ)", style="bold magenta")

    for week_label, total in zip(week_labels, weekly_totals):
        # Đổi màu tuần hiện tại
        if week_label == current_week_label:
            week_label = f"[bold red]{week_label}[/bold red]"
            total_str = f"[bold red]{total:,.0f}[/bold red]"
        else:
            total_str = f"{total:,.0f}"
        table.add_row(week_label, total_str)

    # Hiển thị bảng với rich
    console.print(table)

    # Vẽ biểu đồ cột với rich
    max_label_length = max(len(label) for label in week_labels)
    max_value = max(weekly_totals) if weekly_totals else 1

    bar_chart = ""
    for week_label in week_labels:
        value = weekly_totals[week_labels.index(week_label)]
        bar_length = int((value / max_value) * 40)  # Quy định chiều dài cột
        
        # Đổi màu tuần hiện tại trong biểu đồ
        if week_label.strip("[/bold red]") == current_week_label.strip("[/bold red]"):
            bar_chart += f"[bold red]{week_label.ljust(max_label_length)} | {'█' * bar_length} {value:,.0f} VNĐ[/bold red]\n"
        else:
            bar_chart += f"{week_label.ljust(max_label_length)} | {'[yellow]' + '█' * bar_length + '[/]'} {value:,.0f} VNĐ\n"

    # Hiển thị biểu đồ cột
    console.print(Panel(bar_chart, title="Biểu đồ cột chi tiêu", title_align="left"))

    # Hiển thị chi tiết cho từng tuần
    for week_label in week_labels:
        console.print(f"\nChi tiết cho {week_label}:")
        week_expenses = weekly_expenses[week_label.strip("[/bold red]")]
        if week_expenses:
            print(format_expenses_table(week_expenses))
        else:
            print("Không có chi tiêu nào trong tuần này.")

    # Thêm ghi chú dưới biểu đồ tổng hợp
    note = "Ghi chú: Biểu đồ và bảng chi tiết cho chi tiêu mỗi tuần trong 4 tuần gần đây."
    console.print(f"\n[note] {note}")
