# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
import os
RUTA = "/mnt/asistmil/ASISTMIL/OPENRP.CSV"
RUTA2 = "./OPENERP_CO.CSV"

class incidencias(osv.Model):
    _name = "asistmil.incidencias"

    _columns = {
        'empleado': fields.integer("Empleado"),
        'fecha': fields.date("Fecha"),
        'entrada': fields.float("Entrada"),
        'inicomida': fields.float("Inicio comida"),
        'fincomida': fields.float("Fin comida"),
        'entrada': fields.float("Entrada"),
        'salida': fields.float("Salida"),
        'horario': fields.char("Horario"),
        'retardo': fields.float("Retardo"),
        'anticipado': fields.float("Anticipado"),
        'comida': fields.float("Comida"),
        'extras': fields.float("Extras"),
        'total': fields.float("Total"),
        'registros': fields.integer("Registros"),
    }

class autorizaciones(osv.Model):
    _name = "asistmil.autorizaciones"


    def insert(self, cr, uid, empleado, fecha, justificante):
        if type(fecha) in (str,unicode):
            y,m,d = fecha.split("-")
            fecha = "%s/%s/%s"%(d,m,y)
        else:
            fecha = fecha.strftime("%d/%m/%Y")
        with open(RUTA, "a") as f:
            f.write("%s,%s,%s\r\n"%(empleado,fecha,justificante))

        return True

    def insert_occacional(self, cr, uid, empleado, fecha, horario, tiempo):
        if type(fecha) in (str,unicode):
            y,m,d = fecha.split("-")
            fecha = "%s/%s/%s"%(d,m,y)
        else:
            fecha = fecha.strftime("%d/%m/%Y")
        with open(RUTA2, "a") as f:
            f.write("%s,%s,%s,%s\r\n"%(empleado,fecha,horario,tiempo))

        return True

    _columns = {
        'empleado': fields.integer("Empleado"),
        'fecha': fields.date("Fecha"),
        'justificante': fields.integer("Justificante"),
        'folio': fields.char("Folio")
    }

class justificantes(osv.Model):
    _name = "asistmil.justificantes"

    def name_get(self, cr, uid, ids, context=None):
        names = []
        for rec in self.browse(cr, uid, ids):
            nombre = "[%s] %s"%(rec.clave, rec.descripcion)
            names.append((rec.id, nombre))
        return names

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                         context=None, limit=100):
        if not args:
            args = []

        ids = self.search(cr, user, [('clave', 'ilike', name)] + args, limit=limit, context=context)

        search_domain = [('descripcion', operator, name)]
        if ids: search_domain.append(('id', 'not in', ids))
        ids.extend(self.search(cr, user, search_domain + args,
                           limit=limit, context=context))

        recs = self.name_get(cr, user, ids, context)
        return sorted(recs, key=lambda (id, name): ids.index(id))

    _columns = {
        'clave': fields.integer("Clave"),
        'descripcion': fields.char(u"Descripción"),
        'tiempo': fields.char("Tiempo"),
        'dia': fields.char(u"Día"),
        'entrada': fields.char("Entrada"),
        'salida': fields.char("Entrada")
    }

class secuencias(osv.Model):
    _name = "asistmil.secuencias"
    _rec_name = 'clave'

    _columns = {
        'clave': fields.integer("Clave"),
        'domingo': fields.integer("Domingo"),
        'lunes': fields.integer("Lunes"),
        'martes': fields.integer("Martes"),
        'miercoles': fields.integer(u"Miércoles"),
        'jueves': fields.integer("Jueves"),
        'viernes': fields.integer("Viernes"),
        'sabado': fields.integer(u"Sábado"),
        'descripcion': fields.char(u"Descripción")
    }

#Las siguientes tablas no se copian directo del asistmil, hay un proceso que las arma

class asignaciones(osv.Model):
    _name = "asistmil.asignaciones"

    _columns = {
        'emp': fields.integer("Empleado"),
        'semana': fields.integer("Semana"),
        'anio': fields.integer(u"Año"),
        'secuencia': fields.integer("Secuencia"),
    }

class inciden(osv.Model):
    _name = "asistmil.inciden"

    _columns = {
        'empleado': fields.integer("Empleado"),
        'fecha': fields.date("Fecha"),
        'tiempo': fields.float("Tiempo"),
        'tipo': fields.char("Tipo"),
        'secuencia': fields.integer("Secuencia"),
        'process': fields.boolean("Aplicado")
    }

#Botón para actualizar los justificantes on demand

class actualizar_justificantes(osv.TransientModel):
    _name = "asistmil.actualizar.justificantes"

    def actualizar(self, cr, uid, ids, context=None):
        os.system("python /opt/addons_zenpar/facial/carga_justificantes.py")
        return True
