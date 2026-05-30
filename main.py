import csv

class Cliente:
    def __init__(self, id, nombre, email, ciudad, edad):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.ciudad = ciudad
        self.edad = edad


# ValidarFila verifica que cada fila del CSV tenga los campos requeridos y que los datos sean válidos.
def ValidarFila(fila, numero_linea):
    CamposRequeridos = ["id", "nombre", "email", "ciudad", "edad"]

    for campo in CamposRequeridos:
        if campo not in fila:
            return None, f"Linea {numero_linea}: falta la columna '{campo}'"

    id_cliente = fila["id"].strip()
    nombre = fila["nombre"].strip()
    email = fila["email"].strip()
    ciudad = fila["ciudad"].strip()
    edad_texto = fila["edad"].strip()

    if not id_cliente:
        return None, f"Linea {numero_linea}: id vacio"

    if not nombre:
        return None, f"Linea {numero_linea}: nombre vacio"

    if "@" not in email or "." not in email:
        return None, f"Linea {numero_linea}: email invalido"

    if not ciudad:
        return None, f"Linea {numero_linea}: ciudad vacia"

    try:
        edad = int(edad_texto)
        if edad < 0:
            return None, f"Linea {numero_linea}: edad fuera de rango"
    except ValueError:
        return None, f"Linea {numero_linea}: edad no numerica"


    return Cliente(id_cliente, nombre, email, ciudad, edad), None

#Carga del archivo usando rutas sin comillas, validando cada fila y acumulando errores para reportar al usuario.
def CargaDeClientes(ruta_archivo):
    clientes = []
    errores = []
    ids_cargados = set()

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)

            if lector.fieldnames is None:
                return [], ["El archivo esta vacio o no tiene encabezados"]

            Columnas = ["id", "nombre", "email", "ciudad", "edad"]
            if lector.fieldnames != Columnas:
                errores.append(
                    "Faltan Columnas requeridas o el formato es incorrecto. Se esperaban: id, nombre, email, ciudad, edad"
                )

            for numero_linea, fila in enumerate(lector, start=2):
                if None in fila:
                    errores.append(f"Linea {numero_linea}: contiene campos extra")
                    continue

                cliente, error = ValidarFila(fila, numero_linea)
                if error:
                    errores.append(error)
                    continue

                if cliente.id in ids_cargados:
                    errores.append(f"Linea {numero_linea}: id duplicado '{cliente.id}'")
                    continue

                clientes.append(cliente)
                ids_cargados.add(cliente.id)

    except FileNotFoundError:
        errores.append(f"No se encontro el archivo: {ruta_archivo}")
    except OSError as error:
        errores.append(f"No se pudo leer el archivo: {error}")

    return clientes, errores

#Muestra detalles del cliente que coincide con la busqueda
def MostrarCliente(cliente):
    print(f"ID: {cliente.id}")
    print(f"Nombre: {cliente.nombre}")
    print(f"Email: {cliente.email}")
    print(f"Ciudad: {cliente.ciudad}")
    print(f"Edad: {cliente.edad}")

#Busqueda por ID
def BuscarUsandoID(clientes):
    IdBuscado = input("Ingrese el ID del cliente: ").strip()
    for cliente in clientes:
        if cliente.id == IdBuscado:
            print("\nCliente encontrado:")
            MostrarCliente(cliente)
            return

    print("No se encontro un cliente con ese ID.")

#Busqueda por ciudad
def BuscarPorCiudad(clientes):
    CiudadBuscada = input("Ingrese la ciudad: ").strip().lower()
    encontrados = [
        cliente for cliente in clientes if cliente.ciudad.lower() == CiudadBuscada
    ]

    if not encontrados:
        print("No se encontraron clientes en esa ciudad.")
        return

    print(f"\nClientes encontrados: {len(encontrados)}")
    for cliente in encontrados:
        print("-" * 40)
        MostrarCliente(cliente)

#Ordenar por Edad
def OrdenarPorEdad(clientes):
    if not clientes:
        print("No hay clientes cargados.")
        return

    ClientesOrdenados = sorted(clientes, key=lambda cliente: cliente.edad)

    print("\nClientes ordenados por edad:")
    for cliente in ClientesOrdenados:
        print(f"{cliente.id} | {cliente.edad:3} | {cliente.nombre} | {cliente.email} | {cliente.ciudad}")

#Muestra errores 
def MostrarErrores(errores):
    if not errores:
        print("No se registraron errores.")
        return

    print(f"\nErrores encontrados: {len(errores)}")
    for error in errores:
        print(f"- {error}")

#Menu principal del programa
def Menu():
    print("\n=== Sistema de Clientes ===")
    print("1. Cargar clientes desde otro archivo CSV")
    print("2. Buscar cliente por ID")
    print("3. Listar clientes por ciudad")
    print("4. Listar clientes ordenados por edad")
    print("5. Ver reporte de errores")
    print("6. Salir")

#ejecucion del programa
def main():
    clientes = []
    errores = []

    ruta=input("Ingrese la ruta del archivo CSV: ").strip()
    clientes, errores = CargaDeClientes(ruta)
    print(f"Clientes validos cargados: {len(clientes)}")
    print(f"Registros invalidos o advertencias: {len(errores)}")

    while True:
        Menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            ruta = input("Ruta del archivo CSV: ").strip()

            clientes, errores = CargaDeClientes(ruta)
            print(f"Clientes validos cargados: {len(clientes)}")
            print(f"Registros invalidos o advertencias: {len(errores)}")

        elif opcion == "2":
            if clientes:
                BuscarUsandoID(clientes)
            else:
                print("Primero debe cargar los clientes.")

        elif opcion == "3":
            if clientes:
                BuscarPorCiudad(clientes)
            else:
                print("Primero debe cargar los clientes.")

        elif opcion == "4":
            OrdenarPorEdad(clientes)

        elif opcion == "5":
            MostrarErrores(errores)

        elif opcion == "6":
            print("Programa finalizado.")
            break

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()
