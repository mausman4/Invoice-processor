import easygui as gui
import yagmail
from pdf2image import convert_from_path
from pdf2image.exceptions import(
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from scan_to_ocr import stt
from cost_breakdown import scrape
from PIL import Image
from datetime import date

def convert_pdf_to_image(aPATH, oPATH):
    images = convert_from_path(aPATH, output_folder=oPATH)
    return images

#ask for email login
yag = yagmail.SMTP(input('Email: '), input('Password: '))

today = date.today()
date_today = today.strftime("%B %d %Y")

pdf_PATH = gui.fileopenbox()

image = convert_pdf_to_image(pdf_PATH, 'Output_PIL')

if (len(image) == 0):
    print('An error has occured, please try again')
elif(len(image) == 1):
    image[0].save('invoice_page_0.jpg', 'JPEG')
else:
    for i in range(len(image)):
        image[i].save('invoice'+ str(i) +'.jpg', 'JPEG')

#will substitute actual path here, this is just for my local working directory
invoice = stt('/Users/danielwang/Documents/School/Yagmail/invoice_page_0.jpg')



#Find the invoice number
invc_num_pos = invoice.find('Invoice # : ')
invc_num_start = invc_num_pos + 12
invc_num_end_pos = invoice[invc_num_pos:].find('\n')
invc_num = invoice[invc_num_start: invc_num_pos + invc_num_end_pos]

#find sold to 
#if sold to == No customer, can skip finding the company name
#also will need a different email template

sld_pos = invoice.find('Sold To')
sld_start = sld_pos + 10
sld_end_pos = invoice[sld_pos:].find('Station')
sld = invoice[sld_start: sld_pos + sld_end_pos - 1]


if (sld == "No Cust"):
    
    sub_cost, gst_cost, pst_cost, total_cost = scrape(invoice)
    
    contents = [
         "Hi,\n\n\tPlease see the attached file for invoice #: " + invc_num + ", dated: " + date_today + 
        "\n\n\tSubtotal: " + "{:.2f}".format(sub_cost) +"\nGST: " + "{:.2f}".format(gst_cost) +
        "\nPST: " + "{:.2f}".format(pst_cost) + "\nThe total cost is: " + "{:.2f}".format(total_cost) + "\n\nBest regards,\n\tDaniel", pdf_PATH
    ]
    
else:
    #Find the company name
    cmp_pos = invoice.find('COMPANY NAME : ')
    cmp_start = cmp_pos + 15
    cmp_end_pos = invoice[cmp_pos:].find('Date/Time : ')
    cmp_name = invoice[cmp_start:cmp_pos + cmp_end_pos]

    sub_cost, gst_cost, pst_cost, total_cost = scrape(invoice)

    contents = [
        "Hi " + cmp_name + ",\n\n\tPlease see the attached file for invoice #: " + invc_num + ", dated: " + date_today + 
        "\n\n\tSubtotal: " + "{:.2f}".format(sub_cost) +"\nGST: " + "{:.2f}".format(gst_cost) +
        "\nPST: " + "{:.2f}".format(pst_cost) + "\nThe total cost is: " + "{:.2f}".format(total_cost) + "\n\nBest regards,\n\tDaniel", pdf_PATH
    ]

yag.send(input('Recipent email: '), "Invoice #: " + invc_num + ", " + date_today, contents)
