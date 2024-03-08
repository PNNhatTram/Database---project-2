import pandas as pd
from faker import Faker
from collections import defaultdict
from sqlalchemy import create_engine
import time
import random

fake = Faker()

#nhập số lượng hàng cần phát sinh dữ liệu cho mỗi bảng
ntr= int(input("Enter rows of TRUONG: "))
nhs= int(input("Enter rows of HS: "))
#hàm xét học lực
def kt_dtb(dtb):
    if dtb<5:
        return "Yếu"
    elif dtb>=5 and dtb<7:
        return "Trung bình"
    elif dtb>=7 and dtb<8:
        return "Khá"
    elif dtb>=8 and dtb<9:
        return "Giỏi"
    else:
        return "Xuất sắc"
#hàm xét kết quả
def kt_kq(dtb):
    if dtb>5:
        return "Hoàn thành"
    else:
        return "Chưa hoàn thành"

#dữ liệu lưu vào các dictionary
fake_data_tr = defaultdict(list)
fake_data_hs = defaultdict(list)
fake_data_hoc = defaultdict(list)
#bắt đầu tính thời gian
start_time = time.time()
#phát sinh dữ liệu cho bảng TRUONG
for _ in range(ntr):
    fake_data_tr["MATR"].append("TR" + str(fake.unique.random_int(min=1000, max=9999)))
    fake_data_tr["TENTR"].append( fake.company())
    fake_data_tr["DCHITR"].append( fake.address())

df_fake_data_tr = pd.DataFrame(fake_data_tr)
#phát sinh dữ liệu cho bảng HS
for _ in range(nhs):
    id = "HS" + str(fake.unique.random_int(min=1000000, max=9999999))
    fake_data_hs["MAHS"].append(id)
    fake_data_hs["HO"].append(fake.last_name())
    fake_data_hs["TEN"].append(fake.first_name()) 
    fake_data_hs["CCCD"].append(fake.unique.ean(length=13))
    fake_data_hs["NTNS"].append(fake.date_of_birth(minimum_age=18, maximum_age=25)) 
    fake_data_hs["DIACHI_HS"].append(fake.address())

df_fake_data_hs = pd.DataFrame(fake_data_hs)
#phát sinh dữ liệu cho bảng hoc
ma_hoc_sinh = df_fake_data_hs["MAHS"].unique()

for mahs in ma_hoc_sinh:
    # Tạo số lượng hàng ngẫu nhiên từ 1 đến 3 cho mỗi hs
    num_rows = random.randint(1, 3)
    # chọn ngẫu nhiên 1 trường cho hs
    matr = random.choice(df_fake_data_tr["MATR"])

    for i in range(num_rows):
        # Tạo dữ liệu cho mỗi hàng
        diemtb = round(random.uniform(0, 10), 2)
        xeploai = kt_dtb(diemtb)
        kq = kt_kq(diemtb)
        nam = random.randint(2020,2023)

        fake_data_hoc["MAHS"].append(mahs)
        fake_data_hoc["MATR"].append(matr)
        fake_data_hoc["NAMHOC"].append(nam)
        fake_data_hoc["DIEMTB"].append(diemtb)
        fake_data_hoc["XEPLOAI"].append(xeploai) 
        fake_data_hoc["KQUA"].append(kq)

df_fake_data_hoc = pd.DataFrame(fake_data_hoc)

# Xoá các dòng trùng lặp về 3 cột MAHS, MATR và NAMHOC
df_fake_data_hoc.drop_duplicates(subset=['MAHS', 'MATR', 'NAMHOC'], inplace=True)
#tạo engine kết nôi CSDL mysql
engine = create_engine('mysql://root:nhattram78204@localhost/truonghoc2', echo=False)
#bắt đầu nạp dữ liệu vào các bảng
with engine.connect() as conn, conn.begin():
    df_fake_data_tr.to_sql('truong', con=conn, index=False, if_exists='append')
    
with engine.connect() as conn, conn.begin():
    df_fake_data_hs.to_sql('hs', con=conn, index=False, if_exists='append')

with engine.connect() as conn, conn.begin():
    df_fake_data_hoc.to_sql('hoc', con=conn, index=False, if_exists='replace')
#thời gian kết thúc
end_time = time.time()
elapsed_time = end_time - start_time

print("tgian chay: ", elapsed_time, "giay")


