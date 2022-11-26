from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtGui import QMovie, QFont
from app_stock_anyalizer_util import logger 
import app_stock_anyalizer_const as const 
import app_stock_anyalizer_css as css 

AnyaCSS = css.AnyaStyle()
CSSAlterableTypes = [const.WIDGET_TYPE_LABEL,
                     const.WIDGET_TYPE_INPUT_BOX,
                     const.WIDGET_TYPE_DROPDOWN,
                     const.WIDGET_TYPE_PUSHBTN
                     ]


class WidgetController():
    def __init__(self):
        self.widgets = {}
        self.widget_factory = WidgetFactory()
    
    def Add(self,name:str,type:str,args:dict)->QWidget:
        widget = self.widget_factory.Create(type,args)
        if widget == None:
            logger.error(f"failed to create widget {name}")
            return None 
        if name in self.widgets:
            logger.warn(f"widget {name} already exists")
        if type in CSSAlterableTypes:
            widget.setFont(AnyaCSS.GetDefaultFont())
        self.widgets[name] = widget
        return widget

    def GetWidget(self,name:str):
        if name in self.widgets:
            return self.widgets[name]
        return None 

class WidgetFactory():
    def Create(self,type:str,args:dict) ->QWidget:
        try: 
            if type == const.WIDGET_TYPE_LABEL:
                return self._create_label(args)
            elif type == const.WIDGET_TYPE_INPUT_BOX:
                return self._create_input_box(args)
            elif type == const.WIDGET_TYPE_DROPDOWN:
                return self._create_dropdown(args)
            elif type == const.WIDGET_TYPE_GIF:
                return self._create_gif(args)
            elif type == const.WIDGET_TYPE_WIDGET:
                return self._create_widget(args)
            elif type == const.WIDGET_TYPE_MPL_GRAPH:
                return self._create_mpl_graph(args)
            elif type == const.WIDGET_TYPE_PUSHBTN:
                return self._create_push_button(args)
        except:
            return None 
        
    
    def _create_label(self,args:dict)->QWidget:
        labelName = args[const.WIDGET_ARG_LABEL_NAME] or const.DEFAULT_STRING 
        label = QLabel(labelName)
        return label
    
    def _create_input_box(self,args:dict) ->QWidget:
        le = QLineEdit()
        placholder = args[const.WIDGET_ARG_PLACEHOLDER_NAME] or const.DEFAULT_STRING 
        le.setPlaceholderText(placholder)
        return le
    
    def _create_dropdown(self,args:dict) ->QWidget:
        dd = QComboBox()
        items = args[const.WIDGET_ARG_DROPDOWN_ITEMS] or [const.DEFAULT_STRING]
        dd.addItems(items)
        return dd
    
    def _create_gif(self,args:dict) ->QWidget:
        gif = QLabel() 
        try: 
            filepath = args[const.WIDGET_ARG_FILEPATH]
            gif.movie = QMovie(filepath) 
            gif.setMovie(gif.movie) 
            gif.movie.start()
        except Exception as e:
            logger.error("unable to find gif, err={e}")
        finally:
            return gif 
        
        
    def _create_widget(self,args:dict) ->QWidget:
        widget = QWidget()
        layout = args[const.LAYOUT_OBJ] or QVBoxLayout()
        childWidgets = args[const.CHILD_WIDGETS] or []
        try: 
            col_ratios = args[const.CHILD_WIDGETS_COLUMN_RATIO]
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
            return widget
            
    def _create_mpl_graph(self,args:dict) -> QWidget:
        parent = args[const.MPL_PARENT_OBJ]
        sc = MplGraph( width=args[const.MPL_GRAPH_WIDTH], 
                       height=args[const.MPL_GRAPH_HEIGHT], 
                       dpi=args[const.MPL_GRAPH_DPI])
        sc.axes.plot(args[const.MPL_DATA])
        toolbar = NavigationToolbar(sc, parent)
        graph = self._create_widget(
            {
                const.LAYOUT_OBJ:QVBoxLayout(),
                const.CHILD_WIDGETS:[toolbar,sc]
            }
        )
        graph.canvas = sc 
        graph.toolbar = toolbar
        return graph
        
    def _create_push_button(self,args:dict) ->QWidget:
        pbtn = QPushButton(args[const.PUSHBTN_TEXT])
        pbtn.clicked.connect(args[const.FUNC])
        return pbtn 
    

class MplGraph(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        self.axes = fig.add_subplot(111)
        super().__init__(fig) 



