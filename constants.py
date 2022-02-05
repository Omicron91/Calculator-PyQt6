STYLE_SHEET = """
    *{
        font-family: Lucida Sans;
        font-size: 12pt;
    }
    QWidget#centralwidget{
        background: rgba(80, 50, 200, 128);
    }
    QPushButton{
        background: grey;
        color: white;
        border-radius: 3px;
    }
    QPushButton#pushButton_menu{
        background: rgba(0, 0, 0, 0);
        border-radius: 5px;
    }
    QPushButton#pushButton_menu:hover{
        background: rgba(0, 0, 0, 50);
        border-radius: 5px;
    }

    QPushButton#pushButton_close{
        background: rgba(255, 0, 4, 0);
        color: white;
        border-radius: none;
    }
    QPushButton#pushButton_close:hover{
        background: rgba(255, 0, 4, 150);
        color: white;
        border-radius: none;
    }
    QPushButton#pushButton_close:pressed{
        background: rgba(255, 0, 4, 220);
        color: white;
        border-radius: none;
    }

    QPushButton#pushButton_minimize{
        background: rgba(20, 20, 20, 0);
        color: white;
        border-radius: none;
    }
    QPushButton#pushButton_minimize:hover{
        background: rgba(20, 20, 20, 150);
        color: white;
        border-radius: none;
    }
    QPushButton#pushButton_minimize:pressed{
        background: rgba(20, 20, 20, 220);
        color: white;
        border-radius: none;
    }

    QPushButton:hover{
        background: rgb(116, 116, 116);
    }

    QPushButton:pressed{
        background: rgb(96, 96, 96);
    }

    QPushButton#pushButton_eq{
        background: orange;
    }

    QPushButton#pushButton_eq:hover{
    background: rgb(225, 145, 0);
    }

    QPushButton#pushButton_eq:pressed{
    background: rgb(200, 120, 0);
    }



    QPushButton#pushButton_op1{
        background: rgba(20, 20, 20, 0);
    }

    QPushButton#pushButton_op1:hover{
    background: rgba(20, 20, 20, 40);
    }

    QPushButton#pushButton_op1:pressed{
    background: rgba(20, 20, 20, 80);
    }

    QPushButton#pushButton_op3{
        background: rgba(20, 20, 20, 0);
    }

    QPushButton#pushButton_op3:hover{
    background: rgba(20, 20, 20, 40);
    }

    QPushButton#pushButton_op3:pressed{
    background: rgba(20, 20, 20, 80);
    }

    QFrame#divider{
        color: white;
        border-top: 2px solid  grey;
    }

    QLabel{
        background: rgba(0, 0, 0, 150);
        color: white;
        font-family: Lucida Sans;
        font-weight: bold;
        font-size: 30pt;
    }

    QLabel#label{
        border-radius: 8px;
        padding-left: 12px;
    }

    QLabel#label_title{
        background: rgba(0, 0, 0, 0);
        font-size: 9pt;
    }
"""