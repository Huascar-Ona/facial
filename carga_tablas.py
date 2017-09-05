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

print "Secuencias"
table = Table(tpath + "Secuencias.DB")
tup = []
cr.execute("select count(*) from asistmil_secuencias")
if cr.fetchone()[0] == 0:
    for i,row in enumerate(table):
        data = [i+1,row.Clave,row.Domingo,row.Lunes,row.Martes,row.Miercoles,row.Jueves,row.Viernes,row.Sabado,row.Descripcion]
        tup.append(data)
    if tup:
        args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
        cr.execute("insert into asistmil_secuencias(id,clave,domingo,lunes,martes,miercoles,jueves,viernes,sabado,descripcion) values " + args_str)

print "Asignacion"
table = Table(tpath + "Asignacion.DB")
tup = []
for i,row in enumerate(table):
    if not row.Inicio:
        continue
    anio,semana,dia = row.Inicio.isocalendar()
    cr.execute("select * from asistmil_asignaciones where emp=%s and semana=%s and anio=%s", (row.Registro, semana, anio))
    if not cr.fetchall():
        tup.append([row.Registro, semana, anio, row.Secuencia])
if tup:
    args_str = ','.join(cr.mogrify("(%s,%s,%s,%s)", x) for x in tup)
    cr.execute("insert into asistmil_asignaciones(emp, semana, anio, secuencia) values " + args_str)

print "Autorizaciones"
table = Table(tpath + "Autorizaciones.DB")
tup = []
for i,row in enumerate(table):
    data = [i+1,row.Empleado,row.Fecha,row.Justificante,row.Folio]
    tup.append(data)
if tup:
    args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s)", x) for x in tup)
    cr.execute("truncate table asistmil_autorizaciones")
    cr.execute("insert into asistmil_autorizaciones(id,empleado,fecha,justificante,folio) values " + args_str)

print "Incidencias"
table = Table(tpath + "Incidencias.DB")
tup = []
for i,row in enumerate(table):
    data = [i+1,row.Empleado,row.Fecha,row.Entrada,row.Inicomida,row.Fincomida,row.Salida,row.Horario,row.Retardo,row.Anticipado,row.Comida,row.Extras,row.Total,row.Registros]
    for j in range(0,len(data)):
        if type(data[j]) == datetime.time:
            timeobject = data[j]
            minutos = timeobject.hour*60+timeobject.minute
            data[j] = minutos
    tup.append(data)
if tup:
    args_str = ','.join(cr.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
    cr.execute("truncate table asistmil_incidencias")
    cr.execute("insert into asistmil_incidencias(id,empleado,fecha,entrada,inicomida,fincomida,salida,horario,retardo,anticipado,comida,extras,total,registros) values " + args_str)

conn.commit()
conn.close()
