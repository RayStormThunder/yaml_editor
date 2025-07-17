# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'weighted_sub_row.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QSizePolicy,
    QSpinBox, QWidget)

class Ui_SepecificSetting(object):
    def setupUi(self, SepecificSetting):
        if not SepecificSetting.objectName():
            SepecificSetting.setObjectName(u"SepecificSetting")
        SepecificSetting.resize(600, 34)
        font = QFont()
        font.setPointSize(12)
        SepecificSetting.setFont(font)
        self.horizontalLayout = QHBoxLayout(SepecificSetting)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.SpecificSettingName = QLineEdit(SepecificSetting)
        self.SpecificSettingName.setObjectName(u"SpecificSettingName")

        self.horizontalLayout.addWidget(self.SpecificSettingName)

        self.SpecificSettingNumber = QSpinBox(SepecificSetting)
        self.SpecificSettingNumber.setObjectName(u"SpecificSettingNumber")
        self.SpecificSettingNumber.setMaximum(9999999)

        self.horizontalLayout.addWidget(self.SpecificSettingNumber)


        self.retranslateUi(SepecificSetting)

        QMetaObject.connectSlotsByName(SepecificSetting)
    # setupUi

    def retranslateUi(self, SepecificSetting):
        SepecificSetting.setWindowTitle(QCoreApplication.translate("SepecificSetting", u"Form", None))
    # retranslateUi

