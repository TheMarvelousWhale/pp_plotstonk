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
    
    
"""
     ticker       max       min       avg
8      ABBV  0.457204 -0.001305  0.295163
25      PDD  0.504827 -0.030808  0.305457
5   NESN.SW  0.492056  0.048140  0.318867
27     NTES  0.682553  0.077710  0.332506
9       JNJ  0.594450 -0.419060  0.335345
12      GSK  0.567537  0.075791  0.354327
26     BILI  0.591929  0.178301  0.376030
6      NOVN  0.666179 -0.177601  0.390163
24     BABA  0.569934  0.051294  0.390986
7       PFE  0.617731  0.072842  0.411487
11      PFE  0.617731  0.072842  0.411487
28     BIDU  0.594047  0.180347  0.435728
2       MCD  0.681275 -0.489228  0.487281
1       PEP  0.661369 -0.041825  0.492192
23     NFLX  0.740575  0.186908  0.503589
10      SAN  0.658762  0.127774  0.550221
0        KO  0.868173  0.381710  0.557480
30     TWLO  0.918312  0.331136  0.562764
14      IBM  0.782962  0.384455  0.565176
22     META  0.911985  0.366392  0.582108
32     DDOG  0.861673  0.427033  0.590676
19     TSLA  0.763247  0.260076  0.605596
13      TSM  0.810841  0.250368  0.610271
31     COUR  0.846973  0.387672  0.610279
29      SLX  0.746945  0.401247  0.621428
4       YUM  0.826093  0.307227  0.654154
3      SBUX  0.907856  0.421144  0.664827
16     QCOM  0.870600  0.613780  0.751913
17      AMD  0.808194  0.642467  0.754066
21    GOOGL  0.866109  0.674408  0.781825
15     NVDA  0.911924  0.697891  0.816775
20     MSFT  0.931151  0.711071  0.833797
18     AAPL  0.925818  0.758835  0.845154
"""