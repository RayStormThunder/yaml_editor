# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'added_removed_lists.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SearchFilter = QHBoxLayout()
        self.SearchFilter.setObjectName(u"SearchFilter")
        self.SearchText = QLabel(Form)
        self.SearchText.setObjectName(u"SearchText")
        font = QFont()
        font.setPointSize(12)
        self.SearchText.setFont(font)

        self.SearchFilter.addWidget(self.SearchText)

        self.SearchInputInclude = QLineEdit(Form)
        self.SearchInputInclude.setObjectName(u"SearchInputInclude")
        self.SearchInputInclude.setFont(font)

        self.SearchFilter.addWidget(self.SearchInputInclude)

        self.FilterIncludeText = QLabel(Form)
        self.FilterIncludeText.setObjectName(u"FilterIncludeText")
        self.FilterIncludeText.setFont(font)

        self.SearchFilter.addWidget(self.FilterIncludeText)

        self.FilterInclude = QComboBox(Form)
        self.FilterInclude.setObjectName(u"FilterInclude")
        self.FilterInclude.setFont(font)

        self.SearchFilter.addWidget(self.FilterInclude)

        self.FilterExcludeText = QLabel(Form)
        self.FilterExcludeText.setObjectName(u"FilterExcludeText")
        self.FilterExcludeText.setFont(font)

        self.SearchFilter.addWidget(self.FilterExcludeText)

        self.FilterExclude = QComboBox(Form)
        self.FilterExclude.setObjectName(u"FilterExclude")
        self.FilterExclude.setFont(font)

        self.SearchFilter.addWidget(self.FilterExclude)

        self.TypeText = QLabel(Form)
        self.TypeText.setObjectName(u"TypeText")
        self.TypeText.setFont(font)

        self.SearchFilter.addWidget(self.TypeText)

        self.Type = QComboBox(Form)
        self.Type.setObjectName(u"Type")
        self.Type.setFont(font)

        self.SearchFilter.addWidget(self.Type)

        self.SearchFilter.setStretch(1, 1)
        self.SearchFilter.setStretch(3, 1)
        self.SearchFilter.setStretch(5, 1)
        self.SearchFilter.setStretch(7, 1)

        self.verticalLayout.addLayout(self.SearchFilter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_3)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.Lists = QHBoxLayout()
        self.Lists.setObjectName(u"Lists")
        self.IncludeList = QListView(Form)
        self.IncludeList.setObjectName(u"IncludeList")
        self.IncludeList.setFont(font)

        self.Lists.addWidget(self.IncludeList)

        self.ManageList = QVBoxLayout()
        self.ManageList.setObjectName(u"ManageList")
        self.SpacerTop = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.ManageList.addItem(self.SpacerTop)

        self.Move = QPushButton(Form)
        self.Move.setObjectName(u"Move")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Move.sizePolicy().hasHeightForWidth())
        self.Move.setSizePolicy(sizePolicy)
        self.Move.setFont(font)

        self.ManageList.addWidget(self.Move)

        self.SpacerBottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.ManageList.addItem(self.SpacerBottom)

        self.AddRemoveInput = QLineEdit(Form)
        self.AddRemoveInput.setObjectName(u"AddRemoveInput")
        self.AddRemoveInput.setFont(font)

        self.ManageList.addWidget(self.AddRemoveInput)

        self.AddRemoveButton = QPushButton(Form)
        self.AddRemoveButton.setObjectName(u"AddRemoveButton")
        self.AddRemoveButton.setFont(font)

        self.ManageList.addWidget(self.AddRemoveButton)


        self.Lists.addLayout(self.ManageList)

        self.ExcludeList = QListView(Form)
        self.ExcludeList.setObjectName(u"ExcludeList")
        self.ExcludeList.setFont(font)

        self.Lists.addWidget(self.ExcludeList)

        self.Lists.setStretch(0, 2)
        self.Lists.setStretch(1, 1)
        self.Lists.setStretch(2, 2)

        self.verticalLayout.addLayout(self.Lists)

        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SearchText.setText(QCoreApplication.translate("Form", u"Search:", None))
        self.SearchInputInclude.setPlaceholderText(QCoreApplication.translate("Form", u"Type to search Include and Exclude List", None))
        self.FilterIncludeText.setText(QCoreApplication.translate("Form", u"Filter Include:", None))
        self.FilterExcludeText.setText(QCoreApplication.translate("Form", u"Filter Exclude:", None))
        self.TypeText.setText(QCoreApplication.translate("Form", u"Type:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Included List", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"Excluded List", None))
        self.Move.setText(QCoreApplication.translate("Form", u"<- Move ->", None))
        self.AddRemoveInput.setText("")
        self.AddRemoveInput.setPlaceholderText(QCoreApplication.translate("Form", u"Type what to remove/add", None))
        self.AddRemoveButton.setText(QCoreApplication.translate("Form", u"Add/Remove from Lists", None))
    # retranslateUi

