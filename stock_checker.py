import csv

def check_stock(ticker):
    with open('nasdaq_screener_1673447079600.csv', 'r') as csvfile:
        cvsreader = csv.reader(csvfile)

        for row in cvsreader:
            if ticker in row: return True
        
        return False
