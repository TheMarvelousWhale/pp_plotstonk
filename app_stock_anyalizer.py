"""
The stock - anyalizer should have the following features:
- input a ticker name, choosing period (dropdown) and interval (drop down)
- display the stock price Open High Low Close 
- have anya gif
- have tabular analysis of other important stats:
    * avg return 
    * avg sd
    * corr with SPY 500 
    * PE ratio
    in tabular form 
"""
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow
)
from PyQt5.QtGui import QMovie

import yfinance as yf
import yaml
import app_stock_anyalizer_const as const
import app_stock_anyalizer_util as util
import app_stock_anyalizer_widgets as anya_widgets
from get_corrs import *

defaultData = yf.Ticker("SPY").history(period="1y")[["High","Low","Open","Close"]]
defaultMean, defaultSD = get_mean_sd(defaultData)
defaultCorr = GetAvgCorrWithSPY("SPY")

with open(const.YML_FILE) as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)   



class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Stock Anya-lyzer")
        
        self.widgetCtrl = anya_widgets.WidgetController()
        wc = self.widgetCtrl

        sideCol = wc.Add("side_col",const.WIDGET_TYPE_WIDGET,{
            const.LAYOUT_OBJ:QVBoxLayout(),
            const.CHILD_WIDGETS:[
                wc.Add("anya_gif",const.WIDGET_TYPE_GIF,{
                    const.WIDGET_ARG_FILEPATH:"media/anya.gif"
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
                    wc.Add("graph",const.WIDGET_TYPE_MPL_GRAPH,{
                            const.LAYOUT_OBJ:QVBoxLayout(),
                            const.MPL_PARENT_OBJ: self,
                            const.MPL_DATA:defaultData,
                            const.MPL_GRAPH_WIDTH: conf[const.MPL_GRAPH_WIDTH],
                            const.MPL_GRAPH_HEIGHT: conf[const.MPL_GRAPH_HEIGHT],
                            const.MPL_GRAPH_DPI:conf[const.MPL_GRAPH_DPI]
                        }),
                    wc.Add("stats_row",const.WIDGET_TYPE_WIDGET,{
                            const.LAYOUT_OBJ:QHBoxLayout(),
                            const.CHILD_WIDGETS:[
                               wc.Add("mean",const.WIDGET_TYPE_LABEL, {
                                        const.WIDGET_ARG_LABEL_NAME:const.STATS_MEAN_TMPL.substitute(mean=defaultMean)
                                    }),
                               wc.Add("sd",const.WIDGET_TYPE_LABEL,{
                                        const.WIDGET_ARG_LABEL_NAME:const.STATS_SD_TMPL.substitute(sd=defaultSD)
                                    }),
                               wc.Add("corr",const.WIDGET_TYPE_LABEL,{
                                        const.WIDGET_ARG_LABEL_NAME:const.STAT_CORR_TMPL.substitute(corr=defaultCorr)
                                    })
                            ]
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
        graph =  wc.GetWidget("graph")
        newTicker,newData = self.get_latest_data()
        mean,sd = get_mean_sd(newData)
        corr = GetAvgCorrWithSPY(newTicker)
        graph.canvas.axes.cla()
        graph.canvas.axes.plot(newData)
        graph.canvas.draw()
        wc.GetWidget("mean").setText(const.STATS_MEAN_TMPL.substitute(mean=mean))
        wc.GetWidget("sd").setText(const.STATS_SD_TMPL.substitute(sd=sd))
        wc.GetWidget("corr").setText(const.STAT_CORR_TMPL.substitute(corr=corr))

    def get_latest_data(self):
        wc = self.widgetCtrl
        ticker = str(wc.GetWidget("input_ticker").text()) or const.DEFAULT_TICKER 
        period = str(wc.GetWidget("dropdown_period").currentText()) or const.DEFAULT_PERIOD.text()
        interval = str(wc.GetWidget("dropdown_interval").currentText()) or const.DEFAULT_INTERVAL
        newData = yf.Ticker(ticker).history(period=period,interval=interval)[["High","Low","Open","Close"]]
        if len(newData) == 0:
            self.handle_error()
            return ticker,defaultData
        self.clear_error()
        util.logger.info(f"get new data, ticker:{ticker},period:{period},interval:{interval}, shape: {newData.shape}")
        return ticker,newData

    def handle_error(self):
        self._set_anya_gif("media/anya_scared.gif")
    def clear_error(self):
        self._set_anya_gif("media/anya.gif")
        
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
    w = MainWindow()
    w.resize(conf["window_width"],conf["window_height"])
    app.exec_()
    
    

