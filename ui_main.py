# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1200, 675)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TopBar = QHBoxLayout()
        self.TopBar.setObjectName(u"TopBar")
        self.NameGroup = QHBoxLayout()
        self.NameGroup.setObjectName(u"NameGroup")
        self.NameLabel = QLabel(self.frame)
        self.NameLabel.setObjectName(u"NameLabel")

        self.NameGroup.addWidget(self.NameLabel)

        self.NameLineEdit = QLineEdit(self.frame)
        self.NameLineEdit.setObjectName(u"NameLineEdit")

        self.NameGroup.addWidget(self.NameLineEdit)


        self.TopBar.addLayout(self.NameGroup)

        self.GameGroup = QHBoxLayout()
        self.GameGroup.setObjectName(u"GameGroup")
        self.GameLabel = QLabel(self.frame)
        self.GameLabel.setObjectName(u"GameLabel")

        self.GameGroup.addWidget(self.GameLabel)

        self.GameLineEdit = QLineEdit(self.frame)
        self.GameLineEdit.setObjectName(u"GameLineEdit")

        self.GameGroup.addWidget(self.GameLineEdit)


        self.TopBar.addLayout(self.GameGroup)

        self.DescriptionGroup = QHBoxLayout()
        self.DescriptionGroup.setObjectName(u"DescriptionGroup")
        self.DescriptionLabel = QLabel(self.frame)
        self.DescriptionLabel.setObjectName(u"DescriptionLabel")

        self.DescriptionGroup.addWidget(self.DescriptionLabel)

        self.DescriptionLineEdit = QLineEdit(self.frame)
        self.DescriptionLineEdit.setObjectName(u"DescriptionLineEdit")

        self.DescriptionGroup.addWidget(self.DescriptionLineEdit)


        self.TopBar.addLayout(self.DescriptionGroup)

        self.PatcherVersion = QLabel(self.frame)
        self.PatcherVersion.setObjectName(u"PatcherVersion")

        self.TopBar.addWidget(self.PatcherVersion)

        self.TopBar.setStretch(0, 2)
        self.TopBar.setStretch(1, 2)
        self.TopBar.setStretch(2, 4)
        self.TopBar.setStretch(3, 1)

        self.horizontalLayout.addLayout(self.TopBar)


        self.verticalLayout_2.addWidget(self.frame)

        self.MainHorizontal = QHBoxLayout()
        self.MainHorizontal.setObjectName(u"MainHorizontal")
        self.MainTabs = QTabWidget(self.centralwidget)
        self.MainTabs.setObjectName(u"MainTabs")
        self.General = QWidget()
        self.General.setObjectName(u"General")
        self.verticalLayout_4 = QVBoxLayout(self.General)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.GeneralSettings = QHBoxLayout()
        self.GeneralSettings.setObjectName(u"GeneralSettings")
        self.SearchLabel = QLabel(self.General)
        self.SearchLabel.setObjectName(u"SearchLabel")

        self.GeneralSettings.addWidget(self.SearchLabel)

        self.SearchField = QLineEdit(self.General)
        self.SearchField.setObjectName(u"SearchField")

        self.GeneralSettings.addWidget(self.SearchField)

        self.WeightedSettingsEnabled = QCheckBox(self.General)
        self.WeightedSettingsEnabled.setObjectName(u"WeightedSettingsEnabled")

        self.GeneralSettings.addWidget(self.WeightedSettingsEnabled)

        self.HideDescriptionTextEnabled = QCheckBox(self.General)
        self.HideDescriptionTextEnabled.setObjectName(u"HideDescriptionTextEnabled")

        self.GeneralSettings.addWidget(self.HideDescriptionTextEnabled)


        self.verticalLayout_4.addLayout(self.GeneralSettings)

        self.MainLayout = QHBoxLayout()
        self.MainLayout.setObjectName(u"MainLayout")
        self.ScrollMain = QScrollArea(self.General)
        self.ScrollMain.setObjectName(u"ScrollMain")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ScrollMain.sizePolicy().hasHeightForWidth())
        self.ScrollMain.setSizePolicy(sizePolicy)
        self.ScrollMain.setWidgetResizable(True)
        self.ScrollMain.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 614, 486))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.Spacer = QSpacerItem(20, 495, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.Spacer)

        self.ScrollMain.setWidget(self.scrollAreaWidgetContents_3)

        self.MainLayout.addWidget(self.ScrollMain)

        self.DescriptionText = QTextEdit(self.General)
        self.DescriptionText.setObjectName(u"DescriptionText")

        self.MainLayout.addWidget(self.DescriptionText)

        self.MainLayout.setStretch(0, 2)
        self.MainLayout.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.MainLayout)

        self.verticalLayout_4.setStretch(1, 1)
        self.MainTabs.addTab(self.General, "")

        self.MainHorizontal.addWidget(self.MainTabs)

        self.Selection = QVBoxLayout()
        self.Selection.setObjectName(u"Selection")
        self.GameSelect = QFrame(self.centralwidget)
        self.GameSelect.setObjectName(u"GameSelect")
        self.GameSelect.setFrameShape(QFrame.Shape.StyledPanel)
        self.GameSelect.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.GameSelect)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.GameSelect)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.ScrollGame = QScrollArea(self.GameSelect)
        self.ScrollGame.setObjectName(u"ScrollGame")
        self.ScrollGame.setWidgetResizable(True)
        self.ScrollGame.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 218, 235))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.Spacer1 = QSpacerItem(20, 221, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.Spacer1)

        self.ScrollGame.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.ScrollGame)


        self.Selection.addWidget(self.GameSelect)

        self.SlotSelect = QFrame(self.centralwidget)
        self.SlotSelect.setObjectName(u"SlotSelect")
        self.SlotSelect.setFrameShape(QFrame.Shape.StyledPanel)
        self.SlotSelect.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.SlotSelect)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.SlotSelect_2 = QLabel(self.SlotSelect)
        self.SlotSelect_2.setObjectName(u"SlotSelect_2")
        self.SlotSelect_2.setFont(font)
        self.SlotSelect_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.SlotSelect_2)

        self.ScrollSlot = QScrollArea(self.SlotSelect)
        self.ScrollSlot.setObjectName(u"ScrollSlot")
        self.ScrollSlot.setWidgetResizable(True)
        self.ScrollSlot.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 218, 235))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.Spacer2 = QSpacerItem(20, 221, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.Spacer2)

        self.ScrollSlot.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.ScrollSlot)


        self.Selection.addWidget(self.SlotSelect)


        self.MainHorizontal.addLayout(self.Selection)

        self.MainHorizontal.setStretch(0, 4)
        self.MainHorizontal.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.MainHorizontal)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.SaveYamlButton = QPushButton(self.centralwidget)
        self.SaveYamlButton.setObjectName(u"SaveYamlButton")

        self.horizontalLayout_3.addWidget(self.SaveYamlButton)

        self.LoadYamlButton = QPushButton(self.centralwidget)
        self.LoadYamlButton.setObjectName(u"LoadYamlButton")

        self.horizontalLayout_3.addWidget(self.LoadYamlButton)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 17))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.NameLabel.setText(QCoreApplication.translate("MainWindow", u"Slot:", None))
        self.GameLabel.setText(QCoreApplication.translate("MainWindow", u"Game:", None))
        self.DescriptionLabel.setText(QCoreApplication.translate("MainWindow", u"Description:", None))
        self.PatcherVersion.setText(QCoreApplication.translate("MainWindow", u"Archipelago Version: 0.6.1", None))
        self.SearchLabel.setText(QCoreApplication.translate("MainWindow", u"Search:", None))
        self.WeightedSettingsEnabled.setText(QCoreApplication.translate("MainWindow", u"Enter Weighted Option Mode", None))
        self.HideDescriptionTextEnabled.setText(QCoreApplication.translate("MainWindow", u"Hide Setting Description", None))
        self.DescriptionText.setMarkdown("")
        self.DescriptionText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.General), QCoreApplication.translate("MainWindow", u"General", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Game", None))
        self.SlotSelect_2.setText(QCoreApplication.translate("MainWindow", u"YAML", None))
        self.SaveYamlButton.setText(QCoreApplication.translate("MainWindow", u"Save YAML as '{slot}_{game}.yaml'", None))
        self.LoadYamlButton.setText(QCoreApplication.translate("MainWindow", u"LOAD YAML", None))
    # retranslateUi

