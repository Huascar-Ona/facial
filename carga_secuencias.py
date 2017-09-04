from pypxlib import Table
import psycopg2
import datetime

conn = psycopg2.connect("dbname=offset21junio user=openerp password=zentella host=localhost")
cr = conn.cursor()

table = Table("/mnt/servidorconta/ASISTMIL/Secuencias.DB")
tup = []
for i,row in enumerate(table):
    data = [i+1,row.Clave,row.Domingo,row.Lunes,row.Martes,row.Miercoles,row.Jueves,row.Viernes,row.Sabado,row.Descripcion]
    tup.append(data)
args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
cr.execute("insert into asistmil_secuencias(id,clave,domingo,lunes,martes,miercoles,jueves,viernes,sabado,descripcion) values " + args_str)
conn.commit()
conn.close()
