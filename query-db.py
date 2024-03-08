import mysql.connector
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import time

#nhập thông tin cần thiết
db_name = input("Enter db: ")
truong_name = input("Enter school: ")
nam = str(input("Enter year: "))
hoc_luc = input("Enter grade: ")
#liên kết đến CSDL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nhattram78204",
    database=db_name
)

mycursor = mydb.cursor()

#thực thi truy vấn
sql_query = "SELECT hs.ho, hs.ten, hs.ntns, hoc.diemtb, hoc.xeploai, hoc.kqua \
            FROM hs \
            INNER JOIN hoc ON hs.mahs = hoc.mahs \
            INNER JOIN truong ON truong.matr = hoc.matr \
            WHERE truong.tentr = %s AND hoc.namhoc = %s AND hoc.xeploai = %s"

start_time = time.time()

mycursor.execute(sql_query, (truong_name, nam, hoc_luc))

myresult = mycursor.fetchall()

end_time = time.time()
elapsed_time = end_time - start_time

# Tạo một thẻ gốc <root> để chứa tất cả các phần tử
root = ET.Element("root")

for row in myresult:
    # Tạo một thẻ con <student> cho mỗi hàng và thêm nó vào thẻ gốc
    student = ET.SubElement(root, "student")

    # Thêm các phần tử con <name>, <birthdate>, <average_score>, <grade>, và <result> vào thẻ <student>
    ET.SubElement(student, "name").text = f"{row[0]} {row[1]}"
    ET.SubElement(student, "birthdate").text = str(row[2])
    ET.SubElement(student, "average_score").text = str(row[3])
    ET.SubElement(student, "grade").text = str(row[4])
    ET.SubElement(student, "result").text = row[5]

# Tạo cây XML với thẻ xử lý khai báo mã ký tự là utf-8
declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
tree = ET.ElementTree(root)
xml_str = declaration + ET.tostring(root, encoding='unicode')

# Parse chuỗi XML và chỉnh sửa định dạng
dom = minidom.parseString(xml_str)
pretty_xml_str = dom.toprettyxml(indent="\t", encoding='utf-8')

# Lưu chuỗi XML vào file trong thư mục xml_folder
if not os.path.exists('XML'):
    os.makedirs('XML')
filename = f"XML/{db_name}-{truong_name.replace(' ', '')}-{nam}-{hoc_luc}.xml"
with open(filename, 'wb') as f:
    f.write(pretty_xml_str)

print("Exported to XML file:", filename)
print("tgian chay: ", elapsed_time, "giay")