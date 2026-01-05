from bs4 import BeautifulSoup
import lxml

with open ('dict.xml', 'r') as file:
    data = file.read()

Bs_data =BeautifulSoup(data, "xml")

b_unique = Bs_data.find_all('unique')

print(b_unique)

b_name = Bs_data.find_all('child', {'name':'Frank'})

print(b_name)

value = b_name.get('test')

print(value)