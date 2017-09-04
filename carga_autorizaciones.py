from pypxlib import Table
import psycopg2
import datetime

conn = psycopg2.connect("dbname=offset21junio user=openerp password=zentella host=localhost")
cr = conn.cursor()

table = Table("/mnt/servidorconta/ASISTMIL/Autorizaciones.DB")
tup = []
for i,row in enumerate(table):
    data = [i+1,row.Empleado,row.Fecha,row.Justificante,row.Folio]
    tup.append(data)
args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s)", x) for x in tup)
cr.execute("truncate table asistmil_autorizaciones")
cr.execute("insert into asistmil_autorizaciones(id,empleado,fecha,justificante,folio) values " + args_str)
conn.commit()
conn.close()
