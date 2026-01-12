import psycopg2
from datetime import date
import pandas as pd
from app.db import conectar_bd
from app.queries import (
    QUERY_CAJA,
    QUERY_PARTICIPANTE,
    QUERY_INSERTAR_PAGO,
    QUERY_RESUMEN_COMPLETO,    
    QUERY_RESUMEN_ID,
    QUERY_ULTIMO_PAGO,
    QUERY_ACTUALIZAR_PAGO
)

#OBTENEMOS LA FECHA DE INCIO
def obtener_fecha_inicio():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute(QUERY_CAJA)
    fecha_inicio, semanas = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return fecha_inicio, semanas

#CALCULAMOS LA SEMANA ACTUAL
def semana_actual():
    fecha_inicio, semanas_totales = obtener_fecha_inicio()
    hoy = date.today()
    
    dias = (hoy - fecha_inicio).days
    semana = (dias // 7) + 1
    return min(semana, semanas_totales)

#AQUI HAGO LA FUNCION PARA MOSTRAR EL RESUMEN YA QUE SE OCUPA EN VARIAS LADOS Y ES MAS COMODO Y LIMPIO
def mostrar_resumen(participante_id, nombre, pago, pagado, semana, semanas_totales):
    esperado = semana * pago
    diferencia = pagado - esperado

    capital = pago * semanas_totales
    interes = capital * 0.10
    total = capital + interes

    if diferencia > 0:
        estado = "ADELANTADO"
    elif diferencia < 0:
        estado = "ATRASADO"
    else:
        estado = "AL DÍA"

    print(f"""
{nombre} (ID: {participante_id})
Pagado: ${pagado:,.2f}
Esperado: ${esperado:,.2f}
Diferencia: ${diferencia:,.2f}
Estado: {estado}
-------------------------------
Proyeccion al final de la caja:
Capital final: ${capital:,.2f} |  Interés (10%): ${interes}
Total a recibir: ${total:,.2f}        
""")
    
#REGISTAR PAGO (CON CONFIRMACION)

def registrar_pago():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        participante_id = int(input("ID del participante: "))
        
        cursor.execute(QUERY_PARTICIPANTE, (participante_id,))
        
        dato = cursor.fetchone()
        
        if not dato:
            print("ID no encontrado")
            return
        
        nombre, pago = dato
        print(f"NOMBRE: {nombre}")
        print(f"pago semanal: ${pago}")
        
        if input("¿Confirmar? (S/N): ").upper() != "S":
            print("Cancelado")
            return
        
        monto = int(input("Monto pagado: " ))
        if monto % 100 != 0:
            print("Monto no valido")
            return
        
        cursor.execute(QUERY_INSERTAR_PAGO, (participante_id, monto))
        conn.commit()
        print ("Pago registrado correctamente")
        
    except ValueError:
        print("Debes ingresar solo números")
    
    except psycopg2.Error as e:
        print("Error en la base de datos")    
        print(e)
    
    finally:
        if 'cursor' in locals():
             cursor.close()
        if 'conn' in locals():
             conn.close()

# EXPORTAR EL EXCEL
def exportar_excel(df, nombre_archivo):
    try:
        df.to_excel(nombre_archivo, index=False)
        print(f"Excel generado correctamente: {nombre_archivo}")
        
    except Exception as e:
        print("Error al generar el archivo Excel")
        print(e)
        
# CREAR EL EXCEL PARA PODER OBSERVAR LOS DATOS DEL RESUMEN COMPLETO
def resumen_completo_excel():
    try:
        conn = conectar_bd()

        df = pd.read_sql(QUERY_RESUMEN_COMPLETO, conn)

        semana = semana_actual()
        _, semanas_totales = obtener_fecha_inicio()

        df["Esperado"] = df["pago_semanal"] * semana
        df["Diferencia"] = df["total_pagado"] - df["Esperado"]
        df["Capital Final"] = df["pago_semanal"] * semanas_totales
        df["Interés (10%)"] = df["Capital Final"] * 0.10
        df["Total a Recibir"] = df["Capital Final"] + df["Interés (10%)"]

        def estado(row):
            if row["Diferencia"] > 0:
                return "ADELANTADO"
            elif row["Diferencia"] < 0:
                return "ATRASADO"
            return "AL DÍA"

        df["Estado"] = df.apply(estado, axis=1)

        # MOSTRAR EN PANTALLA
        for _, r in df.iterrows():
            mostrar_resumen(
                r["id"], r["nombre"], r["pago_semanal"], r["total_pagado"],
                semana, semanas_totales
            )

        if input("\n¿Deseas exportar a Excel? (S/N): ").upper() == "S":
            exportar_excel(df, "resumen_caja_completo.xlsx")

    except Exception as e:
        print("Error al generar el resumen completo")
        print(e)

    finally:
        if 'conn' in locals():
            conn.close()

#CREAR EL EXCEL PARA PODER OBSERVAR LOS DATOS DEL RESUMEN POR PERSONA ID
def resumen_id_excel():
    try:
        conn = conectar_bd()
        participante_id = int(input("ID del participante: "))

        df = pd.read_sql(
            QUERY_RESUMEN_ID,
            conn,
            params=(participante_id,)
        )

        if df.empty:
            print("No existe ese participante")
            return

        semana = semana_actual()
        _, semanas_totales = obtener_fecha_inicio()

        df["Esperado"] = df["pago_semanal"] * semana
        df["Diferencia"] = df["total_pagado"] - df["Esperado"]
        df["Capital Final"] = df["pago_semanal"] * semanas_totales
        df["Interés (10%)"] = df["Capital Final"] * 0.10
        df["Total a Recibir"] = df["Capital Final"] + df["Interés (10%)"]

        df["Estado"] = df["Diferencia"].apply(
            lambda x: "ADELANTADO" if x > 0 else "ATRASADO" if x < 0 else "AL DÍA"
        )

        r = df.iloc[0]
        mostrar_resumen(
            r["id"], r["nombre"], r["pago_semanal"], r["total_pagado"],
            semana, semanas_totales
        )

        if input("\n¿Deseas exportar este resumen a Excel? (S/N): ").upper() == "S":
            exportar_excel(df, f"resumen_{r['nombre']}.xlsx")

    except Exception as e:
        print("Error al generar el resumen por ID")
        print(e)

    finally:
        if 'conn' in locals():
            conn.close()

#ESTAS SON LAS FUNCIONES QUE VOY A NECESITAR PARA PODER FUNCIONAR LA WEB -----------------------------

def registrar_pago_web(participante_id, monto):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute(QUERY_PARTICIPANTE, (participante_id,))
        dato = cursor.fetchone()

        if not dato:
            return False, "ID no encontrado o participante inactivo"

        nombre, pago_semanal = dato

        if monto % 100 != 0:
            return False, "El monto debe ser múltiplo de 100"

        cursor.execute(
            QUERY_INSERTAR_PAGO,
            (participante_id, monto)
        )
        conn.commit()

        return True, f"Pago registrado correctamente para {nombre}"

    except Exception as e:
        return False, f"Error: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
def resumen_completo_web():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(QUERY_RESUMEN_COMPLETO)
    filas = cursor.fetchall()

    semana = semana_actual()
    _, semanas_totales = obtener_fecha_inicio()

    resultado = []

    for participante_id, nombre, pago, pagado in filas:
        esperado = semana * pago
        diferencia = pagado - esperado

        capital = pago * semanas_totales
        interes = capital * 0.10
        total = capital + interes

        if diferencia > 0:
            estado = "adelantado"
            estado_texto = "ADELANTADO"
            
        elif diferencia < 0:
            estado = "atrasado"
            estado_texto = "ATRASADO"
            
        else:
            estado = "aldia"
            estado_texto = "AL DÍA"

        resultado.append({
            "id": participante_id,
            "nombre": nombre,
            "pagado": pagado,
            "esperado": esperado,
            "diferencia": diferencia,
            "estado": estado,
            "estado_texto": estado_texto,
            "capital": capital,
            "interes": interes,
            "total": total
        })

    cursor.close()
    conn.close()

    return resultado

def resumen_id_web(participante_id):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute(QUERY_RESUMEN_ID, (participante_id,))
    fila = cursor.fetchone()  

    if not fila:
        cursor.close()
        conn.close()
        return None

    semana = semana_actual()
    _, semanas_totales = obtener_fecha_inicio()

    participante_id, nombre, pago_semanal, total_pagado = fila

    esperado = semana * pago_semanal
    diferencia = total_pagado - esperado

    capital = pago_semanal * semanas_totales
    interes = capital * 0.10
    total = capital + interes

    if diferencia > 0:
        estado = "adelantado"
        estado_texto = "ADELANTADO"
        
    elif diferencia < 0:
        estado = "atrasado"
        estado_texto = "ATRASADO"
        
    else:
        estado = "aldia"
        estado_texto = "AL DÍA"
          

    resultado = {
        "id": participante_id,
        "nombre": nombre,
        "pago_semanal": pago_semanal,   
        "pagado": total_pagado,
        "esperado": esperado,
        "diferencia": diferencia,
        "estado": estado,
        "estado_texto": estado_texto,
        "capital": capital,
        "interes": interes,
        "total": total
    }

    cursor.close()
    conn.close()

    return resultado

def obtener_ultimo_pago_web(participante_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(QUERY_ULTIMO_PAGO, (participante_id,))
        return cursor.fetchone()  # (pago_id, monto) o None
    finally:
        cursor.close()
        conn.close()
        
def actualizar_pago_web(pago_id, nuevo_monto):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            QUERY_ACTUALIZAR_PAGO,
            (nuevo_monto, pago_id)
        )
        conn.commit()
        return True, "Pago actualizado correctamente"
    except Exception as e:
        conn.rollback()
        return False, f"Error al actualizar pago: {e}"
    finally:
        cursor.close()
        conn.close()