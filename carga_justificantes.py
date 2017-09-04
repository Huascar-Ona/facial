from pypxlib import Table
import psycopg2
import datetime

conn = psycopg2.connect("dbname=offset21junio user=openerp password=zentella host=localhost")
cr = conn.cursor()

table = Table("/mnt/servidorconta/ASISTMIL/Justificantes.DB")
tup = []
for i,row in enumerate(table):
    data = [i+1,row.Clave,row.Descripcion,row.Tiempo,row.Dia,row.Entrada,row.Salida]
    tup.append(data)
args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
cr.execute("insert into asistmil_justificantes(id,clave,descripcion,tiempo,dia,entrada,salida) values " + args_str)
conn.commit()
conn.close()
