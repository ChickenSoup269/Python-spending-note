from savings import *
from expenses import *

# Function to apply savings to current expenses
def apply_savings():
    if not savings:
        print(Fore.RED + "Không có tiền tiết kiệm nào để sử dụng." + Style.RESET_ALL)
        return

    date = input("Nhập ngày của khoản tiết kiệm cần sử dụng (YYYY-MM-DD): ")
    if date not in savings:
        print(Fore.RED + "Ngày tiết kiệm không hợp lệ." + Style.RESET_ALL)
        return
    
    amount = int(input("Nhập số tiền cần sử dụng (VNĐ): "))
    if amount > savings[date]["amount"]:
        print(Fore.RED + "Số tiền yêu cầu vượt quá số tiền tiết kiệm hiện có." + Style.RESET_ALL)
        return
    
    # Deduct savings and add to expenses
    # Trước khi thực hiện điều này, gọi hàm add_expense_from_savings
 
    add_expense_from_savings(amount, "Chi tiêu từ tiết kiệm")


# Function to add an expense directly from savings
def get_savings_balance():
    today = datetime.now().strftime('%Y-%m-%d')
    return savings.get(today, {"amount": 0})["amount"]

def update_savings_balance(amount_spent):
    today = datetime.now().strftime('%Y-%m-%d')
    if today in savings:
        savings[today]["amount"] -= amount_spent
        if savings[today]["amount"] <= 0:
            del savings[today]  # Xóa ngày nếu số dư không còn
    else:
        print(Fore.RED + "Không có số dư tiết kiệm cho ngày hôm nay!" + Style.RESET_ALL)

def add_expense_from_savings(amount, category):
    savings_balance = get_savings_balance()
    
    if amount > savings_balance:
        print(Fore.RED + "Số tiền chi tiêu vượt quá số dư tiết kiệm hiện có!" + Style.RESET_ALL)
        return
    
    # Thực hiện chi tiêu từ tiết kiệm
    # Giảm số dư tiết kiệm trước khi thêm chi tiêu
    update_savings_balance(amount)

    # Tiến hành thêm chi tiêu
    while True:
        add_expense(amount, category)
        
        # Hỏi người dùng có muốn xác nhận chi tiêu không
        confirm_question = [
            inquirer.Confirm('confirm', message="Bạn có muốn xác nhận chi tiêu này không?", default=True)
        ]
        confirm_answer = inquirer.prompt(confirm_question)

        if confirm_answer['confirm']:
            print(Fore.GREEN + f"Chi tiêu được xác nhận. Đã trừ {amount:,} VNĐ từ số dư tiết kiệm." + Style.RESET_ALL)
            break
        else:
            # Nếu không xác nhận, khôi phục số dư tiết kiệm
            print(Fore.YELLOW + "Chi tiêu đã bị hủy. Không trừ số tiền từ số dư tiết kiệm." + Style.RESET_ALL)
            # Hoàn lại số tiền vào số dư tiết kiệm
            add_savings(amount)
            break
