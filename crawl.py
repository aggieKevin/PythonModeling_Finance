
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import quandl
from urllib.request import urlopen
from io import StringIO

# Importing list of companies in S&P 500
companylist = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text
soup = BeautifulSoup(companylist, 'lxml') #Parses out the html
#looks for the first table, the SP500 table
tableofcompanpanies = soup.find_all('table')[0] 
#converts the data into a dataframe in pandas
companydataframe = pd.read_html(str(tableofcompanpanies), header = 0)[0] 

#Identifying the columns
companydataframe = companydataframe[['Symbol', 'Security', 'CIK']]

maindictionarylist = {}
year = '2015'
doc = '10-K'
headersfor_csv = ['Company', 'Ticker', 'anticipate', 'believe', 'depend', 'fluctuate', 'indefinite', 'likelihood',
                  'possible', 'predict', 'risk', 'uncertain',
                  '2014 Closing Price', '2015 Closing Price', '2015 Return']
# csv_loopwriter = csv.DictWriter()
csv_file = open('Master CSV Quiz 6.csv', 'w', newline='')
csv_regwriter = csv.writer(csv_file)

dictionarycsv = open("Dictionary CSV.csv", "w", newline="")
csv_loopwriter = csv.DictWriter(dictionarycsv, fieldnames=headersfor_csv)
        # csv_loopwriter.writeheader()

countstart = 0
countstop = 4

# cnt + 1
for i, row in enumerate(companydataframe.values):
    print('i is :',i)
    csv_regwriter.writerow(row)
    #Code found from Youtube to import add ons and open master index

with open('Master CSV Quiz 6.csv', "r") as csv_file, open("Dictionary CSV.csv", "w", newline="") as dictionarycsv: 
    csv_reader = csv.reader(csv_file)
    csv_loopwriter = csv.DictWriter(dictionarycsv, fieldnames=headersfor_csv)
    csv_loopwriter.writeheader()
    # next(csv_reader)        #Potentially in master index?

    # dictionarycsv = open("Dictionary CSV.csv", "w", newline="")
    # csv_loopwriter = csv.DictWriter(csv_file, fieldnames=headersfor_csv)
    # csv_loopwriter.writeheader()

    # Everything must be within this for loop to run the analysis on each 10-K
    count=0
    for line in csv_reader:
        count+=1
        print('count is,',count)
        if count==10:
            break
        company = line[1]
        cik = line[2]
        ticker = line[0]
        doc = '10-K'
        maindictionarylist.update({"Company": company})
        maindictionarylist.update({"Ticker": ticker})
        # Defining variables (a portion of this was imported from the youtube video)
        source_10K = 'https://www.sec.gov/Archives/'
        url = "https://www.sec.gov/Archives/edgar/full-index/" + year + "/QTR1/master.idx"
        data = urlopen(url).read().decode('ascii', 'ignore')
        datafile = StringIO(data)# reads and writes a string buffer
        masterindex = csv.reader(datafile, delimiter="|")
        for line in masterindex:
            if cik in line and doc in line: #printing lines with both the correct cik and document type

                finalurl = source_10K + line[-1] #consolidating urls to get a specific 10-K

        read10K = requests.get(finalurl).text
        uncertainwords = ['anticipate', 'believe', 'depend', 'fluctuate', 'indefinite', 'likelihood',
                              'possible', 'predict', 'risk', 'uncertain']
        # print("These are the number of uncertain words for " + company + " in " + year + "")
        for word in uncertainwords: #looping to populate the dictionary list
            maindictionarylist.update({word:str(read10K).count(word)})
        quandl.ApiConfig.api_key = "-52sce7LBiQX5w1gK6c1"
        try:
            endingdate = '2014-12-31'
            data2014 = quandl.get_table('WIKI/PRICES', qopts={'columns': ['ticker', 'date', 'adj_close']},
                                    ticker=[ticker],
                                    date=[endingdate], paginate=True)

            maindictionarylist.update({"2014 Closing Price": data2014['adj_close'][0]})

            endingdate = '2015-12-31'
            data2015 = quandl.get_table('WIKI/PRICES', qopts={'columns': ['ticker', 'date', 'adj_close']},
                                        ticker=[ticker],
                                        date=[endingdate], paginate=True)
            maindictionarylist.update({"2015 Closing Price": data2015['adj_close'][0]})

            overallreturn = float((data2015['adj_close'] - data2014['adj_close']) / data2014['adj_close'])

            maindictionarylist.update({'2015 Return': overallreturn})
            print('maindict here, ',maindictionarylist)
            csv_loopwriter.writerow(maindictionarylist)
        except:
            continue
            print('in except')


