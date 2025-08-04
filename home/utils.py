import sqlite3

def obtener_codigo(tabla, nombre):
    conexion = sqlite3.connect("ahogamientos.db")
    cursor = conexion.cursor()
    cursor.execute(f"SELECT cod{tabla} FROM {tabla} WHERE nombre{tabla} = ?", (nombre,))
    resultado = cursor.fetchone()
    if resultado is None:
        return None
    else:
        return resultado[0]

def obtener_nombre(tabla, codigo):
    conexion = sqlite3.connect("ahogamientos.db")
    cursor = conexion.cursor()
    cursor.execute(f"SELECT nombre{tabla} FROM {tabla} WHERE cod{tabla} = ?", (codigo,))
    resultado = cursor.fetchone()
    if resultado is None:
        return None
    else:
        return resultado[0]

def obtener_fecha_incidente(codigo):
    conexion = sqlite3.connect("ahogamientos.db")
    cursor = conexion.cursor()
    cursor.execute(f"SELECT fecha FROM Incidente WHERE codIncidente = ?", (codigo,))
    resultado = cursor.fetchone()
    if resultado is None:
        return None
    else:
        return resultado[0]

from django.db import connection

def obtener_ahogamientos_por_comunidad(anio, codigos):
    from django.db import connection

    if not codigos:
        return []

    placeholders = ','.join(['?'] * len(codigos))
    query = f'''
        SELECT c.nombreCCAA AS Comunidad, COUNT(v.codVictima) AS Ahogamientos
        FROM Victima v
        JOIN Incidente i ON v.incidente = i.codIncidente
        JOIN CCAA c ON v.localidad.provincia.CCAA.codCCAA = c.codCCAA
        WHERE c.codCCAA IN ({placeholders}) AND strftime('%Y', i.fecha) = ?
        GROUP BY c.nombreCCAA
        ORDER BY Ahogamientos DESC
    '''
    params = list(codigos) + [str(anio)]
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultados = cursor.fetchall()
    return resultados
