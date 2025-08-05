<script setup>
import { ref, onMounted } from "vue";
import SearchAutocomplete from "./SearchAutocomplete.vue";
import SkinImage from "./SkinImage.vue";
// defineEmits(["onWrongGuess", "onRightGuess"]);
defineProps({
  msg: String,
});

const SERVER_URL = "http://localhost:8000/";

// const count = ref(0);
var test = ref(false);
var localstoragetest = ref(0);

const searchDisable = ref([
  [false, false, false],
  [false, false, false],
  [false, false, false],
]);

function toggleTest() {
  test.value = !test.value;
}

const guesses = ref(10);
const already_guessed = ref([]);

function createWrongGuess(name, r, c) {
  const guessEvent = new CustomEvent("onWrongGuess", {
    detail: {
      name: name,
      row: r,
      col: c,
    },
  });
  return guessEvent;
}

function createRightGuess(name, r, c, index, num_possible) {
  const guessEvent = new CustomEvent("onRightGuess", {
    detail: {
      name: name,
      row: r,
      col: c,
      index: index,
      num_possible: num_possible,
    },
  });
  return guessEvent;
}

document.addEventListener("invalidGuess", (e) => {
  // implement what happens when a user inputs the wrong thing (not in list)
});

document.addEventListener("userGuessed", (e) => {
  console.log(e.detail.name);
  guesses.value = guesses.value - 1;
  console.log(
    "row",
    e.detail.row,
    "col",
    e.detail.col,
    "board_data",
    board_data
  );
  // console.log(board_data["board"][e.detail.row][e.detail.col]);

  const right_answers = board_data.value["board"][e.detail.row][e.detail.col];
  const index = right_answers.indexOf(e.detail.name);

  if (index === -1) {
    // emit("onWrongGuess");
    console.log("wrong guess", e.detail.name);
    document.dispatchEvent(
      createWrongGuess(e.detail.name, e.detail.row, e.detail.col)
    );
  } else {
    console.log("right guess", e.detail.name);
    // already_guessed.value.push(e.detail.name);
    // remove the skin from the possible guesses
    function notSkin(name) {
      return name != e.detail.name;
    }
    const index_to_remove = all_skins.value.indexOf(e.detail.name);
    console.log("DEBUG:", e.detail.name, index_to_remove);
    // all_skins.value = all_skins.value.splice(index_to_remove);
    // all_skins.value.splice(index_to_remove);
    all_skins.value = all_skins.value.filter(notSkin);
    // all_skins.value.splice(index_to_remove, index_to_remove)
    // all_skins.value = [];
    // console.log()
    document.dispatchEvent(
      createRightGuess(
        e.detail.name,
        e.detail.row,
        e.detail.col,
        index + 1, // to account for 0-indexing
        right_answers.length
      )
    );
  }
});

document.addEventListener(
  "onWrongGuess",
  //IMPLENENT THE EVENT LISTENER
  (e) => {
    const row = e.detail.row;
    const col = e.detail.col;
    console.log("IN THE WRONG GUESS THINGY", guesses.value);

    if (guesses.value === 0) {
      for (let r = 0; r < searchDisable.value.length; r++) {
        for (let c = 0; c < searchDisable.value[r].length; c++) {
          searchDisable.value[r][c] = true;
        }
      }
    }
  }
);

function rowColtoString(row, col) {
  return "" + row + col;
}

document.addEventListener("onRightGuess", (e) => {
  const row = e.detail.row;
  const col = e.detail.col;
  console.log(
    "IN THE RIGHT GUESS THINGY",
    e.detail.num_possible,
    e.detail.index
  );
  var skin_name = e.detail.name.replace(" | ", "_").replace(" ", "_");
  // console.log("SKIN NAME CLEANED: ", skin_name);
  fetch(SERVER_URL + "get_skin_image/" + skin_name)
    .then((response) => response.blob())
    .then((imageBlob) => {
      const imageUrl = URL.createObjectURL(imageBlob);

      const element = document.getElementById(
        rowColtoString(row, col) + "-img" // get the ID for the corresponding image component
      );

      searchDisable.value[row][col] = true;

      if (element) {
        const img = document.createElement("img");

        img.src = imageUrl;
        /*
        LATER: Add a thing where the background color changes depending on how well you guess,
        so:
        #1 best choice would be Gold (like knife)
        Top 5% would be Red (Covert)
        Top 10% would be Pink (Classified)
        Top 25% would be Purple
        Top 50% would be Blue
        Top 75% would be Industrial, and
        Remainder would be Grey

        Could probably calculate this just by taking the index (1-based, should already be done for me) and chechking if:
        Equals 1
        or
        index / num_possible < some threshold
        */
        const index = e.detail.index;
        const num_possible = e.detail.num_possible;

        img.style.height = "30%";
        img.style.width = "auto";
        img.style.maxWidth = "200px";

        var color = "#ffffff"; // default to white

        if (index === 1) {
          color = "#b39700";
        } else if (index / num_possible <= 0.1) {
          color = "#921010";
        } else if (index / num_possible <= 0.2) {
          color = "#8d129a";
        } else if (index / num_possible <= 0.4) {
          color = "#38009d";
        } else if (index / num_possible <= 0.6) {
          color = "#001a9c";
        } else if (index / num_possible <= 0.8) {
          color = "#1f4e83";
        } else {
          color = "#636b6d";
        }

        element.style.backgroundColor = color;
        // img.style.resize = "10%";

        element.appendChild(img);
      }
    });
});

