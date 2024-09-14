FROM python:3.12

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép file Python chính vào container
ADD main.py .

# Sao chép toàn bộ thư mục json vào container
COPY . /app

# Cài đặt các phụ thuộc
RUN pip install -r requirements.txt

# Chạy ứng dụng Python
CMD ["python", "main.py"]
