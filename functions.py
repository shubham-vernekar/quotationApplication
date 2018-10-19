from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.graphics import shapes, renderPDF
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus import ListFlowable, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def createBullet(c, text, x, y, font, size, indent=0):
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    if indent != 0:
        t = ListFlowable([Paragraph(text, style)], bulletType='bullet', start='circle', leftIndent=indent,
                         fontName=font, bulletFontName="Helvetica", bulletFontSize=8, bulletAnchor="Start")
    else:
        t = ListFlowable([Paragraph(text, style)], bulletType='bullet', start='circle',
                         fontName=font, bulletFontName="Helvetica", bulletFontSize=8, bulletAnchor="Start")
    t.wrapOn(c, 480, 20)
    t.drawOn(c, x, y)
    return y-size


def pad(key, size):
    if len(key) >= size:
        return key
    else:
        return key+" "*(size-len(key))


def createLine(c, x, y, width, size, color):
    c.setLineWidth(size)
    c.setStrokeColor((HexColor(color)))
    c.line(x, y, x+width, y)


def drawTable(c, x, y, data, Textcolor, fontSize, dx=0.6, total=True):
    pading = [max([len(el[index]) for el in data])
              for index in xrange(len(data[0]))]
    pading = [pading[index]+8 if index ==
              0 else pading[index]+4 for index in xrange(len(pading))]

    createLine(c, x-5, y+13, sum(pading)*fontSize*dx, 2, "0xff8100")
    for m, rec in enumerate(data):
        temp = x
        if m == 0 or (m >= len(data)-2 and total):
            linewidth = 2
        else:
            linewidth = 1

        createLine(c, x-5, y-10, sum(pading) *
                   fontSize*dx, linewidth, "0xff8100")
        for k, word in enumerate(rec):
            if m == 0 or (m == len(data)-1 and total):
                _ = createTextBox(c, word, x, y, Textcolor,
                                  "MavenProBlack", fontSize)
            else:
                _ = createTextBox(c, word, x, y, Textcolor,
                                  "MavenPro", fontSize)

            x += pading[k]*fontSize*dx
        y -= fontSize+15
        x = temp
    return y


def createTextBox(canvas, data, horiz, vert, color, font, size):
    textobject = canvas.beginText()
    textobject.setTextOrigin(horiz, vert)
    textobject.setFont(font, size)
    textobject.setFillColor(HexColor(color))
    for line in data.split("\n"):
        vert -= size
        textobject.textLine(line)

    canvas.drawText(textobject)
    return vert


def createBarGraph(c, x, y, data, labels, colors, barnames, minvalue, maxvalue, step, h=75, w=300, dy=0):
    drawing = Drawing(400, 200)
    legend = Legend()

    legend.columnMaximum = 99
    legend.alignment = 'right'
    legend.dx = 7
    legend.dy = 7
    legend.dxTextSpace = 5
    legend.deltay = 10
    legend.strokeWidth = 0
    legend.strokeColor = HexColor("0xffffff")
    legend.subCols[0].minWidth = 75
    legend.subCols[0].align = 'left'
    legend.boxAnchor = 'c'
    legend.y = h+25
    legend.x = w+110
    legend.fontName = "MavenPro"
    legend.fontSize = 8.5
    legendList = []
    for k, i in enumerate(colors):
        legendList.append((HexColor(i), barnames[k]))

    legend.colorNamePairs = legendList

    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = h  # 75
    bc.width = w  # 300
    bc.data = data
    bc.bars.strokeColor = HexColor("0xffffff")
    bc.valueAxis.labels.fontName = "MavenPro"
    bc.valueAxis.labels.fontSize = 8
    bc.valueAxis.labels.dx = -10
    bc.valueAxis.valueMin = minvalue
    bc.valueAxis.valueMax = maxvalue
    bc.valueAxis.valueStep = step
    bc.categoryAxis.labels.boxAnchor = 'n'
    bc.categoryAxis.labels.dx = 0
    bc.categoryAxis.labels.dy = -10-dy
    bc.categoryAxis.labels.angle = 0
    bc.categoryAxis.labels.fontName = "MavenPro"
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.categoryNames = labels
    for k in xrange(len(colors)):
        bc.bars[k].fillColor = HexColor(colors[k])
        #self.chart.bars[k].fillColor   = HexColor(colors[k])

    drawing.add(bc)
    drawing.add(legend, 'legend')
    drawing.drawOn(c, x, y)


def getPieChart(c, x, y, data, data_suff, labels, colors, fsize=8.5, radius=0.60, legdx=180, legdy=100):
    d = Drawing(200, 200)
    legend = Legend()
    legend.columnMaximum = 99
    legend.alignment = 'right'
    legend.dx = 7
    legend.dy = 7
    legend.dxTextSpace = 5
    legend.deltay = 10
    legend.strokeWidth = 0
    legend.strokeColor = HexColor("0xffffff")
    legend.subCols[0].minWidth = 75
    legend.subCols[0].align = 'left'
    legend.boxAnchor = 'c'
    legend.y = legdy
    legend.x = legdx
    legend.fontName = "MavenPro"
    legend.fontSize = 8.5
    legendList = []
    for k, i in enumerate(colors):
        legendList.append((HexColor(i), labels[k]))

    # [(HexColor(colors[0]), ('BP')), (HexColor(colors[1]), ('BT'))]
    legend.colorNamePairs = legendList

    pc3 = Pie()
    pc3.x = 10
    pc3.y = 10
    pc3.data = data
    pc3.labels = [str(r)+data_suff if r >= 15 else "" for r in data]
    pc3.slices.strokeColor = HexColor("0xffffff")
    pc3.slices.labelRadius = radius
    pc3.slices.fontName = "MavenPro"
    pc3.slices.fontSize = fsize
    pc3.slices.fontColor = HexColor("0xffffff")
    for k, i in enumerate(colors):
        pc3.slices[k].fillColor = HexColor(i)
    d.add(pc3, 'pie3')
    d.add(legend, 'legend')
    d.drawOn(c, x, y)


def getrange(data, step):
    mx = max([max(rec) for rec in data])
    mn = min([min(rec) for rec in data])
    maxRet = minRet = 0
    while True:
        maxRet += step
        if maxRet > mx:
            break
    if mn >= 0:
        return 0, maxRet
    while True:
        minRet -= step
        if minRet < mn:
            break
    return minRet, maxRet


def cstr(value):
    return "{:,}".format(value)
