from functions import createTextBox,createLine,createBullet
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, A4, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PageSetups import getData



def createPDF(Filename,AllData,prnt,Rate,TransInc,TransVal=0):
    if True:#try:
        horiz=45
        vert=760
        pdfmetrics.registerFont(TTFont('Calibri','Fonts/Calibri.ttf'))
        pdfmetrics.registerFont(TTFont('CalibriBold','Fonts/Calibri Bold.ttf'))
        c = canvas.Canvas(Filename,pagesize=A4)
        c.setTitle("Quotation from Citadel")
        Type=AllData["Type"]
        x=createTextBox(c,"Date: "+AllData["Date"],horiz, vert+5,"0x000000",'Calibri',11)
        x=createTextBox(c,"To,",horiz, x-20,"0x000000",'CalibriBold',11)
        x=createTextBox(c,AllData["Client Name"],horiz, x-4,"0x000000",'CalibriBold',11)
        xt=createTextBox(c,AllData["Client Address"],horiz, x-4,"0x000000",'Calibri',11)
        logo = ImageReader('Images/CitadelLogo.png')
        if prnt:
            c.drawImage(logo, horiz+360, vert-70, width=120,height=80,mask='auto')

        x=createTextBox(c,"Kind Attention: ",horiz, xt-15,"0x00000",'CalibriBold',11)
        xt=createTextBox(c,AllData["Addressed To"],horiz+77, xt-15,"0x000000",'Calibri',11)
        x=createTextBox(c,"Subject: ",horiz, xt-15,"0x000000",'CalibriBold',11)
        x=createTextBox(c,AllData["Subject"],horiz+45, xt-15,"0x000000",'Calibri',11)
        x=createTextBox(c,"Dear Sir/Madam,",horiz, x-15,"0x000000",'Calibri',11)
        data="With reference to the above said subject we are pleased to forward our most competitive rate for your further \napproval."
        x=createTextBox(c,data,horiz, x-11,"0x000000",'Calibri',11)

        t=Table(AllData["Table Data"])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('FONT',(0,0),(-1,0),'CalibriBold',11),
                               ('VALIGN',(0,0),(-1,-1),'BOTTOM'),
                               ('INNERGRID', (0,0), (-1,-1), 1.5, HexColor("0x000000")),
                               ('BOX', (0,0), (-1,-1), 2, HexColor("0x000000")),
                               ('BACKGROUND',(0,0),(-1,0),HexColor("0xadadad")),]))
        t.wrapOn(c, 100, 40)
        if Type=="Blocks":
            t.drawOn(c, horiz+7, x-207)
        elif Type=="Lintel":
            t.drawOn(c, horiz+7, x-185)
            x+=25
        elif Type=="Wall Panels":
            t.drawOn(c, horiz+7, x-200)
        elif Type=="AAC Slabs":
            t.drawOn(c, horiz+7, x-218)
            

        x=createTextBox(c,"The Material shall be supplied on following Terms and Conditions:",horiz, x-242,"0x00000",'CalibriBold',11)
        createLine(c,horiz,x+7,302,1,"0x000000")
        x=createTextBox(c,"1. Validity:",horiz, x-15,"0x00000",'CalibriBold',11)
        x=createBullet(c,"Rate are valid for 15 days from the date of quotation.",horiz+17,x-7,'Calibri',11)
        x=createBullet(c,"The quotation is based on current market prices for the enquiry received.",horiz+17,x-4,'Calibri',11)
        x=createTextBox(c,"2. Taxes:",horiz, x-7,"0x00000",'CalibriBold',11)
        if Type=="Blocks":
            taxstatement=AllData["GST Type"]+" of "+str(AllData["Tax"])+"% (Rs. "+str(round(Rate*float(AllData["Tax"]/float(100)),2))+") and SGST "+str(AllData["Tax"])+"% (Rs. "+str(round(Rate*float(AllData["Tax"]/float(100)),2))+") is extra."
        else:
            taxstatement="GST of "+str(AllData["Tax"]*2)+"% (Rs."+str(round(Rate*float(AllData["Tax"]*2/float(100)),2))+") is extra."
        x=createBullet(c,taxstatement,horiz+17,x-7,'Calibri',11)
        x=createTextBox(c,"2. Freight:",horiz, x-7,"0x00000",'CalibriBold',11)
        x=createBullet(c,"Orders shall be in multiple of full truck loads, Ex- warehouse, Transportation from depot to site as per actual with taxes to your account",horiz+17,x-19,'Calibri',11)
        if TransInc :
            transData="Transportation is included in the given rate."
        elif not TransInc and TransVal>0:   
            transData="Transportation cost is Rs."+str(TransVal) +" which is not included in the given rate."
        else:
            transData="Transportation is extra."

        xt=createBullet(c,".",horiz+17,x-5,'CalibriBold',11,43)
        x=createTextBox(c,transData,horiz+35, x-2,"0x00000",'CalibriBold',11)
        x=createTextBox(c,"4. Delivery:",horiz, x-7,"0x00000",'CalibriBold',11)
        if Type=="Blocks":
            data="Within 7 days from receipt of your confirmed written Purchase Orders. In case of Non standard material it will take 7 days."
        elif Type in ["Lintel","WallPanels"]:
            data="Within 30 days from receipt of your confirmed written Purchase Order and Cheque."
            x+=11
        elif Type=="AACSlabs":
            data="Within 15 days from receipt of your confirmed written Purchase Order and Cheque."
            x+=11
        x=createBullet(c,data,horiz+17,x-19,'Calibri',11)
        x=createBullet(c,"Unloading of material to be arranged by Client, No warai Charges nor Hamal Panchyat Labour would be enternained by us for any Payment.",horiz+17,x-16,'Calibri',11)
        x=createTextBox(c,"5. Special Clause:",horiz, x-7,"0x00000",'CalibriBold',11)
        x=createBullet(c,"Any Purchase orders released by you for time agreed upon ,giving reference to this quotation will automatically acceptable. Imply that all clauses that are mentioned in this quotation are acceptable.",horiz+17,x-19,'Calibri',11)
        c.showPage()

        #Page TWO
        c.drawImage(logo, horiz+195, vert-20, width=100,height=75,mask='auto')
        x=createTextBox(c,"6. Force Majeure:",horiz, vert-40,"0x00000",'CalibriBold',11)
        data="""Buyers will not be entitled to take objection or make any claim, if the manufacture, supply or shipment or transport \
    or delivery of goods is prevented or hindered or delayed or any shortage of material by strike, accident, civil \
    commotion, accident at works, breakdown of machinery, any inevitable or unforeseen event, embargo, restrain of \
    Govt, fraud, fire storms floods, earthquake or any act of God."""
        x=createBullet(c,data,horiz+17,x-43,'Calibri',11)
        x=createTextBox(c,"7. Payment terms:",horiz, x-7,"0x00000",'CalibriBold',11)
        xt=createBullet(c,".",horiz+17,x-7,'CalibriBold',11,91)
        x=createTextBox(c,"The terms of payment shall be 100 % Advance with PO in favor of 'Citadel Eco Build Pvt. Ltd.' .",horiz+35, x-4,"0x00000",'CalibriBold',11)
        x=createBullet(c,"Penal Interest will be at rate of 2% per month would be charged for over due bills .",horiz+17,x-5,'CalibriBold',11)
        x=createTextBox(c,"8. Purchase Order: ",horiz, x-7,"0x00000",'CalibriBold',11)
        x=createBullet(c,'The Purchase order should be in the name of "Citadel Eco Build Pvt Ltd".',horiz+17,x-7,'CalibriBold',11)
        x=createTextBox(c,"9. Others: ",horiz, x-7,"0x00000",'CalibriBold',11)
        x=createBullet(c,'The minimum order quantity should be in our standard packing only for motar Standard packing shall not be broken.',horiz+17,x-19,'CalibriBold',11)
        x=createBullet(c,'All the taxes will be charged as per Government norms any difference in tax rate will be levied @ extra.',horiz+17,x-4,'CalibriBold',11)
        x=createTextBox(c,"10. We need following documents from your side to open your account for the first time dealing.",horiz, x-7,"0x00000",'CalibriBold',11)
        x=createTextBox(c,"1)      TIN registration certificate ",horiz+35, x-5,"0x00000",'Calibri',11)
        x=createTextBox(c,"2)      CST Registration No & certificate ",horiz+35, x-3,"0x00000",'Calibri',11)
        x=createTextBox(c,"3)      Excise registration details for Excise Billing ",horiz+35, x-3,"0x00000",'Calibri',11)
        x=createTextBox(c,"4)      Address proof ",horiz+35, x-3,"0x00000",'Calibri',11)
        x=createTextBox(c,"5)      Account Opening Form ",horiz+35, x-3,"0x00000",'Calibri',11)
        x=createTextBox(c,"We look forward to your valued order and assure you of our best services always.",horiz, x-15,"0x00000",'Calibri',11)
        x=createTextBox(c,"Thanking you",horiz, x-5,"0x00000",'Calibri',11)
        x=createTextBox(c,"Yours sincerely, ",horiz, x-15,"0x00000",'CalibriBold',11)
        x=createTextBox(c,AllData["AgentName"],horiz, x-15,"0x00000",'CalibriBold',11)
        x=createTextBox(c,AllData["AgentPos"],horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"Mobile : "+AllData["AgentPh"],horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"Citadel Eco-build Pvt Ltd",horiz, x-18,"0x00000",'CalibriBold',11)
        x=createTextBox(c,"759/35 Samadhan Apts, Bhandarkar Road",horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"Good Luck Cross, Shivajinagar,",horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"Pune 411004",horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"[Phone] 091 20 25656575",horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"[Fax] 091 20 265289672",horiz, x-4,"0x00000",'Calibri',11)
        x=createTextBox(c,"[Website] http://www.citadelecobuild.com",horiz, x-4,"0x0000ff",'Calibri',11)
        c.save()
        return True
    # except:
    #     return False


# inputDATA=[["Output/Citadel_AACSlabs.pdf","AACSLABS"],["Output/Citadel_Wallpanels.pdf","WALLPANELS"],
#         ["Output/Citadel_Lintel.pdf","LINTEL"],["Output/Citadel_Blocks.pdf","BLOCKS"]]
   
# for Filename,typ in inputDATA:
#     rateBlocks=4100
#     createPDF(45,760,getData(rateBlocks,typ),prnt=True,Rate=4100,TransInc=False,TransVal=800)
#     