// add in events for correct guess, as well as incorrect guess...

const board_data = ref(null);
const all_skins = ref(null);

function fetchAllSkins() {
  fetch(SERVER_URL + "all_skins").then((response) => {
    response.json().then((value) => {
      console.log(value);
      all_skins.value = value;
      return value;
    });
  });
}

function fetchBoard() {
  return fetch(SERVER_URL + "board");
}

onMounted(() => {
  let response;
  fetchAllSkins();
  fetchBoard()
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response error when getting game board");
      }
      response.json().then((value) => {
        console.log(value);
        board_data.value = value;
        console.log(
          "board",
          board_data["board"],
          "row qs",
          board_data["row_queries"]
        );
        return value;
      });
    })
    .then((data) => {
      // console.log("printing data...");
      // console.log(data.json());
    });
  // for testing:
  if (localStorage.getItem("test")) {
    let t = JSON.parse(localStorage.getItem("test"));
    console.log("The current stored value is: ", t, "increment by one:");
    localStorage.setItem("test", t + 1);
  } else {
    localStorage.setItem("test", JSON.stringify(0));
  }
});
</script>

<template>
  <button @click="toggleTest">Click here</button>
  <p>Guesses left: {{ guesses }}</p>
  <div v-if="board_data">
    <table>
      <tr>
        <td>...</td>
        <th>
          {{ board_data["col_queries"][0] }}
        </th>
        <th>{{ board_data["col_queries"][1] }}</th>
        <th>{{ board_data["col_queries"][2] }}</th>
      </tr>
      <tr>
        <th>{{ board_data["row_queries"][0] }}</th>
        <td class="square">
          <!-- <p v-if="test">Testing 123</p> -->
          <SkinImage :row="0" :col="0" />
          <SearchAutocomplete
            :items="all_skins"
            :row="0"
            :col="0"
            :disabled="searchDisable[0][0]"
            @wrongGuess="console.log('HELP ME')"
          />
        </td>
        <td class="square">
          <SkinImage :row="0" :col="1" />
          <SearchAutocomplete
            :items="all_skins"
            :row="0"
            :col="1"
            :disabled="searchDisable[0][1]"
          />
        </td>
        <td class="square">
          <SkinImage :row="0" :col="2" />
          <SearchAutocomplete
            :items="all_skins"
            :row="0"
            :col="2"
            :disabled="searchDisable[0][2]"
          />
        </td>
      </tr>
      <tr>
        <th>{{ board_data["row_queries"][1] }}</th>
        <td class="square">
          <SkinImage :row="1" :col="0" />
          <SearchAutocomplete
            :items="all_skins"
            :row="1"
            :col="0"
            :disabled="searchDisable[1][0]"
          />
        </td>
        <td class="square">
          <SkinImage :row="1" :col="1" />
          <SearchAutocomplete
            :items="all_skins"
            :row="1"
            :col="1"
            :disabled="searchDisable[1][1]"
          />
        </td>
        <td class="square">
          <SkinImage :row="1" :col="2" />
          <SearchAutocomplete
            :items="all_skins"
            :row="1"
            :col="2"
            :disabled="searchDisable[1][2]"
          />
        </td>
      </tr>
      <tr>
        <th>{{ board_data["row_queries"][2] }}</th>
        <td class="square">
          <SkinImage :row="2" :col="0" />
          <SearchAutocomplete
            :items="all_skins"
            :row="2"
            :col="0"
            :disabled="searchDisable[2][0]"
          />
        </td>
        <td class="square">
          <SkinImage :row="2" :col="1" />
          <SearchAutocomplete
            :items="all_skins"
            :row="2"
            :col="1"
            :disabled="searchDisable[2][1]"
          />
        </td>
        <td class="square">
          <SkinImage :row="2" :col="2" />
          <SearchAutocomplete
            :items="all_skins"
            :row="2"
            :col="2"
            :disabled="searchDisable[2][2]"
          />
        </td>
      </tr>
    </table>
  </div>
  <div v-else>
    <!-- Optionally show something else if board_data is undefined -->
    <p>Loading or No Data Available</p>
  </div>
</template>

<style scoped>
.square {
  width: 200px;
  height: 200px;

  border-width: 2px;
  border-color: rgb(47, 82, 147);
  border-style: solid;
}
</style>
