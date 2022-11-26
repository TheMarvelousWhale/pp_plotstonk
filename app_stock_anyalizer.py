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
    QWidget,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QMainWindow
)

from PyQt5.QtGui import QMovie

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import yfinance as yf, pandas as pd
import yaml
import app_stock_anyalizer_const as const

defaultData = yf.Ticker("SPY").history(period="1y")[["High","Low","Open","Close"]]
with open(const.YML_FILE) as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)   

widgetController = {}
            
def AddWidget(**kwargs)->QWidget:
    widgetId=kwargs["id"]
    widgetArgs = kwargs["args"]
    widgetType = kwargs["type"]
    
    if widgetType == const.WIDGET_TYPE_LABEL:
        widget =  QLabel(widgetArgs[const.WIDGET_ARG_LABEL_NAME])
    elif widgetType == const.WIDGET_TYPE_INPUT_BOX:
        widget = QLineEdit()
        widget.setPlaceholderText(widgetArgs[const.WIDGET_ARG_PLACEHOLDER_NAME])
    elif widgetType == const.WIDGET_TYPE_DROPDOWN:
        widget = QComboBox()
        widget.addItems(widgetArgs[const.WIDGET_ARG_DROPDOWN_ITEMS])
    elif widgetType == const.WIDGET_TYPE_GIF:
        widget = QLabel() 
        movie = QMovie(widgetArgs[const.WIDGET_ARG_FILEPATH]) 
        widget.setMovie(movie) 
        movie.start()
    elif widgetType == const.WIDGET_TYPE_WIDGET:
        widget = QWidget()
        layout = widgetArgs[const.LAYOUT_OBJ]

        childWidgets = widgetArgs[const.CHILD_WIDGETS]
        try: 
            col_ratios = widgetArgs[const.CHILD_WIDGETS_COLUMN_RATIO]
            canAddRatio = True 
            if col_ratios == None or len(col_ratios) != len(childWidgets):
                canAddRatio = False
        except:
            canAddRatio = False
        finally:
            for i, childWidget in enumerate(childWidgets):
                if canAddRatio:
                    ratio = int(col_ratios[i])
                    layout.addWidget(childWidget,ratio)
                else:
                    layout.addWidget(childWidget)
            widget.setLayout(layout)
    elif widgetType == const.WIDGET_TYPE_MPL:
        parent = widgetArgs[const.MPL_PARENT_OBJ]
        sc = MplCanvas(parent, 
                       width=widgetArgs[const.MPL_GRAPH_WIDTH], 
                       height=widgetArgs[const.MPL_GRAPH_HEIGHT], 
                       dpi=widgetArgs[const.MPL_GRAPH_DPI])
        sc.axes.plot(widgetArgs[const.MPL_DATA])
        toolbar = NavigationToolbar(sc, parent)
        widget = AddWidget(
            id=widgetId,
            type=const.WIDGET_TYPE_WIDGET,
            args= {
                const.LAYOUT_OBJ:QVBoxLayout(),
                const.CHILD_WIDGETS:[toolbar,sc]
            }
        )
        widget.canvas = sc 
        widget.toolbar = toolbar
        
    elif widgetType == const.WIDGET_TYPE_PUSHBTN:
        widget = QPushButton(widgetArgs[const.PUSHBTN_TEXT])
        widget.clicked.connect(widgetArgs[const.FUNC])
    
    if widgetId != "" and widgetId not in widgetController:
        widgetController[widgetId] = widget 
    
    return widget
        
        
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Anya-lyzer")
        
        sideCol =  AddWidget(
            id="side_col",
            type=const.WIDGET_TYPE_WIDGET,
            args={
                const.CHILD_WIDGETS: [               
                    AddWidget(
                        id="anya_gif",
                        type=const.WIDGET_TYPE_GIF,
                        args={const.WIDGET_ARG_FILEPATH:"media/anya.gif"}
                    ),
                    AddWidget(
                        id="label_ticker",
                        type=const.WIDGET_TYPE_LABEL,
                        args={const.WIDGET_ARG_LABEL_NAME:"Ticker"}
                    ),
                    AddWidget(
                        id="input_ticker",
                        type=const.WIDGET_TYPE_INPUT_BOX,
                        args={const.WIDGET_ARG_PLACEHOLDER_NAME:"SPY"}
                    ),
                    AddWidget(
                        id="label_period",
                        type=const.WIDGET_TYPE_LABEL,
                        args={const.WIDGET_ARG_LABEL_NAME:"Period"}    
                    ),
                    AddWidget(
                        id="dropdown_period",
                        type=const.WIDGET_TYPE_DROPDOWN,
                        args={const.WIDGET_ARG_DROPDOWN_ITEMS:const.PERIOD_LIST}
                    ),
                    AddWidget(
                        id="label_interval",
                        type= const.WIDGET_TYPE_LABEL,
                        args={const.WIDGET_ARG_LABEL_NAME:"Interval"}  
                    ),
                    AddWidget(
                        id="dropdown_interval",
                        type=const.WIDGET_TYPE_DROPDOWN,
                        args={const.WIDGET_ARG_DROPDOWN_ITEMS:const.INTERVAL_LIST}
                    ),
                    AddWidget(
                        id="refresh_btn",
                        type=const.WIDGET_TYPE_PUSHBTN,
                        args={
                            const.PUSHBTN_TEXT:"Refresh",
                            const.FUNC: self.update_graph
                        }
                    ),
                    ],
                const.LAYOUT_OBJ:QVBoxLayout()
            })
               
        graphCol = AddWidget(
            id="graph_col",
            type=const.WIDGET_TYPE_WIDGET,
            args={
                const.LAYOUT_OBJ:QVBoxLayout(),
                const.CHILD_WIDGETS:[
                    AddWidget(
                        id="graph",
                        type=const.WIDGET_TYPE_MPL,
                        args={
                            const.LAYOUT_OBJ:QVBoxLayout(),
                            const.MPL_PARENT_OBJ: self,
                            const.MPL_DATA:defaultData,
                            const.MPL_GRAPH_WIDTH: conf[const.MPL_GRAPH_WIDTH],
                            const.MPL_GRAPH_HEIGHT: conf[const.MPL_GRAPH_HEIGHT],
                            const.MPL_GRAPH_DPI:conf[const.MPL_GRAPH_DPI]
                            }
                        )
                    ]
                }
            )
        
        mainWidget = AddWidget(
            id="main",
            type=const.WIDGET_TYPE_WIDGET,
            args={
                const.LAYOUT_OBJ:QHBoxLayout(),
                const.CHILD_WIDGETS: [
                    sideCol,graphCol
                ],
                const.CHILD_WIDGETS_COLUMN_RATIO:[3,7]
            }
        )

        self.widget = mainWidget
        self.setCentralWidget(mainWidget)
        self.show()

        
    def update_graph(self):
        # Trigger the canvas to update and redraw.
        graph =  widgetController["graph"]
        newData = get_latest_data()
        graph.canvas.axes.cla()
        graph.canvas.axes.plot(newData)
        graph.canvas.draw()

def get_latest_data():
    ticker = str(widgetController["input_ticker"].text())
    if ticker == "":
        ticker = const.DEFAULT_TICKER 
    period = str(widgetController["dropdown_period"].currentText())
    if period == "":
        period = const.DEFAULT_PERIOD.text()
    interval = str(widgetController["dropdown_interval"].currentText())
    if interval == "":
        interval = const.DEFAULT_INTERVAL
    newData = yf.Ticker(ticker).history(period=period,interval=interval)[["High","Low","Open","Close"]]
    if len(newData) == 0:
        newData = defaultData
    return newData


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig) 
        
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(conf["window_width"],conf["window_height"])
    app.exec_()
    
    

