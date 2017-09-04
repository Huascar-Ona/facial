from pypxlib import Table
from datetime import datetime
import sys

fecha_inicio = datetime.strptime(sys.argv[1], "%Y-%m-%d") 
fecha_fin = datetime.strptime(sys.argv[2], "%Y-%m-%d") 

table = Table("/mnt/servidorconta/ASISTMIL/Incidencias.DB")
faltas = []
for i,row in enumerate(table):
    #data = [i+1,row.Empleado,row.Fecha,row.Entrada,row.Inicomida,row.Fincomida,row.Salida,row.Horario,row.Retardo,row.Anticipado,row.Comida,row.Extras,row.Total,row.Registros]
    fecha = datetime(row.Fecha.year, row.Fecha.month, row.Fecha.day)
    if fecha_inicio <= fecha <= fecha_fin:
        if row.Horario == 'FALTA':
            faltas.append(row)
print faltas
