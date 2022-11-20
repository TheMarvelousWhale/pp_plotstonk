import yfinance as yf
import pandas as pd

def get60rollwindow(ticker,d={}):
    if ticker in d:
        data = d[ticker]
    else:
        data = yf.download(
            tickers=ticker,
            period='1y',
            interval='1d')
        d[ticker] = data
    data["Avg"]=(data["High"]+data["Low"])/2
    mid = data["Avg"].pct_change()
    step =7
    return [mid[i:i+60] for i in range(0,len(mid)-len(mid)%step,step)]

def getCovs(ta,tb):
    a = get60rollwindow(ta)
    b = get60rollwindow(tb)
    n=min(len(a),len(b))
    x = [a[i].corr(b[i]) for i in range(n)] 
    #ts = pd.DatetimeIndex([a[i].index[0] for i in range(n)])
    #pd.Series(x,index=ts).plot()
    if len(x) == 0:
        return 1,1,1
    return max(x),min(x),sum(x)/len(x)

def rankLeastCorrelated(tickers,target="SPY"):
    aggr = []
    for i in tickers :
        aggr.append(getCovs(target,i))
    df = pd.DataFrame(aggr,columns=["max","min","avg"])
    df.insert(loc=0,column="ticker",value=tickers)
    print(df.sort_values(by=["avg","max","min"]))

# add all the stocks you eyeing
# this will find the least correlated with the SP500
if __name__ == "__main__":
    rankLeastCorrelated(["KO","PEP","MCD","SBUX","YUM","NESN.SW",
                         "NOVN","PFE","ABBV","JNJ","SAN", "PFE","GSK",
                         "TSM","IBM", "NVDA","QCOM","AMD",
                         "AAPL","TSLA","MSFT","GOOGL","META","NFLX",
                         "BABA","PDD","BILI","NTES","BIDU",
                         "SLX","TWLO","COUR","DDOG",
                         ])