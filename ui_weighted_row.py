# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'weighted_row.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_WeightedRow(object):
    def setupUi(self, WeightedRow):
        if not WeightedRow.objectName():
            WeightedRow.setObjectName(u"WeightedRow")
        WeightedRow.resize(1000, 300)
        font = QFont()
        font.setPointSize(12)
        WeightedRow.setFont(font)
        self.horizontalLayout = QHBoxLayout(WeightedRow)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(WeightedRow)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 0, 0, 0)
        self.Vertial = QVBoxLayout()
        self.Vertial.setObjectName(u"Vertial")
        self.Name = QLabel(self.frame)
        self.Name.setObjectName(u"Name")
        self.Name.setFont(font)
        self.Name.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.Vertial.addWidget(self.Name)

        self.AddRow = QPushButton(self.frame)
        self.AddRow.setObjectName(u"AddRow")

        self.Vertial.addWidget(self.AddRow)


        self.horizontalLayout_2.addLayout(self.Vertial)

        self.SubRowHolder = QVBoxLayout()
        self.SubRowHolder.setSpacing(2)
        self.SubRowHolder.setObjectName(u"SubRowHolder")

        self.horizontalLayout_2.addLayout(self.SubRowHolder)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(WeightedRow)

        QMetaObject.connectSlotsByName(WeightedRow)
    # setupUi

    def retranslateUi(self, WeightedRow):
        WeightedRow.setWindowTitle(QCoreApplication.translate("WeightedRow", u"Form", None))
        self.Name.setText(QCoreApplication.translate("WeightedRow", u"TextLabel", None))
        self.AddRow.setText(QCoreApplication.translate("WeightedRow", u"Add New Row", None))
    # retranslateUi

