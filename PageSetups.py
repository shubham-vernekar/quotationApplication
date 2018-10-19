def ceil(key):
    if key%1==0:
        return int(key)
    else:
        return int(key-key%1+1)


def getCost(dat,rateBlocks,key="Lintel"):
    x=dat[:]

    if key=="Lintel":
        edges=[s*100 for s in [5,6,7,10,11,12,15,16,17,20,21,22,25]]
    else:
        edges=[s*100 for s in [10,11,12,15,16,17,20,21,22,25,26,27,30,31,32,35,36,37,40]]
    for i in edges:
        if i>=x[2]:
            x[2]=i
            break

    vol=x[0]*600*x[2]/float(1000000000)
    return vol*rateBlocks#*x[3]

def getData(inData):
    rateBlocks=inData['Rate']
    types=inData['Type']
    rqdata=inData['Required Quantity']

    if types=="Blocks":
        # BLOCKS
        tax=6
        blksize=[int(x) for x in inData['Block Size'].split(" x ")]
        trucksize=float(inData['Truck Size'][:-4])
        tabledata=[["Sr.No.","Size of AAC Blocks"," Volume of \n Block (in \n Cum) "," Rate per \n Cum ","Rate per Pc","Rate per Sq.ft"," Qty per \n Truck Load \n (in nos.) "]]
        blks=["075","100","125","150","200","225","250","300"]
        for k,i in enumerate(blks):
            vol=int(i)*blksize[0]*blksize[1]/float(1000000000)
            ratePerBlock=vol*rateBlocks
            volSqFeet=blksize[0]*blksize[1]*10.76/float(1000000)
            tabledata.append ([str(k),"   "+i+" x "+str(blksize[0])+" x "+str(blksize[1])+" mm   ",str(round(vol,4)), str(rateBlocks),str(round(ratePerBlock,2)),str(round(ratePerBlock/volSqFeet,2)),str(ceil(trucksize/vol))])
        subject='Quotation for ISI Grade no. 1. "Biltech" Light Weight Aerated Autoclaved Concrete Blocks'

    elif types=="AAC Slabs":
        tax=14
        total=0
        tabledata=[["Sr.No.", "Size of AAC Slabs", "Rate per Pc", "Required\nQuantity\n(Nos)", "Total"]]
        for k,i in enumerate(rqdata):
            vol=i[0]*i[1]*i[2]/float(1000000000)
            ratePerBlock=getCost(i,rateBlocks)
            cost=ratePerBlock*i[3]
            total+=cost
            tabledata.append([str(k)," X ".join(map(str,i[:-1]))+" mm",str(round(ratePerBlock,2)),str(i[3]),str(round(cost,2))])
        tabledata.append([" ", " "," ","Grand Total", str(round(total,2))])
        subject='Quotation for Pre-Fab Reinforced AAC Slabs'

    elif types=="Lintel":
        tax=14
        total=0
        tabledata=[["Sr.No.", "Size of AAC Lintels", "Rate per Pc (Rs.)", "Required\nQuantity", "Total\n(Rs.)"]]
        for k,i in enumerate(rqdata):
            vol=i[0]*i[1]*i[2]/float(1000000000)
            ratePerBlock=getCost(i,rateBlocks)
            cost=ratePerBlock*i[3]
            total+=cost
            tabledata.append([str(k)," X ".join(map(str,i[:-1]))+" mm",str(round(ratePerBlock,2)),str(i[3]),str(round(cost,2))])
        tabledata.append([" ", " "," ","Grand Total", str(round(total,2))])
        subject='Quotation for Pre-Fab Reinforced AAC Lintels'
    
    elif types=="Wall Panels":
        tax=14
        total=0
        tabledata=[["Sr.No.", "Size of AAC Wall Panels", "Rate per Pc", "Required\nQuantity", "Total"]]
        for k,i in enumerate(rqdata):
            vol=i[0]*i[1]*i[2]/float(1000000000)
            ratePerBlock=getCost(i,rateBlocks)
            cost=ratePerBlock*i[3]
            total+=cost
            tabledata.append([str(k)," X ".join(map(str,i[:-1]))+" mm",str(round(ratePerBlock,2)),str(i[3]),str(round(cost,2))])
        tabledata.append([" ", " "," ","Grand Total", str(round(total,2))])
        subject='Quotation for Pre-Fab Reinforced AAC Wall Panles'

    return {"Type":types,"Date":inData['Date'],"Client Name":inData['Client Name'],"Client Address":inData['Client Address'],
    "Addressed To":inData['Addressed To'],"Subject":subject,'Table Data':tabledata,"AgentName":inData['AgentName'],
    "AgentPos":inData['AgentPos'],"AgentPh":inData['AgentPh'],"GST Type":inData['GST Type'],"Tax":tax}


# inData={'Client Name': u'gh', 'Transportation': True, 'Client Address': u'kjg', 'Type': u'AAC Slabs', 'GST Type': u'CGST', 'TransportationCost': 0, 'AgentPos': u'kgh', 'Rate': 22000, 'Addressed To': u'jhg', 'AgentName': u'kjhg', 'Date': u'30.07.2017', 'Required Quantity': [[150, 600, 2300, 40], [150, 600, 2000, 40]], 'AgentPh': u'464654654'}
# for i in getData(inData)["Table Data"]:
#     print i
# getData(inData)
# blksize=[250,625]
# rateBlocks=4100
# trucksize=25
# print ceil(trucksize/(75*blksize[0]*blksize[1]/float(1000000000)))
#print str(round((75*blksize[0]*blksize[1]*rateBlocks/float(1000000000))/(blksize[0]*blksize[1]/float(1000000)*10.76),2))