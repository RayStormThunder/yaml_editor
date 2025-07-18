# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
        self.verticalLayout_8 = QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.TopBar = QHBoxLayout()
        self.TopBar.setObjectName(u"TopBar")
        self.YAMLGroup = QHBoxLayout()
        self.YAMLGroup.setObjectName(u"YAMLGroup")
        self.YAMLName = QLabel(self.frame)
        self.YAMLName.setObjectName(u"YAMLName")

        self.YAMLGroup.addWidget(self.YAMLName)

        self.YAMLLineEdit = QLineEdit(self.frame)
        self.YAMLLineEdit.setObjectName(u"YAMLLineEdit")

        self.YAMLGroup.addWidget(self.YAMLLineEdit)


        self.TopBar.addLayout(self.YAMLGroup)

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

        self.DescriptionGroup.setStretch(1, 2)

        self.TopBar.addLayout(self.DescriptionGroup)

        self.TopBar.setStretch(0, 5)
        self.TopBar.setStretch(1, 4)
        self.TopBar.setStretch(2, 4)
        self.TopBar.setStretch(3, 8)

        self.verticalLayout_8.addLayout(self.TopBar)


        self.verticalLayout_2.addWidget(self.frame)

        self.MainHorizontal = QHBoxLayout()
        self.MainHorizontal.setObjectName(u"MainHorizontal")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.Settings = QFrame(self.centralwidget)
        self.Settings.setObjectName(u"Settings")
        self.Settings.setFrameShape(QFrame.Shape.StyledPanel)
        self.Settings.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.Settings)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.RedState = QCheckBox(self.Settings)
        self.RedState.setObjectName(u"RedState")
        self.RedState.setChecked(True)

        self.horizontalLayout.addWidget(self.RedState)

        self.GreenState = QCheckBox(self.Settings)
        self.GreenState.setObjectName(u"GreenState")
        self.GreenState.setChecked(True)

        self.horizontalLayout.addWidget(self.GreenState)

        self.BlueState = QCheckBox(self.Settings)
        self.BlueState.setObjectName(u"BlueState")
        self.BlueState.setChecked(True)

        self.horizontalLayout.addWidget(self.BlueState)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.WeightedSettingsEnabled = QCheckBox(self.Settings)
        self.WeightedSettingsEnabled.setObjectName(u"WeightedSettingsEnabled")

        self.horizontalLayout.addWidget(self.WeightedSettingsEnabled)

        self.HideDescriptionTextEnabled = QCheckBox(self.Settings)
        self.HideDescriptionTextEnabled.setObjectName(u"HideDescriptionTextEnabled")

        self.horizontalLayout.addWidget(self.HideDescriptionTextEnabled)


        self.verticalLayout_9.addWidget(self.Settings)

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
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 49, 454))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.Spacer = QSpacerItem(20, 495, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.Spacer)

        self.ScrollMain.setWidget(self.scrollAreaWidgetContents_3)

        self.MainLayout.addWidget(self.ScrollMain)

        self.DescriptionText = QTextEdit(self.General)
        self.DescriptionText.setObjectName(u"DescriptionText")
        self.DescriptionText.setReadOnly(True)
        self.DescriptionText.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.MainLayout.addWidget(self.DescriptionText)

        self.MainLayout.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.MainLayout)

        self.verticalLayout_4.setStretch(1, 1)
        self.MainTabs.addTab(self.General, "")

        self.verticalLayout_9.addWidget(self.MainTabs)


        self.MainHorizontal.addLayout(self.verticalLayout_9)

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
        self.YAMLName.setText(QCoreApplication.translate("MainWindow", u"YAML Prefix Name:", None))
        self.NameLabel.setText(QCoreApplication.translate("MainWindow", u"Slot:", None))
        self.GameLabel.setText(QCoreApplication.translate("MainWindow", u"Game:", None))
        self.DescriptionLabel.setText(QCoreApplication.translate("MainWindow", u"Description:", None))
        self.RedState.setText(QCoreApplication.translate("MainWindow", u"Enable Yellow Highlighting", None))
        self.GreenState.setText(QCoreApplication.translate("MainWindow", u"Enable Green Highlighting", None))
        self.BlueState.setText(QCoreApplication.translate("MainWindow", u"Enable Blue Highlighting", None))
        self.WeightedSettingsEnabled.setText(QCoreApplication.translate("MainWindow", u"Enter Weighted Option Mode", None))
        self.HideDescriptionTextEnabled.setText(QCoreApplication.translate("MainWindow", u"Hide Setting Description", None))
        self.SearchLabel.setText(QCoreApplication.translate("MainWindow", u"Search:", None))
        self.DescriptionText.setMarkdown(QCoreApplication.translate("MainWindow", u"Getting Started:\n"
"\n"
"**_Loading a YAML:**_\n"
"\n"
"To properly edit a game's yaml. Start by adding a template yaml of that game\n"
"into the 'YAMLS' folder. Upon doing this, a folder with that game's name should\n"
"appear. You can either place a previously edited yaml into that folder, or you\n"
"can load the base yaml that is already in there. You can select your game on\n"
"the right, followed by the yaml you want.\n"
"\n"
"**_Saving a YAML:**_\n"
"\n"
"Once you have changed your yaml to your liking. You can hit the save button at\n"
"the bottom. The file will saved into it's game folder inside 'YAMLS.' The file\n"
"name will be {YAML Prefix Name}-{Game Name}.yaml. If you already have a file\n"
"with that name it will be overwritten. So change the 'YAML Prefix Name' if you\n"
"don't want to overwrite your file.\n"
"\n"
"\n"
"**_Row Color Meaning:**_\n"
"\n"
"Green: Green means that you changed the value of that row in this session.\n"
"Blue\n"
": Blue means the value of a row is different from the val"
                        "ue of that row in the template file.\n"
"\n"
"Yellow: Yellow means that it is a row or value that was added by you manually.\n"
"\n"
"\n"
"**_Adding items to list tabs:**_\n"
"\n"
"On the non-general tabs, you may have some lists that are missing data. By\n"
"typing information into the 'add/remove' field in the bottom middle, you can\n"
"add (or remove) that item from the list. Once an item is added to the list, it\n"
"will always be there across any yaml for that game. This can be useful for\n"
"lists that aren't associated with items or locations. Or if you don't have a\n"
"datapackage.\n"
"\n"
"**_What does a datapackage do:**_\n"
"\n"
"If your game has a datapackage, it will automatically fill the lists in\n"
"non-general tabs with the items and locations associated with your game. It\n"
"also allows for the filtering dropdowns to have useful things to filter. If you\n"
"do not have a datapackage, all lists will be empty by default and you will not\n"
"be able to filter anything. \n"
"\n"
"**_Obtaining a "
                        "datapackage:**_\n"
"\n"
"This program will automatically update the supported game datapackage if you\n"
"are connected to the internet. If you want to get the datapackage of an\n"
"unsupported game because  your game does not have a datapackage, or if new\n"
"items or locations have been added. You can create a multiworld with that game.\n"
"Then have this yaml editor connect to that multiworld and it will extract the\n"
"datapackage. This is done by not having a yaml loaded and filling out the\n"
"fields at the top (not including 'YAML Prefix Name') and then pressing the\n"
"'Extract Datapackage with Server Connection' button at the bottom. Keep in mind\n"
"that some of the fields are case sensitive. So make sure you have it correct.\n"
"\n"
"    \n"
"\n"
"", None))
        self.DescriptionText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Getting Started:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; text-deco"
                        "ration: underline;\">Loading a YAML:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To properly edit a game's yaml. Start by adding a template yaml of that game into the 'YAMLS' folder. Upon doing this, a folder with that game's name should appear. You can either place a previously edited yaml into that folder, or you can load the base yaml that is already in there. You can select your game on the right, followed by the yaml you want.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; text-decoration: underline;\">Saving a YAML:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0"
                        "px;\">Once you have changed your yaml to your liking. You can hit the save button at the bottom. The file will saved into it's game folder inside 'YAMLS.' The file name will be {YAML Prefix Name}-{Game Name}.yaml. If you already have a file with that name it will be overwritten. So change the 'YAML Prefix Name' if you don't want to overwrite your file.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-weight:700; text-decoration: underline;\">Row Color Meaning:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ff00;\">Green</span>: Green means that you changed the value of that row in this session.<br /><span style=\" color:#00aaff;\">Blue</span>: Blue means the value of a row is different from the value of that row in the template file.<br /><span style=\" color:#ffff00;\">Yellow</span>: Yellow mea"
                        "ns that it is a row or value that was added by you manually.<br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; text-decoration: underline;\">Adding items to list tabs:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">On the non-general tabs, you may have some lists that are missing data. By typing information into the 'add/remove' field in the bottom middle, you can add (or remove) that item from the list. Once an item is added to the list, it will always be there across any yaml for that game. This can be useful for lists that aren't associated with items or locations. Or if you don't have a datapackage.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bott"
                        "om:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; text-decoration: underline;\">What does a datapackage do:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If your game has a datapackage, it will automatically fill the lists in non-general tabs with the items and locations associated with your game. It also allows for the filtering dropdowns to have useful things to filter. If you do not have a datapackage, all lists will be empty by default and you will not be able to filter anything. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700; text-decoration: underline;\">Obtaining a datapackage:</spa"
                        "n></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program will automatically update the supported game datapackage if you are connected to the internet. If you want to get the datapackage of an unsupported game because  your game does not have a datapackage, or if new items or locations have been added. You can create a multiworld with that game. Then have this yaml editor connect to that multiworld and it will extract the datapackage. This is done by not having a yaml loaded and filling out the fields at the top (not including 'YAML Prefix Name') and then pressing the 'Extract Datapackage with Server Connection' button at the bottom. Keep in mind that some of the fields are case sensitive. So make sure you have it correct.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">    </span></p></body></html>", None))
        self.MainTabs.setTabText(self.MainTabs.indexOf(self.General), QCoreApplication.translate("MainWindow", u"General", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Game", None))
        self.SlotSelect_2.setText(QCoreApplication.translate("MainWindow", u"YAML", None))
        self.SaveYamlButton.setText(QCoreApplication.translate("MainWindow", u"Save YAML as '{slot}_{game}.yaml'", None))
        self.LoadYamlButton.setText(QCoreApplication.translate("MainWindow", u"LOAD YAML", None))
    # retranslateUi

