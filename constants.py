import os

BASE_DIR = os.getcwd()
UI_DIR = os.path.join(BASE_DIR, "ui")

STYLE_SHEET = """
    
    *{
        background-color: rgba(25, 25, 25, 128);
        
        color: rgb(230, 230, 230);
        font-family: Lucida Sans;
        font-size: 11pt;
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

    QLabel#labelResult
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

    QPushButton[num]
    {
        background-color: rgb(0, 0, 0);
        color: rgb(255, 255, 255);
        font-size: 12pt;
        font-weight: bold;
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
        color: rgb(255, 255, 255);
    }

    QPushButton#btnMinimize
    {
        background-color: rgba(25, 25, 25, 0);
        color: rgb(255, 255, 255);
    }

    QPushButton#btnMenu
    {
        background-color: rgba(25, 25, 25, 0);
    }

"""