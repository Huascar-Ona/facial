from pypxlib import Table
from datetime import datetime
import sys

table = Table("/mnt/servidorconta/ASISTMIL/Autorizaciones.DB")
for field in table.fields:
    print field,table.fields[field]
