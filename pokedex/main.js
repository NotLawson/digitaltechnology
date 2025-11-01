// Main Pokedex script

const urlparams = new URLSearchParams(window.location.search);
var data = null;
async function main() {
    if (urlparams.has("pokemon")) {
        const pokemon = urlparams.get("pokemon");
        try {
            data = await getPokemon(pokemon);
            loadReadout(data);
            document.getElementById("note").hidden = true;
        } catch (error) {
            console.error("Error fetching Pokemon data:", error);
            document.getElementById("note").hidden = false;
            return;
        }
    }
}
main();

function help() {
    const headingCode = "color: blue; font-size: 16px;";
    const normalCode = "color: blue; font-size: 12px;";
    const last = "color: red; font-size: 12px;";
    console.log("%cPokedex Console!", headingCode);
    console.log("%cWelcome to the Pokedex Console!", normalCode);
    console.log("%cThe following functions are available:", normalCode);
    console.log("%c  - load(pokemonData)%c - Load and display the given Pokemon data in the console.", normalCode, normalCode);
    console.log("%c  - loadReadout(pokemonData)%c - Load and display the given Pokemon data in the webpage readout.", normalCode, normalCode);
    console.log("%c  - getPokemon(pokemon)%c - Search for the Pokemon name or ID entered in the search box and display its data.", normalCode, normalCode);
    console.log("%c  - help()%c - Display this help information.", normalCode, normalCode);
    console.log("%c  - clear()%c - Clear the console.", normalCode, normalCode);
    console.log("%cHave fun!", last);
}

help();

function load(pokemonData) {
    console.log("Pokedex Entry:");
    console.log("ID:", pokemonData.id);
    console.log("Name:", pokemonData.name);
    console.log("Type(s):", pokemonData.type.map(t => t.name).join(", "));
    console.log("Height:", pokemonData.height/10, "m");
    console.log("Weight:", pokemonData.weight/10, "kg");
    console.log("GIF URL:", pokemonData.gif);
    console.log("Stats:");
    pokemonData.stats.forEach(stat => {
        console.log(`  ${stat.stat.name}: ${stat.base_stat}`);
    });
}

function loadReadout(pokemonData) {
    // Load name
    const nameDiv = document.querySelector("#pokemonName");
    nameDiv.innerHTML = pokemonData.name;

    // Load types
    const typesDiv = document.querySelector("#pokemonTypes");
    pokemonData.type.forEach(type => {
        const img = document.createElement("img");
        img.src = type.url;
        img.alt = type.name;
        img.height = 14;
        img.width = 32;
        typesDiv.appendChild(img);
    });

    // Load avatar
    const avatarImg = document.querySelector("#pokemonAvatar");
    avatarImg.src = pokemonData.gif;
    avatarImg.alt = pokemonData.name + " Avatar";

    // Load ID, height, weight
    const idSpan = document.querySelector("#pokemonID");
    idSpan.innerHTML = `#${pokemonData.id}`;
    const heightSpan = document.querySelector("#pokemonHeight");
    heightSpan.innerHTML = `<strong>Height:</strong> ${pokemonData.height/10} m`;
    const weightSpan = document.querySelector("#pokemonWeight");
    weightSpan.innerHTML = `<strong>Weight:</strong> ${pokemonData.weight/10} kg`;

    // Load stats
    const statsDiv = document.querySelector("#pokemonStats");
    pokemonData.stats.forEach(stat => {
        const statItem = document.createElement("tr");
        statItem.innerHTML = `<td>${capitalize(stat.stat.name)}</td><td>${stat.base_stat}</td>`;
        statsDiv.appendChild(statItem);
    });

    const  readoutDiv = document.querySelector("#readout");
    readoutDiv.classList.remove("hidden");
}

function search() {
    const searchInput = document.querySelector("#searchInput");
    const formInput = document.querySelector("#pokemonInput");
    formInput.value = searchInput.value.trim().toLowerCase();
    document.getElementById("form").submit();
}

document.addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    search();
  }
});