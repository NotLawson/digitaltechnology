// Pokedex API
const base = "https://pokeapi.co/api/v2/"

const examplePokemonData = {
    "id": 1,
    "name":"<name>",
    "type":["<type1>", "<type2>"],
    "height":7,
    "weight":69,
    "gif":"<gif_url>",
    "stats":[

    ]
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

async function getPokemon(pokemon) {
    return await fetch(base + "pokemon/" + pokemon)
    .then(res => {
        if (res.ok) { return res.json(); } else { throw new Error("Pokemon Not Found");}
    })
    .then(data => {
        return {
            id: data.id,
            name: capitalize(data.name),
            type: data.types.map(t => { 
                t.type.name = capitalize(t.type.name);
                id = t.type.url.split("/")[6];
                t.type.url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/ruby-sapphire/" + id + ".png";
                return t.type;
            }),
            height: data.height,
            weight: data.weight,
            gif: data.sprites.other.showdown.front_default,
            stats: data.stats
        }
    });
}