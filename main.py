import easygui as gui
import yagmail
from pdf2image import convert_from_path
from pdf2image.exceptions import(
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from scan_to_ocr import stt
from PIL import Image
from datetime import date

def convert_pdf_to_image(aPATH, oPATH):
    images = convert_from_path(aPATH, output_folder=oPATH)
    return images

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

#Find the company name
cmp_pos = invoice.find('COMPANY NAME : ')
cmp_start = cmp_pos + 15
cmp_end_pos = invoice[cmp_pos:].find('Date/Time : ')
cmp_name = invoice[cmp_start:cmp_pos + cmp_end_pos]

#Find the subtotal
subtotal_pos = invoice.find('SUBTOTAL: ')
subtotal_start = subtotal_pos + 10
subtotal_end_pos = invoice[subtotal_pos:].find('\n')
subtotal_cost = float(invoice[subtotal_start: subtotal_pos + subtotal_end_pos])

#Find the GST
gst_pos = invoice[subtotal_pos + subtotal_end_pos + 1:].find('GST: ') + subtotal_pos + subtotal_end_pos + 1
gst_start = gst_pos + 5
gst_end_pos = invoice[gst_pos:].find('\n')
gst_cost = float(invoice[gst_start: gst_pos + gst_end_pos])

#Find the PST
pst_pos = invoice[gst_pos + gst_end_pos + 1:].find('PST: ') + gst_pos + gst_end_pos + 1
pst_start = pst_pos + 5
pst_end_pos = invoice[pst_pos:].find('\n')
pst_cost = float(invoice[pst_start: pst_pos + pst_end_pos])

#Find the Total
total_pos = invoice[pst_pos + pst_end_pos + 1:].find("TOTAL: ") + pst_pos + pst_end_pos + 1
total_start = total_pos + 7
total_end_pos = invoice[total_pos:].find("\n")
total_cost=float(invoice[total_start: total_pos + total_end_pos])

today = date.today()
date_today = today.strftime("%B %d %Y")
yag = yagmail.SMTP(input('Email: '), input('Password: '))
contents = [
    "Hi " + cmp_name + ",\n\n\tPlease see the attached file for invoice #: " + invc_num + ", dated: " + date_today + 
    "\n\tSubtotal: " + str(subtotal_cost) +"\nGST: " + str(gst_cost) +
    "\nPST: " + str(pst_cost) + "\nThe total cost is: " + str(total_cost) + "\n\nBest regards,\n\tDaniel", pdf_PATH
]

yag.send(input('Recipent email: '), "Invoice #: " + invc_num + ", " + date_today, contents)

