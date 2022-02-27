import os

BASE_DIR = os.getcwd()
UI_DIR = os.path.join(BASE_DIR, "ui")

NUMBERS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
UNARY_OPERATIONS = ("+/-", "%", "1/x", "pow(x,2)", "sqrt(x)")
BINARY_OPERATIONS = ("+", "-", "X", "/")
EQ = ("=",)
DEL_CLEAR = ("C", "DEL")
DECIMAL_POINT = (".",)

STYLE_SHEET = """
    
    *{
        background-color: rgba(25, 25, 25, 128);
        
        color: rgb(230, 230, 230);
        font-family: Lucida Sans;
        font-size: 11pt;
    }

    QSizeGrip
    {
        background-color: rgba(255, 255, 255, 128);
    }

    QLabel[title]
    {
        background-color: rgba(0, 0, 0, 0);
        margin-left:9px; 
        font-size: 11pt;
    }

    QLabel[subTitle]
    {
        background-color: rgba(0, 0, 0, 0);
        margin: 9px 0px 9px 9px; 
        font-size: 11pt;
        font-weight: bold;
    }

    QLineEdit#lineEditResult
    {
        font-size: 28pt;
        font-weight: bold;
    }

    QPushButton[menu]
    {
        padding-left: 9px;
        font-size: 11pt;
        text-align: left;
    }

    QPushButton[num="true"]
    {
        background-color: rgba(64, 64, 64, 255);
        color: rgba(255, 255, 255, 255);
        font-size: 12pt;
        font-weight: bold;
    }
    QPushButton[num="false"]
    {
        background-color: rgba(20, 20, 20, 255);
        color: rgba(255, 255, 255, 255);
        font-size: 10pt;
    }

    QPushButton[eq]
    {
        background-color: rgba(67, 255, 240, 255);
        color : rgba(25, 25, 25, 255);
        font-size: 12pt;
        font-weight: bold;
    }

    QPushButton#btnClose
    {
        background-color: rgba(255, 0, 0, 0);
        color: rgba(255, 255, 255, 255);
    }

    QPushButton#btnClose:hover
    {
        background-color: rgba(255, 0, 0, 255);
        color: rgba(255, 255, 255, 255);
    }

    QPushButton#btnClose:pressed
    {
        background-color: rgba(255, 0, 0, 200);
        color: rgba(255, 255, 255, 200);
    }

    QPushButton#btnMinimize
    {
        background-color: rgba(40, 40, 40, 0);
        color: rgb(255, 255, 255);
    }

    QPushButton#btnMinimize:hover
    {
        background-color: rgba(40, 40, 40, 255);
        color: rgb(255, 255, 255);
    }

    QPushButton#btnMinimize:pressed
    {
        background-color: rgba(40, 40, 40, 200);
        color: rgb(255, 255, 255);
    }

    QPushButton#btnMenu
    {
        background-color: rgba(25, 25, 25, 0);
    }

"""