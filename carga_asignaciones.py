from pypxlib import Table
import psycopg2
import datetime

conn = psycopg2.connect("dbname=offset21junio user=openerp password=zentella host=localhost")
cr = conn.cursor()

table = Table("/mnt/servidorconta/ASISTMIL/Asignacion.DB")
tup = []
for i,row in enumerate(table):
    if not row.Inicio:
        continue
    anio,semana,dia = row.Inicio.isocalendar()
    cr.execute("select * from asistmil_asignaciones where emp=%s and semana=%s and anio=%s", (row.Registro, semana, anio))
    if not cr.fetchall():
        tup.append([i+1, row.Registro, semana, anio, row.Secuencia])
if tup:
    args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s)", x) for x in tup)
    cr.execute("insert into asistmil_asignaciones(id, emp, semana, anio, secuencia) values " + args_str)
    conn.commit()
conn.close()
