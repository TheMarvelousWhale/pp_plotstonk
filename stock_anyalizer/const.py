from string import Template 

YML_FILE = "conf.yml"


"""Widget Type & Args"""
WIDGET_TYPE_LABEL = "label"
WIDGET_ARG_LABEL_NAME = "label_name"

WIDGET_TYPE_INPUT_BOX = "input_box"
WIDGET_ARG_PLACEHOLDER_NAME = "placeholder_name"

WIDGET_TYPE_DROPDOWN = "dropdown"
WIDGET_ARG_DROPDOWN_ITEMS = "dropdown_items"

WIDGET_TYPE_GIF = "gif"
WIDGET_ARG_FILEPATH ="filepath"

WIDGET_TYPE_WIDGET = "widget"
LAYOUT_OBJ = "layout_obj"
CHILD_WIDGETS = "child_widgets"
CHILD_WIDGETS_COLUMN_RATIO = "col_ratio"

WIDGET_TYPE_MPL_GRAPH = "mpl"
MPL_PARENT_OBJ = "mpl_parent_obj"
MPL_DATA = "mpl_data"
MPL_GRAPH_WIDTH = "graph_width"
MPL_GRAPH_HEIGHT = "graph_height"
MPL_GRAPH_DPI = "graph_dpi"

WIDGET_TYPE_PUSHBTN = "push_button"
PUSHBTN_TEXT = "push_button_text"
FUNC = "func"




"""Some Default values """
DEFAULT_TICKER = "SPY"
DEFAULT_PERIOD = "1y"
DEFAULT_INTERVAL = "1m"
DEFAULT_STRING = "waku waku"

INTERVAL_LIST = [
    "1m", "2m", "5m", "15m", "30m", "60m", "90m", 
    "1h", "1d", "5d", "1wk", "1mo", "3mo"
]
PERIOD_LIST = [
    "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", 
    "10y", "ytd", "max"
]



"""Template strings"""
STATS_MEAN_TMPL = Template("Mean Returns: $mean")
STATS_SD_TMPL = Template("Std Dev: $sd")
STAT_CORR_TMPL = Template("Corr w SPY: $corr")

ALERT_NORMAL_TMPL = Template("おはよう $time")
ALERT_ERROR_TMPL = Template("WAKARANAI!! $msg")


