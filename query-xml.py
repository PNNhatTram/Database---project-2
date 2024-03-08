
import io
import lxml.etree as ET

#nhập tên file
file_in = input("Enter file: ")
link_file = r"C:\Users\Admin\Desktop\Study\Cơ sở DL\doan\XML\\" + file_in

# Đọc file xml
tree = ET.parse(link_file)
root = tree.getroot()

# Ngưỡng điểm thấp và cao
low_threshold = input("Enter low threshold: ")
high_threshold = input("Enter high threshold: ")

# Sử dụng XPath để lấy danh sách học sinh có điểm trung bình nằm trong ngưỡng điểm
students = root.xpath(f"student[average_score >= {low_threshold} and average_score <= {high_threshold}]")

# In ra danh sách học sinh vào file txt
filename = file_in.replace('xml', 'txt')
with io.open(filename, mode='w', encoding='utf-8') as f:
    for student in students:
        f.write(f"{student.find('name').text}: {student.find('average_score').text}\n")
