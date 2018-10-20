import sys
from PySide import QtCore, QtGui
from datetime import datetime
from cPickle import load, dump
from PageSetups import getData
from CitadelQuotation import createPDF


def hex2QColor(c):
    """Convert Hex color to QColor"""
    r = int(c[0:2], 16)
    g = int(c[2:4], 16)
    b = int(c[4:6], 16)
    return QtGui.QColor(r, g, b)


def rounder(num):
    if num % 1 == 0.0:
        return int(num)
    else:
        return num


class FormOne(QtGui.QWidget):
    """ First Page of the Application """
    def __init__(self, parent=None):
        super(FormOne, self).__init__(parent)
        horiz = 35
        vert = 65
        now = datetime.now()
        self.basecolor = "efefef"

        # Initialize fonts
        QtGui.QFontDatabase.addApplicationFont('Fonts/Alwyn Bold.ttf')
        Alwyn = QtGui.QFont("Alwyn Bold", 23)
        QtGui.QFontDatabase.addApplicationFont('Fonts/MavenProBold.otf')
        Bebas = QtGui.QFont("MavenProBold", 11)  # , QFont.Bold
        QtGui.QFontDatabase.addApplicationFont('Fonts/MavenProBold.otf')
        BebasSmall = QtGui.QFont("MavenProBold", 9)

        # Make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.backgroundColor = hex2QColor(self.basecolor)
        self.foregroundColor = hex2QColor("333333")
        self.borderRadius = 10
        self.draggable = True
        self.dragging_threshould = 5
        self.__mousePressPos = None
        self.__mouseMovePos = None

        # Define all the elements in the page
        self.label_Title = self.createLabel(
            [horiz+10, vert], [400, 80], "Citadel Ecobuild", Alwyn)

        vert += 60
        self.label_CName = self.createLabel(
            [horiz+5, vert+30], [180, 20], "Client Name:", Bebas)
        self.textBoxCName = self.createTextBox(
            (horiz+180, vert+27), (230, 25), "")

        vert += 33
        self.label_AddrTo = self.createLabel(
            [horiz+5, vert+30], [180, 20], "Addressed To:", Bebas)
        self.textBoxAddrTo = self.createTextBox(
            (horiz+180, vert+27), (230, 25), "")

        vert += 33
        self.label_CAddress = self.createLabel(
            [horiz+5, vert+30], [180, 20], "Client Address:", Bebas)
        self.textBoxCAddress = self.createTextBox(
            (horiz+180, vert+27), (230, 25), "")

        vert += 33
        self.label_AName = self.createLabel(
            [horiz+5, vert+30], [180, 25], "Agent Name:", Bebas)
        self.textBoxAName = self.createTextBox(
            (horiz+180, vert+27), (230, 25), "")

        vert += 33
        self.label_APost = self.createLabel(
            [horiz+5, vert+30], [180, 25], "Agent Post:", Bebas)
        self.textBoxAPost = self.createTextBox(
            (horiz+180, vert+27), (230, 25), "")

        vert += 33
        self.label_AMobile = self.createLabel(
            [horiz+5, vert+30], [180, 25], "Agent Ph No.:", Bebas)
        self.textBoxAMobile = self.createTextBox(
            (horiz+180, vert+27), (230, 25), "")
        self.textBoxAMobile.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp("[- \d]+")))

        vert += 33
        self.label_Dte = self.createLabel(
            (horiz+5, vert+30), (180, 20), "Date:", Bebas)
        self.dateLineEdit = QtGui.QDateEdit(now.today(), self)
        self.dateLineEdit.move(horiz+180, vert+27)
        self.dateLineEdit.setCalendarPopup(True)
        self.dateLineEdit.setDisplayFormat("MMMM d, yyyy")
        self.dateLineEdit.resize(230, 25)

        vert += 33
        self.label_OrdTy = self.createLabel(
            (horiz+5, vert+30), (180, 20), "Order Type:", Bebas)
        self.combo_OrdTy = self.createCombobox(
            (horiz+180, vert+27), (230, 27), ["AAC Slabs", "Blocks", "Lintel", "Wall Panels"])

        vert += 33
        self.label_Rate = self.createLabel(
            [horiz+5, vert+30], [180, 20], "Rate per cm:", Bebas)
        self.textBoxRate = self.createTextBox(
            (horiz+180, vert+27), (105, 25), "")
        self.textBoxRate.setText("0")
        self.label_Rs = self.createLabel(
            [horiz+245, vert+29], [35, 20], "INR", Bebas)
        self.textBoxRate.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[\d]{,8}\.[\d]{,2}")))
        self.combo_GST = self.createCombobox(
            (horiz+345, vert+26), (65, 27), ["CGST", "IGST"])
        self.label_GST = self.createLabel(
            [horiz+300, vert+29], [40, 20], "GST", BebasSmall)

        vert += 38
        self.label_Trans = self.createLabel(
            (horiz+5, vert+30), (250, 20), "Transportion Included:", Bebas)
        self.chk_box_Trans = QtGui.QCheckBox(self, "")
        self.chk_box_Trans.setChecked(True)
        self.chk_box_Trans.move(horiz+260, vert+30)
        self.chk_box_Trans.resize(20, 20)
        self.chk_box_Trans.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        self.chk_box_Trans.setStyleSheet(
            "QCheckBox::indicator { width: 20px; height: 20px;} border-radius: 10px;")
        self.chk_box_Trans.stateChanged.connect(self.transport)

        self.textBoxTransAmount = self.createTextBox(
            (horiz+265, vert+27), (95, 25), "")
        self.textBoxTransAmount.setText("0")
        self.label_TransInr = self.createLabel(
            (horiz+315, vert+29), (100, 20), "INR", Bebas)
        self.label_TransAm = self.createLabel(
            (horiz+380, vert+29), (100, 20), "Amt", Bebas)
        self.textBoxTransAmount.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp("[\d]{,7}\.[\d]{,2}")))

        if self.chk_box_Trans.isChecked() == True:
            self.textBoxTransAmount.hide()
            self.label_TransInr.hide()
            self.label_TransAm.hide()
        else:
            self.textBoxTransAmount.show()
            self.label_TransInr.show()
            self.label_TransAm.show()

        vert += 60
        self.minimizeButton = self.createButton("Generate PDF", (horiz+60, vert+33), (130, 30), lambda: self.genPDF(
            True), "color: #000;border: 2px solid #555;border-radius: 5px;padding: 5px;min-width: 80px;background-color: rgb(255, 255,255);")
        self.minimizeButton = self.createButton("Generate Print", (horiz+240, vert+33), (130, 30), lambda: self.genPDF(
            False), "color: #000;border: 2px solid #555;border-radius: 5px;padding: 5px;min-width: 80px;background-color: rgb(255, 255,255);")

        self.minimizeButton = self.createButton(
            "", (440, 36), (17, 5), self.minimizeWindow, "background-color: black")
        self.exitButton = self.createButton(
            "", (405, 31), (17, 17), self.closeUI, "background-color:  rgb(239,239,239)")
        self.exitButton.setIcon(QtGui.QIcon("Images/57165-cross-sign.png"))
        self.exitButton.setIconSize(QtCore.QSize(19, 19))
        self.exitButton.setFlat(True)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(QtGui.QSizeGrip(self), 0,
                         QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.getO = ""

        self.setMinimumSize(495, 640)
        self.setMaximumSize(495, 640)

    def genPDF(self, isPrint):
        """ Generate PDF file """

        inData = {}
        inData['Client Name'] = self.textBoxCName.text()
        inData['AgentPos'] = self.textBoxAPost.text()
        inData['Addressed To'] = self.textBoxAddrTo.text()
        inData['Client Address'] = self.textBoxCAddress.text()
        inData['Date'] = self.dateLineEdit.date().toString('dd.MM.yyyy')
        inData['AgentPh'] = self.textBoxAMobile.text()
        inData['AgentName'] = self.textBoxAName.text()
        inData['Rate'] = rounder(float(self.textBoxRate.text()))
        inData['Type'] = self.combo_OrdTy.currentText()
        inData['Transportation'] = self.chk_box_Trans.isChecked()
        inData['TransportationCost'] = rounder(
            float(self.textBoxTransAmount.text()))
        inData['GST Type'] = self.combo_GST.currentText()

        if self.combo_OrdTy.currentText() == "Blocks":
            self.getO = BlocksOrder(inData, isPrint)
            self.getO.show()
        else:
            self.getO = getOrder(
                self.combo_OrdTy.currentText(), inData, isPrint)
            self.getO.show()

    def transport(self):
        if self.chk_box_Trans.isChecked() == True:
            self.textBoxTransAmount.hide()
            self.label_TransInr.hide()
            self.label_TransAm.hide()
        else:
            self.textBoxTransAmount.show()
            self.label_TransInr.show()
            self.label_TransAm.show()

    def closeUI(self):
        self.close()

    def createButton(self, text, pos, size, function, css=""):
        """ Wrapper to create a button """

        Button = QtGui.QPushButton(text, self)  # Define button
        Button.move(pos[0], pos[1])  # Define position
        Button.clicked.connect(function)    # Define on click event
        Button.resize(size[0], size[1]) # Define size
        Button.setStyleSheet(css)  # Define CSS 
        return Button

    def createTextBox(self, pos, size, texte="", key="", data=[]):
        """ Wrapper to create a text box """

        textBox = QtGui.QLineEdit(self)
        if key == "comp":
            completer = CustomQCompleter()
            textBox.setCompleter(completer)
            model = QStringListModel()
            completer.setModel(model)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
            model.setStringList(data)

        textBox.resize(size[0], size[1])
        textBox.move(pos[0], pos[1])
        textBox.setText(texte)
        return textBox

    def createLabel(self, pos, size, data, font):
        """ Wrapper to create a text label """

        label = QtGui.QLabel(data, self)
        label.resize(size[0], size[1])
        label.setFont(font)
        label.move(pos[0], pos[1])
        return label

    def createCombobox(self, pos, size, data, key=""):
        """ Wrapper to create a combo box element """

        comboBox = QtGui.QComboBox(self)
        if key == "comp":
            comboBox.setEditable(True)
            c = QtGui.QCompleter(data)
            c.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            c.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
            comboBox.setCompleter(c)
        else:
            for i in data:
                comboBox.addItem(i)
        comboBox.move(pos[0], pos[1])
        comboBox.resize(size[0], size[1])
        comboBox.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        return comboBox

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()                # global
            self.__mouseMovePos = event.globalPos() - self.pos()    # local
        super(FormOne, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & QtCore.Qt.LeftButton:
            globalPos = event.globalPos()
            moved = globalPos - self.__mousePressPos
            if moved.manhattanLength() > self.dragging_threshould:
                # move when user drag window more than dragging_threshould
                diff = globalPos - self.__mouseMovePos
                self.move(diff)
                self.__mouseMovePos = globalPos - self.pos()
        super(FormOne, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            if event.button() == QtCore.Qt.LeftButton:
                moved = event.globalPos() - self.__mousePressPos
                if moved.manhattanLength() > self.dragging_threshould:
                    # do not call click event or so on
                    event.ignore()
                self.__mousePressPos = None
        super(FormOne, self).mouseReleaseEvent(event)

    def minimizeWindow(self):
        self.showNormal()
        self.showMinimized()

    def keyPressEvent(self, e):      # In the event that a key is pressed
        if e.key() == QtCore.Qt.Key_Escape:   # If key pressed is Excape Key
            self.close()


class BlocksOrder(QtGui.QWidget):
    """ Form to get additional information for block orders """

    def __init__(self, inData, isPrint, parent=None):
        super(BlocksOrder, self).__init__(parent)
        horiz = 44
        vert = 40
        self.basecolor = "efefef"

        # fonts
        QtGui.QFontDatabase.addApplicationFont('Fonts/Alwyn Bold.ttf')
        Alwyn = QtGui.QFont("Alwyn Bold", 23)
        QtGui.QFontDatabase.addApplicationFont('Fonts/BebasNeue.ttf')
        Bebas = QtGui.QFont("BebasNeue", 13)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.backgroundColor = hex2QColor(self.basecolor)
        self.foregroundColor = hex2QColor("333333")
        self.borderRadius = 10
        self.draggable = True
        self.dragging_threshould = 5
        self.__mousePressPos = None
        self.__mouseMovePos = None

        self.textlable = self.createLabel(
            (horiz+80, vert), (250, 40), "Blocks", Alwyn)
        vert += 75
        self.label_BlockSize = self.createLabel(
            (horiz, vert), (180, 20), "Blocks Size:", Bebas)
        self.combo_BlockSize = self.createCombobox(
            (horiz+190, vert-3), (120, 27), ["200 x 625", "250 x 625", "240 x 650"])

        vert += 40
        self.label_TruckVol = self.createLabel(
            (horiz, vert), (180, 20), "Truck Volume:", Bebas)
        self.combo_TruckVol = self.createCombobox(
            (horiz+190, vert-3), (120, 27), ["15 cum", "21 cum", "24 cum", "28 cum", "30 cum"])

        buttonCSS = "color: #000;border: 2px solid #555;border-radius: 5px;padding: 5px;min-width: 80px;background-color: rgb(255, 255,255);"

        vert += 60
        self.okbutton = self.createButton(
            "Generate", (horiz+105, vert), (60, 30), lambda: self.genPDF(inData, isPrint), css=buttonCSS)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(QtGui.QSizeGrip(self), 0,
                         QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.exitButton = self.createButton(
            "", (345, 21), (15, 15), self.closeUI, "background-color:  rgb(239,239,239)")
        self.exitButton.setIcon(QtGui.QIcon("Images/57165-cross-sign.png"))
        self.exitButton.setIconSize(QtCore.QSize(19, 19))
        self.exitButton.setFlat(True)

        self.setMinimumSize(400, vert+75)
        self.setMaximumSize(400, vert+75)

    def closeUI(self):
        self.close()

    def createTextBox(self, pos, size, texte="", key="", data=[]):
        textBox = QtGui.QLineEdit(self)

        if key == "comp":
            completer = CustomQCompleter()
            textBox.setCompleter(completer)
            model = QStringListModel()
            completer.setModel(model)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
            model.setStringList(data)

        textBox.resize(size[0], size[1])
        textBox.move(pos[0], pos[1])
        textBox.setText(texte)
        return textBox

    def createCombobox(self, pos, size, data, key=""):
        comboBox = QtGui.QComboBox(self)
        if key == "comp":
            comboBox.setEditable(True)
            c = QtGui.QCompleter(data)
            c.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            c.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
            comboBox.setCompleter(c)
        else:
            for i in data:
                comboBox.addItem(i)
        comboBox.move(pos[0], pos[1])
        comboBox.resize(size[0], size[1])
        comboBox.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        return comboBox

    def createLabel(self, pos, size, data, font):
        label = QtGui.QLabel(data, self)
        label.resize(size[0], size[1])
        label.setFont(font)
        label.move(pos[0], pos[1])
        return label

    def createButton(self, text, pos, size, function, css=""):
        Button = QtGui.QPushButton(text, self)  # Define button
        # Position the button
        Button.move(pos[0], pos[1])
        Button.clicked.connect(function)
        Button.resize(size[0], size[1])
        Button.setStyleSheet(css)
        return Button

    def genPDF(self, inData, isPrint):
        inData['Required Quantity'] = {}
        inData['Block Size'] = self.combo_BlockSize.currentText()
        inData['Truck Size'] = self.combo_TruckVol.currentText()

        outPath = QtGui.QFileDialog.getSaveFileName(
            self, 'Save Pdf', '', "PDF files (*.pdf)")
        if createPDF(outPath[0], getData(inData), isPrint, inData['Rate'], inData['Transportation'], TransVal=inData['TransportationCost']):
            self.msgbox = MsgBox(self.basecolor, "PDF  Successfully  Saved")
            self.msgbox.show()
            self.close()
        else:
            self.msgbox = MsgBox(self.basecolor, "     PDF  Saving  Failed")
            self.msgbox.show()

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

    def center(self):      # Initialize the window at the centre of the screen
        # Get the position rectangle around our window
        qr = self.frameGeometry()
        # Get the screen size of the desktop and find its centre
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        # Move the position rectangle around our window to the center calculated
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):      # In the event that a key is pressed
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:   # If key pressed is Excape Key
            self.closeP()


class getOrder(QtGui.QWidget):
    """ Form to get more order details """

    def __init__(self, categ, inData, isPrint, parent=None):
        super(getOrder, self).__init__(parent)
        horiz = 44
        vert = 50
        self.basecolor = "efefef"

        # fonts
        QtGui.QFontDatabase.addApplicationFont('Fonts/Alwyn Bold.ttf')
        Alwyn = QtGui.QFont("Alwyn Bold", 17)
        QtGui.QFontDatabase.addApplicationFont('Fonts/BebasNeue.ttf')
        Bebas = QtGui.QFont("BebasNeue", 13)
        BebasSmall = QtGui.QFont("BebasNeue", 10)
        QtGui.QFontDatabase.addApplicationFont('Fonts/Queen of Camelot.ttf')
        Queen = QtGui.QFont("Queen of Camelot", 8)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.backgroundColor = hex2QColor(self.basecolor)
        self.foregroundColor = hex2QColor("333333")
        self.borderRadius = 10
        self.draggable = True
        self.dragging_threshould = 5
        self.__mousePressPos = None
        self.__mouseMovePos = None

        self.textlable = self.createLabel(
            (horiz+8, vert), (250, 30), categ, Alwyn)
        vert += 60
        validator_Amt = QtGui.QRegExpValidator(QtCore.QRegExp("[\d]{,4}"))
        self.textlable = self.createLabel(
            (horiz-10, vert+3), (200, 30), "Size of "+categ+" :", Bebas)
        self.textbox_t = self.createTextBox((horiz+155+60, vert+3), (40, 25))
        self.textbox_b = self.createTextBox((horiz+218+75, vert+3), (40, 25))
        self.textbox_l = self.createTextBox((horiz+281+85, vert+3), (40, 25))
        self.textbox_t.setValidator(validator_Amt)
        self.textbox_b.setValidator(validator_Amt)
        self.textbox_l.setValidator(validator_Amt)
        self.label_t = self.createLabel(
            (horiz+146+50, vert+28), (100, 25), "THICKNESS", Queen)
        self.label_t = self.createLabel(
            (horiz+216+70, vert+28), (80, 25), "BREADTH", Queen)
        self.label_t = self.createLabel(
            (horiz+283+78, vert+28), (80, 25), "LENGTH", Queen)
        self.textbox_cross = self.createLabel(
            (horiz+203+65, vert+3), (20, 25), "x", Queen)
        self.textbox_cross = self.createLabel(
            (horiz+266+78, vert+3), (20, 25), "x", Queen)
        vert += 75
        self.textlable = self.createLabel(
            (horiz-10, vert), (250, 30), "Quantity Required :", Bebas)
        self.textbox_req = self.createTextBox((horiz+240, vert+3), (75, 25))
        self.textbox_req.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp("[\d]{,6}")))
        buttonCSS = "color: #000;border: 2px solid #555;border-radius: 5px;padding: 5px;min-width: 80px;background-color: rgb(255, 255,255);"
        self.addButton = self.createButton("ADD", (horiz+345, vert), (40, 30), self.addData,
                                           "color: #000;border: 2px solid #555;border-radius: 5px;padding: 5px;min-width: 40px;background-color: rgb(255, 255,255);")

        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setStyle(QtGui.QStyleFactory.create("cleanlooks"))
        self.table.setHorizontalHeaderLabels(
            ["Thickness", "Breadth", "Length", "Quantity"])
        self.table.setItemDelegate(ValidatedItemDelegate())
        self.table.resize(344, 160)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.move(horiz+22, vert+70)

        [self.table.setColumnWidth(x, 86) for x in xrange(4)]

        vert += 250

        self.okbutton = self.createButton(
            "Generate", (horiz+145, vert+10), (60, 30), lambda: self.genPDF(inData, isPrint), css=buttonCSS)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(QtGui.QSizeGrip(self), 0,
                         QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.exitButton = self.createButton(
            "", (410, 21), (15, 15), self.closeUI, "background-color:  rgb(239,239,239)")
        self.exitButton.setIcon(QtGui.QIcon("Images/57165-cross-sign.png"))
        self.exitButton.setIconSize(QtCore.QSize(19, 19))
        self.exitButton.setFlat(True)

        self.setMinimumSize(480, vert+75)
        self.setMaximumSize(480, vert+75)

    def addData(self):
        rowCount = self.table.rowCount()
        self.table.setRowCount(rowCount+1)
        self.table.resize(368, 180)
        self.table.move(58, 230)
        for k, i in enumerate([self.textbox_t.text(), self.textbox_b.text(), self.textbox_l.text(), self.textbox_req.text()]):
            self.table.setItem(rowCount, k, QtGui.QTableWidgetItem(i))
        [self.table.setRowHeight(x, 28) for x in xrange(rowCount+1)]
        self.table.scrollToBottom()

    def closeUI(self):
        self.close()

    def createTextBox(self, pos, size, texte="", key="", data=[]):
        textBox = QtGui.QLineEdit(self)

        if key == "comp":
            completer = CustomQCompleter()
            textBox.setCompleter(completer)
            model = QStringListModel()
            completer.setModel(model)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
            model.setStringList(data)

        textBox.resize(size[0], size[1])
        textBox.move(pos[0], pos[1])
        textBox.setText(texte)
        return textBox

    def createLabel(self, pos, size, data, font):
        label = QtGui.QLabel(data, self)
        label.resize(size[0], size[1])
        label.setFont(font)
        label.move(pos[0], pos[1])
        return label

    def createButton(self, text, pos, size, function, css=""):
        Button = QtGui.QPushButton(text, self)  # Define button
        # Position the button
        Button.move(pos[0], pos[1])
        Button.clicked.connect(function)
        Button.resize(size[0], size[1])
        Button.setStyleSheet(css)
        return Button

    def genPDF(self, inData, isPrint):
        model = self.table.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                # We suppose data are strings
                data[row].append(int(model.data(index)))

        inData['Required Quantity'] = data

        # print inData

        outPath = QtGui.QFileDialog.getSaveFileName(
            self, 'Save Pdf', '', "PDF files (*.pdf)")
        if createPDF(outPath[0], getData(inData), isPrint, inData['Rate'], inData['Transportation'], TransVal=inData['TransportationCost']):
            self.msgbox = MsgBox(self.basecolor, "PDF  Successfully  Saved")
            self.msgbox.show()
            self.close()
        else:
            self.msgbox = MsgBox(self.basecolor, "     PDF  Saving  Failed")
            self.msgbox.show()
            self.close()

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

    def center(self):      # Initialize the window at the centre of the screen
        # Get the position rectangle around our window
        qr = self.frameGeometry()
        # Get the screen size of the desktop and find its centre
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        # Move the position rectangle around our window to the center calculated
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):      # In the event that a key is pressed
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:   # If key pressed is Excape Key
            self.closeP()


class MsgBox(QtGui.QWidget):
    """ Form to display messages """
    def __init__(self, color, text, parent=None):
        super(MsgBox, self).__init__(parent)
        horiz = 44
        vert = 55

        # fonts
        QtGui.QFontDatabase.addApplicationFont('Fonts/Queen of Camelot.ttf')
        Queen = QtGui.QFont("Queen of Camelot", 11)
        QtGui.QFontDatabase.addApplicationFont('Fonts/BebasNeue.ttf')
        Bebas = QtGui.QFont("BebasNeue", 13)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.backgroundColor = hex2QColor(color)
        self.foregroundColor = hex2QColor("333333")
        self.borderRadius = 10
        self.draggable = True
        self.dragging_threshould = 5
        self.__mousePressPos = None
        self.__mouseMovePos = None

        self.textlable = self.createLabel(
            (horiz+5, vert-30), (350, 30), text, Queen)
        # buttonCSS="color: #000;border: 2px solid #555;border-radius: 5px;padding: 5px;min-width: 80px;background-color: rgb(255, 255,255);"
        buttonCSS = """color: #333;border: 2px solid #555;border-radius: 11px;padding: 5px;background: qradialgradient(cx: 0.3, cy: -0.4,
        fx: 0.3, fy: -0.4,radius: 1.35, stop: 0 #fff, stop: 1 #888);min-width: 80px;"""

        self.okbutton = self.createButton(
            "OK", (horiz+83, vert+8), (60, 30), self.closeP, css=buttonCSS)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(QtGui.QSizeGrip(self), 0,
                         QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.setMinimumSize(350, 120)
        self.setMaximumSize(350, 120)

    def createLabel(self, pos, size, data, font):
        label = QtGui.QLabel(data, self)
        label.resize(size[0], size[1])
        label.setFont(font)
        label.move(pos[0], pos[1])
        return label

    def createButton(self, text, pos, size, function, css=""):
        Button = QtGui.QPushButton(text, self)  # Define button
        # Position the button
        Button.move(pos[0], pos[1])
        Button.clicked.connect(function)
        Button.resize(size[0], size[1])
        Button.setStyleSheet(css)
        return Button

    def closeP(self):
        self.close()

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

    def center(self):      # Initialize the window at the centre of the screen
        # Get the position rectangle around our window
        qr = self.frameGeometry()
        # Get the screen size of the desktop and find its centre
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        # Move the position rectangle around our window to the center calculated
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):      # In the event that a key is pressed
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:   # If key pressed is Excape Key
            self.closeP()


class ValidatedItemDelegate(QtGui.QStyledItemDelegate):
    def createEditor(self, widget, option, index):
        if not index.isValid():
            return 0
        if index.column() == 0:  # only on the cells in the first column
            editor = QtGui.QLineEdit(widget)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp("[\d]{,6}"), editor)
            editor.setValidator(validator)
            return editor
        return super(ValidatedItemDelegate, self).createEditor(widget, option, index)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    startPage = FormOne()
    startPage.show()
    app.exec_()
