from flask import current_app as app, render_template, request
import requests
from difflib import get_close_matches
from .models import Pokemon

# Diccionario de traducción de tipos de Pokémon
type_translation = {
    'normal': 'Normal',
    'fighting': 'Lucha',
    'flying': 'Volador',
    'poison': 'Veneno',
    'ground': 'Tierra',
    'rock': 'Roca',
    'bug': 'Bicho',
    'ghost': 'Fantasma',
    'steel': 'Acero',
    'fire': 'Fuego',
    'water': 'Agua',
    'grass': 'Planta',
    'electric': 'Eléctrico',
    'psychic': 'Psíquico',
    'ice': 'Hielo',
    'dragon': 'Dragón',
    'dark': 'Siniestro',
    'fairy': 'Hada'
}

# Diccionario de traducción de regiones
region_translation = {
    'kanto': 'Kanto',
    'johto': 'Johto',
    'hoenn': 'Hoenn',
    'sinnoh': 'Sinnoh',
    'unova': 'Teselia',
    'kalos': 'Kalos',
    'alola': 'Alola',
    'galar': 'Galar'
}

# Obtener la lista de todos los Pokémon
def obtener_lista_pokemones():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return [pokemon['name'] for pokemon in respuesta.json()['results']]
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    termino = request.form.get('termino')
    if termino:
        lista_pokemones = obtener_lista_pokemones()
        nombre_mas_similar = get_close_matches(termino.lower(), lista_pokemones, n=1)
        if nombre_mas_similar:
            nombre_pokemon = nombre_mas_similar[0]
            url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                nombre = datos['name']
                tipos = [type_translation[tipo['type']['name']] for tipo in datos['types']]
                numero_pokedex = datos['id']
                imagen = datos['sprites']['front_default']
                
                # Obtener la región del Pokémon
                url_especie = datos['species']['url']
                respuesta_especie = requests.get(url_especie)
                if respuesta_especie.status_code == 200:
                    datos_especie = respuesta_especie.json()
                    region = "Desconocida"
                    for entry in datos_especie['pokedex_numbers']:
                        pokedex_name = entry['pokedex']['name']
                        if pokedex_name in region_translation:
                            region = region_translation[pokedex_name]
                            break
                else:
                    region = "Desconocida"
                
                pokemon = Pokemon(nombre, tipos, region, numero_pokedex, imagen)
                return render_template('pokemon.html', pokemon=pokemon)
            else:
                error = "Pokémon no encontrado."
                return render_template('index.html', error=error)
        else:
            error = "Pokémon no encontrado."
            return render_template('index.html', error=error)
    error = "No se proporcionó un término de búsqueda."
    return render_template('index.html', error=error)