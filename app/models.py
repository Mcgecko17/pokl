class Pokemon:
    def __init__(self, nombre, tipos, region, numero_pokedex, imagen):
        self.nombre = nombre
        self.tipos = tipos
        self.region = region
        self.numero_pokedex = numero_pokedex
        self.imagen = imagen

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "tipos": self.tipos,
            "region": self.region,
            "numero_pokedex": self.numero_pokedex,
            "imagen": self.imagen
        }