def scrape(invoice):
    #Find the subtotal
    sub_pos = invoice.find('SUBTOTAL: ')
    sub_start = sub_pos + 10
    sub_end_pos = invoice[sub_pos:].find('\n')
    sub_cost = float(invoice[sub_start: sub_pos + sub_end_pos])

    #Find the GST
    gst_pos = invoice[sub_pos + sub_end_pos + 1:].find('GST: ') + sub_pos + sub_end_pos + 1
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
    
    return sub_cost, gst_cost, pst_cost, total_cost