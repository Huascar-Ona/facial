# -*- coding: utf-8 -*-
#Actualización de la tabla Inciden, debe correrse cada día, actualiza todo lo del mes en curso (en realidad, ventana de 31 días)
import psycopg2
from conf import get_conf

conn, cr, path = get_conf() 

#Los que ya están procesados guardarlos para que no se pierda el registro
cr.execute("select empleado,fecha,tipo,tiempo from asistmil_inciden where age(fecha) <= interval '31 days' and  process='t'")
procesados = []
for row in cr.fetchall():
    procesados.append(row)
    print row[0], row[1].strftime("%Y-%m-%d"), row[2], row[3]
print "Con palomita del mes:", len(procesados)

#Borrar los registros del mes
print "Borrando todo lo del mes..."
cr.execute("delete from asistmil_inciden where age(fecha) <= interval '31 days'")

#Son registros incompletos todos los que su campo horario empiecen con un dígito, y les corresponde el tipo 0355
cr.execute("""insert into asistmil_inciden(empleado,fecha,tipo,secuencia)
              select empleado,fecha,'0355',0
              from asistmil_incidencias
              where substring(horario from 1 for 1) in ('1','2','3','4','5','6','7','8','9')
              and registros=1
              and age(fecha) <= interval '31 days'
              and fecha <= now()""")

#Los registros de la tabla Autorizaciones entran con Tipo igual a la clave del justificante
cr.execute("""insert into asistmil_inciden(empleado,fecha,tipo,tiempo,secuencia)
              select empleado,fecha,lpad(justificante::text, 4, '0'),0,0
              from asistmil_autorizaciones
              where age(fecha) <= interval '31 days'
              and fecha <= now()""")

#Los retardos tienen tipo 0599 y se guarda el tiempo
cr.execute("""insert into asistmil_inciden(empleado,fecha,tipo,tiempo,secuencia)
              select empleado,fecha,'0599',retardo,0
              from asistmil_incidencias
              where retardo is not null 
              and age(fecha) <= interval '31 days'
              and fecha <= now()""")

#Los anticipados tienen tipo 0600 y se guarda el tiempo
cr.execute("""insert into asistmil_inciden(empleado,fecha,tipo,tiempo,secuencia)
              select empleado,fecha,'0600',anticipado,0
              from asistmil_incidencias
              where anticipado is not null 
              and age(fecha) <= interval '31 days'
              and fecha <= now()""")

#Las horas extras entran con tipo 0699, son los que tienen el valor TIEMPO EXTRA en el campo horario y se guarda el tiempo
cr.execute("""insert into asistmil_inciden(empleado,fecha,tipo,tiempo,secuencia)
              select empleado,fecha,'0699',extras,0
              from asistmil_incidencias
              where horario = 'TIEMPO EXTRA'
              and extras is not null
              and age(fecha) <= interval '31 days'
              and fecha <= now()""")

#Las faltas entran con tipo 0000 y son las que el horario sea FALTA
cr.execute("""insert into asistmil_inciden(empleado,fecha,tipo,tiempo,secuencia)
              select empleado,fecha,'0000',0,0
              from asistmil_incidencias
              where horario = 'FALTA'
              and age(fecha) <= interval '31 days'
              and fecha <= now()""")

#Borrar los que tengan falta (0000) y la fecha sea menor a la fecha de alta del empleado o sea un día marcado como vacaciones
cr.execute("""delete from asistmil_inciden t1
              using hr_employee t2
              where t1.empleado=t2.cod_emp
              and (t1.fecha < t2.fecha_alta or t1.fecha in (select fe_asueto from hr_caleasue))""")

print "Volviendo a poner palomita de aplicado a los ya aplicados"
for row in procesados:
    cr.execute("update asistmil_inciden set process='t' where empleado=%s and fecha=%s and tipo=%s and tiempo=%s", row)
cr.execute("select count(*) from asistmil_inciden where process='t' and age(fecha) <= interval '31 days'")
print "Con palomita del mes después de la actualización",  cr.fetchone()[0]

conn.commit()
conn.close()
