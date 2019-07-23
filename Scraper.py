from bs4 import BeautifulSoup
import requests
import csv
import os
import time

start = time.clock()

os.chdir('csvFiles')

URL = 'https://karki23.github.io/Weather-Data/'

source = requests.get(URL+'assignment.html').text

soup = BeautifulSoup(source, 'lxml')

cities = dict()

# ! Saving city names and urls
for city in soup.find_all('a'):
    name_of_city = city['href'].split('.')[0]
    cities[name_of_city] = URL+city['href']


for name in cities:
    # ! Creating the csv file name and saving the url
    file_name = name+'.csv'
    url = cities[name]
    # file_name = city['href'].split('.')[0] + '.csv'
    # url = URL+city['href']
    
    # * Just checking
    print(file_name, url)
    
    # ! Getting the data from the specified URL
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    
    # ! Getting the contents of the table
    table = soup.find('table')
    rows = table.find_all('tr')
    # print(rows)

    # for row in rows:
    #     print(row.text)

    # ! Writing into csv file
    with open(file_name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in rows:
            csv_row = []

            # ! Slow
            # for cell in row.find_all(['td', 'th']):
            #     csv_row.append(cell.text)
            
            # ! Used list comprehension because it's faster
            csv_row = [cell.text for cell in row.find_all(['td', 'th'])]

            # ! Fastest of the lot
            # map(lambda cell: csv_row.append(cell.text), row.find_all(['td', 'th']))

            csv_writer.writerow(csv_row)

print(time.clock() - start, 'seconds')