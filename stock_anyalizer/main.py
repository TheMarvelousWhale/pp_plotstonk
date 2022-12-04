"""
The stock - anyalizer should have the following features:
- input a ticker name, choosing period (dropdown) and interval (drop down)
- display the stock price Open High Low Close 
- have anya gif
- have tabular analysis of other important stats:
    * avg return 
    * avg sd
    * corr with SPY 500 
    * PE ratio (nope)
    in tabular form 
"""
import sys,os
sys.path.append(os.getcwd())
os.chdir(os.path.join(os.getcwd(),"stock_anyalizer"))

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow
)
from PyQt5.QtGui import QMovie, QIcon
from qt_material import apply_stylesheet 
import yfinance as yf
import yaml
import  const, util, widgets
from get_corrs import *

defaultTicker = "SPY"
defaultData = yf.Ticker(defaultTicker).history(period="1y")[const.PRICE_LIST]
defaultMean, defaultSD = get_mean_sd(defaultData)
defaultCorr = getAvgCorrWithSPY(defaultTicker)

with open(const.YML_FILE) as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)   


class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Stock Anya-lyzer")
        self._ticker = defaultTicker
        self.widgetCtrl = widgets.WidgetController()
        wc = self.widgetCtrl

        sideCol = wc.Add("side_col",const.WIDGET_TYPE_WIDGET,{
            const.LAYOUT_OBJ:QVBoxLayout(),
            const.CHILD_WIDGETS:[
                wc.Add("anya_gif",const.WIDGET_TYPE_GIF,{
                    const.WIDGET_ARG_FILEPATH:"../media/anya.gif"
                    }),
                wc.Add("alert_msg",const.WIDGET_TYPE_LABEL,{
                    const.WIDGET_ARG_LABEL_NAME: const.ALERT_NORMAL_TMPL.substitute(ticker=self._ticker)
                    }),
                wc.Add("label_ticker",const.WIDGET_TYPE_LABEL,{
                    const.WIDGET_ARG_LABEL_NAME:"Ticker"
                    }),
                wc.Add("input_ticker",const.WIDGET_TYPE_INPUT_BOX,{
                    const.WIDGET_ARG_PLACEHOLDER_NAME:"SPY"
                    }),
                wc.Add("label_period",const.WIDGET_TYPE_LABEL,{
                    const.WIDGET_ARG_LABEL_NAME:"Period"
                    }),
                wc.Add("dropdown_period",const.WIDGET_TYPE_DROPDOWN,{
                    const.WIDGET_ARG_DROPDOWN_ITEMS:const.PERIOD_LIST
                    }),
                wc.Add("label_interval",const.WIDGET_TYPE_LABEL,{
                    const.WIDGET_ARG_LABEL_NAME:"Interval"
                    }),
                wc.Add("dropdown_interval",const.WIDGET_TYPE_DROPDOWN,{
                    const.WIDGET_ARG_DROPDOWN_ITEMS:const.INTERVAL_LIST
                    }),
                wc.Add("refresh_btn",const.WIDGET_TYPE_PUSHBTN,{
                                    const.PUSHBTN_TEXT:"Refresh",
                                    const.FUNC: self.update_graph
                    }),
            ]
        })
        
               
        graphCol = wc.Add("graph_col",const.WIDGET_TYPE_WIDGET,{
                const.LAYOUT_OBJ:QVBoxLayout(),
                const.CHILD_WIDGETS:[
                    # wc.Add("graph",const.WIDGET_TYPE_MPL_GRAPH,{
                    #         const.LAYOUT_OBJ:QVBoxLayout(),
                    #         const.MPL_PARENT_OBJ: self,
                    #         const.PD_DATA:defaultData,
                    #         const.MPL_GRAPH_WIDTH: conf[const.MPL_GRAPH_WIDTH],
                    #         const.MPL_GRAPH_HEIGHT: conf[const.MPL_GRAPH_HEIGHT],
                    #         const.MPL_GRAPH_DPI:conf[const.MPL_GRAPH_DPI]
                    #     }),
                    wc.Add("stats_row",const.WIDGET_TYPE_WIDGET,{
                            const.LAYOUT_OBJ:QHBoxLayout(),
                            const.CHILD_WIDGETS:[
                               wc.Add("mean",const.WIDGET_TYPE_LABEL, {
                                        const.WIDGET_ARG_LABEL_NAME:const.STATS_MEAN_TMPL.substitute(mean=util.wrap3F(defaultMean))
                                    }),
                               wc.Add("sd",const.WIDGET_TYPE_LABEL,{
                                        const.WIDGET_ARG_LABEL_NAME:const.STATS_SD_TMPL.substitute(sd=util.wrap3F(defaultSD))
                                    }),
                               wc.Add("corr",const.WIDGET_TYPE_LABEL,{
                                        const.WIDGET_ARG_LABEL_NAME:const.STAT_CORR_TMPL.substitute(corr=util.wrap3F(defaultCorr))
                                    })
                            ]
                        }), 
                    wc.Add("qtgraph",const.WIDGET_TYPE_QTGRAPH, {
                        const.PD_DATA:defaultData
                    })
                    ]
                }
            )
        
        mainWidget = wc.Add("main",const.WIDGET_TYPE_WIDGET,{
                const.LAYOUT_OBJ:QHBoxLayout(),
                const.CHILD_WIDGETS: [sideCol,graphCol],
                const.CHILD_WIDGETS_COLUMN_RATIO:[3,7]
            }
        )

        self.widget = mainWidget
        self.setCentralWidget(mainWidget)
        self.show()
        
     
    def update_graph(self):

        # Trigger the canvas to update and redraw.
        wc = self.widgetCtrl
        graph =  wc.GetWidget("qtgraph")
        newTicker,newData = self.get_latest_data()

        mean,sd = get_mean_sd(newData)
        corr = getAvgCorrWithSPY(newTicker)
        # graph.canvas.axes.cla()
        # graph.canvas.axes.plot(newData)
        # graph.canvas.draw()
        xAxis = util.getUnix(newData.index)
        for priceType in const.PRICE_LIST:
            attr = getattr(graph,priceType)
            attr.setData(xAxis,newData[priceType])
        wc.GetWidget("mean").setText(const.STATS_MEAN_TMPL.substitute(mean=util.wrap3F(mean)))
        wc.GetWidget("sd").setText(const.STATS_SD_TMPL.substitute(sd=util.wrap3F(sd)))
        wc.GetWidget("corr").setText(const.STAT_CORR_TMPL.substitute(corr=util.wrap3F(corr)))
            
            
            
    def get_latest_data(self):
        wc = self.widgetCtrl
        ticker = str(wc.GetWidget("input_ticker").text()) or const.DEFAULT_TICKER 
        self._ticker = ticker
        period = str(wc.GetWidget("dropdown_period").currentText()) or const.DEFAULT_PERIOD.text()
        interval = str(wc.GetWidget("dropdown_interval").currentText()) or const.DEFAULT_INTERVAL
        newData = yf.Ticker(ticker).history(period=period,interval=interval)[const.PRICE_LIST]
        if len(newData) == 0:
            self.handle_error()
            return ticker,defaultData
        util.logger.info(f"get new data, ticker:{ticker},period:{period},interval:{interval}, shape: {newData.shape}")
        self.clear_error() 
        return ticker,newData

    def handle_error(self):
        self._set_anya_gif("../media/anya_scared.gif")
        self.widgetCtrl.GetWidget("alert_msg").setText(const.ALERT_ERROR_TMPL.substitute(ticker=self._ticker))
        
    def clear_error(self):
        self._set_anya_gif("../media/anya.gif")
        self.widgetCtrl.GetWidget("alert_msg").setText(const.ALERT_NORMAL_TMPL.substitute(ticker=self._ticker))
        
    def _set_anya_gif(self,path:str):
        wc = self.widgetCtrl
        movie = QMovie(path)
        gif = wc.GetWidget("anya_gif")
        gif.clear()
        gif.setMovie(movie)
        gif.movie = movie
        movie.start()
    
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_amber.xml",extra={'font_size':20})
    w = MainWindow()
    w.resize(conf["window_width"],conf["window_height"])
    w.setWindowIcon(QIcon("../media/anya_icon.jpg"))
    app.exec_()
    
    

