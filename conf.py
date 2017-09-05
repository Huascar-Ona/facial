import psycopg2
def get_conf():
    conn = psycopg2.connect("dbname=offset23agosto user=openerp password=zentella host=localhost")
    cr = conn.cursor()
    path = "/mnt/asistmil/"
    return conn,cr,path
