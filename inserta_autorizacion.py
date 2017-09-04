# -*- coding: utf-8 -*-
from pypxlib import Table
from datetime import datetime
import sys
#empleado = int(sys.argv[1])
#fecha = datetime.strptime(sys.argv[2], "%Y-%m-%d")
#justificante = int(sys.argv[3])
table = Table("/root/Autorizaciones.DB")
#table = Table("/mnt/servidorconta/ASISTMIL/Autorizaciones.DB")
#table.insert((empleado, fecha, justificante, ''))
i = 0
for row in table:
    print i,row
    i += 1
table.close()
