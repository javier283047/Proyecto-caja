import os
import sys
import psycopg2
from archivo_caja import (
    registrar_pago,
    semana_actual,
    resumen_completo_excel,
    resumen_id_excel,
    )


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def submenu_resumen():
    while True:
        limpiar_pantalla()
        print("\n--- RESUMEN ---")
        print("1. Resumen completo")
        print("2. Resumen por ID")
        print("3. Volver al menú principal")
        
        opcion = input("Seleccionar una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            resumen_completo_excel()
            input("\nPresiona ENTER para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            resumen_id_excel()
            input("\nPresiona ENTER para continuar...")
        
        elif opcion == "3":
            break
        
        else:
            print("Opción no válida")
            input("Presiona ENTER...")
    
def menu():
    while True:
        try:   
            print(f"\n---CONTROL DE CAJA 2025 | Semana {semana_actual()}---")
            print("1. Registrar pago")
            print("2. Ver resumen")
            print("3. Salir")
            
            opcion = input("\nSeleccionar una opción: ")
            
            if opcion == "1":
                limpiar_pantalla()
                registrar_pago()
                
            elif opcion == "2":
                submenu_resumen()
                
            elif opcion == "3":
                print("Saliendo del sistema...")
                break
            
            else:
                print("Opción no válida.")
                input("Presiona ENTER...")
                
        except KeyboardInterrupt:
            print("\nSaliendo forzadamente...")
            sys.exit()
        
        except psycopg2.OperationalError:
            print("\nError crítico: No se pudo establecer conexión con el servidor.")
            print("Verifica que PostgreSQL esté ejecutándose.")
            sys.exit()
        
        except Exception as e:
            print(f"\nOcurrió un error inesperado en el menú: {e}")
            sys.exit()
                            
if __name__ == "__main__":
    menu()