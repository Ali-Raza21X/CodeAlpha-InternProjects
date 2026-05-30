# mini db

stocks={
    'AAPL':180,
    'TSLA':280,
    'GOOG':150
}

print('_________STOCK TRACKER________')
print("Available Stocks:", stocks.keys())

name_input=str(input('Enter your stock name:  ')).upper()
value_input=int(input('Enter your amount: '))

# logic

if name_input in stocks:
        
        stocks_price=stocks[name_input]
        total= value_input*stocks_price
        print("\n_____ PORTFOLIO DETAILS _____")
        print("Stock Name:", name_input)
        print("Stock Price:", stocks_price)
        print("Quantity:", value_input)
        print("Total Investment:", total)

else:
        print('stocks not found')
  
        