# -*- coding: utf-8 -*-
from pypxlib import Table
import psycopg2
import datetime
from conf import get_conf

conn, cr, tpath = get_conf()

print "Justificantes"
table = Table(tpath + "Justificantes.DB")
tup = []
cr.execute("select count(*) from asistmil_justificantes")
if cr.fetchone()[0] == 0:
    for i,row in enumerate(table):
        data = [i+1,row.Clave,row.Descripcion,row.Tiempo,row.Dia,row.Entrada,row.Salida]
        tup.append(data)
    if tup:
        args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
        cr.execute("insert into asistmil_justificantes(id,clave,descripcion,tiempo,dia,entrada,salida) values " + args_str)
else:
    print "hay datos"
    for i,row in enumerate(table):
        print "Clave %s?"%row.Clave,
        cr.execute("select count(*) from asistmil_justificantes where clave=%s", (row.Clave,))
        if cr.fetchone()[0] == 0:
            print "no, insertando"
            cr.execute("insert into asistmil_justificantes(clave,descripcion,tiempo,dia,entrada,salida) values (%s,%s,%s,%s,%s,%s)",
                (row.Clave,row.Descripcion,row.Tiempo,row.Dia,row.Entrada,row.Salida))
        else:
            print "sí"

conn.commit()
conn.close()
