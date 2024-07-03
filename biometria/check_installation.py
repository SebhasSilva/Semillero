try:
    import pymongo
    import dns
    print("pymongo y dnspython se han instalado correctamente.")
except ImportError as e:
    print("Error al importar las bibliotecas:", e)
