from database import con


class Order:

    is_exist = False

    def __init__(self, id_doc):
        self.id_doc = id_doc

    def select_from_db(self, select):
        try:
            cur = con.cursor()
            query = select.format(iddoc=self.id_doc)
            cur.execute(query)
            result = cur.fetchone()
            if result:
                # print(cur.description)
                # For each element in the result, we set the object's attribute.
                for index, column in enumerate(cur.description):
                    setattr(self, column[0], result[index])
                self.is_exist = True
            cur.close()
        except TypeError as e:
            print(e)


sel_ord_inf = '''select z.id_doc, z.depno, z.docnum, z.dog_no, z.docdate, z.findate, z.adres_dest, z.userdata1 dt_entry, z.userdata2 dt_product,
    z.userdata3 dt_delivery, z.is_fact, z.syma, ss_cont.name order_contours, ss_ms.name order_ms,
    ss_windowsill.name order_windowsills, ss_otliv.name order_otlivs, trans.id_doc id_trans,
    trans.docdate trans_date, ss_driver.name driver, ss_car.name car
    from doc_acc_zag z
        left join doc_dates dd_cont on dd_cont.id_doc = z.id_doc and dd_cont.vid = 1 and dd_cont.vid_field = 1
        left join spr_service ss_cont on ss_cont.vid = 1001 and ss_cont.id = dd_cont.fint
        left join doc_dates dd_ms on dd_ms.id_doc = z.id_doc and dd_ms.vid = 1 and dd_ms.vid_field = 2
        left join spr_service ss_ms on ss_ms.vid = 1002 and ss_ms.id = dd_ms.fint
        left join doc_dates dd_windowsill on dd_windowsill.id_doc = z.id_doc and dd_windowsill.vid = 1 and dd_windowsill.vid_field = 3
        left join spr_service ss_windowsill on ss_windowsill.vid = 1003 and ss_windowsill.id = dd_windowsill.fint
        left join doc_dates dd_otliv on dd_otliv.id_doc = z.id_doc and dd_otliv.vid = 1 and dd_otliv.vid_field = 4
        left join spr_service ss_otliv on ss_otliv.vid = 1004 and ss_otliv.id = dd_otliv.fint
        left join doc_acc_comps comps on comps.id_doc = z.id_doc and comps.vid_obj = 0 and comps.trans_obj = 1
        left join doc_trans_zag trans on trans.id_doc = comps.id_trans
        left join spr_service ss_driver on ss_driver.vid = 4 and ss_driver.id = trans.id_brig
        left join spr_service ss_car on ss_car.vid = 24 and ss_car.id = trans.id_car
    where z.id_doc = {iddoc}'''
