# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'row.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QSizePolicy, QWidget)

class Ui_BasicRow(object):
    def setupUi(self, BasicRow):
        if not BasicRow.objectName():
            BasicRow.setObjectName(u"BasicRow")
        BasicRow.resize(1000, 30)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BasicRow.sizePolicy().hasHeightForWidth())
        BasicRow.setSizePolicy(sizePolicy)
        BasicRow.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(12)
        BasicRow.setFont(font)
        self.horizontalLayout = QHBoxLayout(BasicRow)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(BasicRow)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(4, 0, 0, 0)
        self.SettingLabel = QLabel(self.frame)
        self.SettingLabel.setObjectName(u"SettingLabel")

        self.horizontalLayout_2.addWidget(self.SettingLabel)

        self.SettingSimpleCombo = QComboBox(self.frame)
        self.SettingSimpleCombo.setObjectName(u"SettingSimpleCombo")
        self.SettingSimpleCombo.setEditable(True)

        self.horizontalLayout_2.addWidget(self.SettingSimpleCombo)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(BasicRow)

        QMetaObject.connectSlotsByName(BasicRow)
    # setupUi

    def retranslateUi(self, BasicRow):
        BasicRow.setWindowTitle(QCoreApplication.translate("BasicRow", u"Form", None))
        self.SettingLabel.setText(QCoreApplication.translate("BasicRow", u"Example Setting:", None))
    # retranslateUi

