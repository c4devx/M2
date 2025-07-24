import os
from db_conector import get_dbengine
from sqlalchemy import text

SCRIPTS_DIR = "scripts_sql"

SCRIPT_ORDER = [
    "2.usuarios.sql",
    "3.categorias.sql",
    "4.productos.sql",
    "5.ordenes.sql",
    "6.detalles.sql",
    "7.direcciones_envio.sql",
    "8.carrito.sql",
    "9.metodos_pago.sql",
    "10.ordenes_metodospago.sql",
    "11.resenas_productos.sql",
    "12.historial_pagos.sql"
]

def run_sql_script(engine, filepath):
    print(f"\nEjecutando script --> {filepath}")
    with engine.connect() as conn:
        with conn.begin():
            with open(filepath, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))

def main():
    print("1. Crear tablas")
    print("2. Cargar datos")
    choice = input("Opción: ").strip()

    engine = get_dbengine()
    print(f"\nConectando a la db --> {engine.url}")

    if choice == "1":
        ddl_path = os.path.join(SCRIPTS_DIR, "1.Create_ddl.sql")
        if os.path.isfile(ddl_path):
            run_sql_script(engine, ddl_path)
        else:
            print("error --> no se encuentra el 1.Create_ddl.sql")

    elif choice == "2":
        print("\n🔄 Ejecutando scripts en orden lógico...")
        for script in SCRIPT_ORDER:
            filepath = os.path.join(SCRIPTS_DIR, script)
            if os.path.isfile(filepath):
                try:
                    run_sql_script(engine, filepath)
                except Exception as e:
                    print(f"error --> {e}\n continuar con el siguiente")
            else:
                print(f"error --> {script} no encontrado")

if __name__ == "__main__":
    main()