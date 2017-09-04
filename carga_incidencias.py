from pypxlib import Table
import psycopg2
import datetime

conn = psycopg2.connect("dbname=offset21junio user=openerp password=zentella host=localhost")
cr = conn.cursor()

table = Table("/mnt/servidorconta/ASISTMIL/Incidencias.DB")
tup = []
for i,row in enumerate(table):
    data = [i+1,row.Empleado,row.Fecha,row.Entrada,row.Inicomida,row.Fincomida,row.Salida,row.Horario,row.Retardo,row.Anticipado,row.Comida,row.Extras,row.Total,row.Registros]
    for j in range(0,len(data)):
        if type(data[j]) == datetime.time:
            timeobject = data[j]
            minutos = timeobject.hour*60+timeobject.minute
            data[j] = minutos
    tup.append(data)
args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
cr.execute("truncate table asistmil_incidencias")
cr.execute("insert into asistmil_incidencias(id,empleado,fecha,entrada,inicomida,fincomida,salida,horario,retardo,anticipado,comida,extras,total,registros) values " + args_str)
conn.commit()
conn.close()
