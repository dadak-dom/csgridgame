<script setup>
import { ref, onMounted } from "vue";
import SkinSquare from "./SkinSquare.vue";
import PastBoards from "./PastBoards.vue";
defineProps({
  msg: String,
});

// require('dotenv').config();

// const SERVER_URL = process.env.GRIDGAME_SERVER_URL;
const SERVER_URL = import.meta.env.VITE_GRIDGAME_SERVER_URL;

const MAX_GUESSES = 10;

var test = ref(false);

const GameState = ref(null);

/*
Format of GameState in localStorage:
{
  key: board-DAY-MONTH-YEAR
  value: JSON FILE
}

JSON FILE format:
{
  guesses: int,
  searchDisable: Array of arrays
  backgroundColors: Array of arrays
  imageHTML: Array of arrays
}
*/

const searchDisable = ref([
  [false, false, false],
  [false, false, false],
  [false, false, false],
]);

const BOOL_DEFAULT = [
  [false, false, false],
  [false, false, false],
  [false, false, false],
];

const STRING_DEFAULT = [
  ["", "", ""],
  ["", "", ""],
  ["", "", ""],
];

const NULL_DEFAULT = [
  [null, null, null],
  [null, null, null],
  [null, null, null],
];

const backgroundColors = ref([
  ["", "", ""],
  ["", "", ""],
  ["", "", ""],
]);

const shakeAnimation = ref([
  [false, false, false],
  [false, false, false],
  [false, false, false],
]);

const imageHTML = ref([
  [null, null, null],
  [null, null, null],
  [null, null, null],
]);

const dailyBoardName = ref("");

// if "daily", grab the daily board
// otherwise, set the board value to the name of the board that we want
const currentBoardString = ref("");
const currentParsedBoardString = ref("");
const currentBoardFileName = ref("");

const guesses = ref(MAX_GUESSES);

/**
 * Save an item to local storage
 *
 * @param key - key for storage
 * @param value - value you want to store, ideally in JSON format
 */
function putItem(key, value) {
  // localStorage.setItem(key, value);
  const boardData = {
    data: value,
  };
  let openRequest = indexedDB.open("SkinsDatabase", 1);

  openRequest.onupgradeneeded = function () {
    console.log("UPGRADING DB!");
    let db = openRequest.result;
    if (!db.objectStoreNames.contains("boards")) {
      // if there's no "boards" store
      let objectStore = db.createObjectStore("boards"); // create it
    }
  };

  openRequest.onerror = function () {
    console.error("Error: ", openRequest.error);
  };

  openRequest.onsuccess = function () {
    let db = openRequest.result;
    // db.createObjectStore("boards", {keyPath : key})// can only be done when upgrading version
    const tx = db.transaction("boards", "readwrite");
    const store = tx.objectStore("boards");

    const putRequest = store.put(boardData, key);

    putRequest.onsuccess = () => {
      console.log("Saved: ", key, "successfully!");
    };

    putRequest.onerror = () => {
      console.error("error, ", putRequest.onerror);
    };
  };
}

/**
 *
 * Check if an item exists in localStorage
 *
 * @param key - key in localStorage
 */
function exists(key) {
  return new Promise((resolve, reject) => {
    const openRequest = indexedDB.open("SkinsDatabase", 1);

    openRequest.onerror = () => {
      console.error("Error opening DB", openRequest.error);
      reject(openRequest.error);
    };

    openRequest.onupgradeneeded = function () {
      const db = openRequest.result;
      if (!db.objectStoreNames.contains("boards")) {
        db.createObjectStore("boards");
      }
    };

    openRequest.onsuccess = function () {
      const db = openRequest.result;
      const tx = db.transaction("boards", "readonly");
      const store = tx.objectStore("boards");
      const getRequest = store.get(key);

      getRequest.onsuccess = () => {
        resolve(!!getRequest.result); // true if value found, false if null/undefined
      };

      getRequest.onerror = () => {
        reject(getRequest.error);
      };
    };
  });
}

/**
 *
 * Retrieve an item from localStorage
 *
 * @param key - key in localStorage
 */
function get(key) {
  return JSON.parse(localStorage.getItem(key));
}

/**
 * Retrieve an item from IndexedDB
 *
 * @param key - key in the db
 */
function getFromIDB(key) {
  return new Promise((resolve, reject) => {
    const openRequest = indexedDB.open("SkinsDatabase", 1);

    openRequest.onerror = () => {
      console.error("Error opening DB", openRequest.error);
      reject(openRequest.error);
    };

    openRequest.onupgradeneeded = function () {
      const db = openRequest.result;
      if (!db.objectStoreNames.contains("boards")) {
        db.createObjectStore("boards");
      }
    };

    openRequest.onsuccess = function () {
      const db = openRequest.result;
      const tx = db.transaction("boards", "readonly");
      const store = tx.objectStore("boards");
      const getRequest = store.get(key);

      getRequest.onsuccess = () => {
        const d = getRequest.result;
        console.log("Running getFromIDB on key: ", key, " result: ", d);
        resolve(d.data);
      };

      getRequest.onerror = () => {
        reject(getRequest.error);
      };
    };
  });
}

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

document.addEventListener("pastBoardChosen", (e) => {
  console.log("MESSAGE RECEIVED: ", e.detail.board);
  currentBoardString.value = e.detail.rawBoardName;
  currentParsedBoardString.value = e.detail.parsedBoardName;
  fetchPastBoard(currentBoardString.value);
});

document.addEventListener("invalidGuess", (e) => {
  // implement what happens when a user inputs the wrong thing (not in list)
  // not to be confused with a WRONG guess
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

  const right_answers = board_data.value["board"][e.detail.row][e.detail.col];
  console.log("Right answers: ", right_answers);
  const index = right_answers.indexOf(e.detail.name);

  if (guesses.value <= 0) {
    for (let r = 0; r < searchDisable.value.length; r++) {
      for (let c = 0; c < searchDisable.value[r].length; c++) {
        searchDisable.value[r][c] = true;
      }
    }
  }

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

    // if (guesses.value === 0) {
    //   for (let r = 0; r < searchDisable.value.length; r++) {
    //     for (let c = 0; c < searchDisable.value[r].length; c++) {
    //       searchDisable.value[r][c] = true;
    //     }
    //   }
    // }

    // Temporarily add the shake animation to the square prop
    shakeAnimation.value[row][col] = true;
    // console.log("Shake animation before:", shakeAnimation.value, shakeAnimation.value[row][col]);
    setTimeout(() => {
      shakeAnimation.value[row][col] = false;
      // console.log("TIMEOUT DONE");
      // console.log("Shake animation after:", shakeAnimation.value);
    }, 500);

    // Save the state of guess count and searchDisable
    const pre = currentBoardFileName.value;
    putItem(pre + "-guesses", JSON.stringify(guesses.value));
    console.log("Search disable test", searchDisable.value);
    putItem(pre + "-searchDisable", JSON.stringify(searchDisable.value));
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

  const element = document.getElementById(
    rowColtoString(row, col) + "-img" // get the ID for the corresponding image component
  );

  searchDisable.value[row][col] = true;

  console.log("ELEMENT", element);

  if (element) {
    const img = document.createElement("img");
    img.src = SERVER_URL + "get_skin_image/" + skin_name;
    /*
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

    // img.style.height = "30%";
    // img.style.width = "auto";
    // img.style.maxWidth = "200px";

    img.style.width = "100%";
    img.style.marginTop = "10%";

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

    backgroundColors.value[row][col] = color;
    console.log(
      "New background color info: ",
      backgroundColors.value[row][col]
    );

    element.appendChild(img);
    console.log("IMAGE ELEMENT: ", img);
    imageHTML.value[row][col] = img.outerHTML;

    console.log(
      "imageHTML",
      imageHTML.value[row][col],
      "outer ",
      img.outerHTML
    );

    // save everything at the end
    const save_prefix = currentBoardFileName.value;
    putItem(`${save_prefix}-guesses`, JSON.stringify(guesses.value));
    putItem(
      `${save_prefix}-searchDisable`,
      JSON.stringify(searchDisable.value)
    );
    putItem(`${save_prefix}-imageHTML`, JSON.stringify(imageHTML.value));
    putItem(
      `${save_prefix}-backgroundColors`,
      JSON.stringify(backgroundColors.value)
    );
    putItem(`${save_prefix}-all_skins`, JSON.stringify(all_skins.value));
  }
  // });
});

// add in events for correct guess, as well as incorrect guess...

const board_data = ref(null);
const all_skins = ref(null);
// NOTE: Things that I will need to keep track of when saving a game:
/*
  all the possible skins: these can change as the data on the backend updates. Want to make sure that new skins are not selectable when it's not a possible answer
  Guesses remaining: easy
  Skins that have already been used
  Which squares have already been guessed: this includes the following:
  - background color for each square
  - image component
  - remember to disable the input to that square
*/

//  Get the unique "all_skins" file associated with the current board
function fetchAllSkins(day, month, year) {
  // if (exists(`${currentBoardString.value}-all_skins`)) {
  //   return get(`${currentBoardString.value}-all_skins`);
  // }

  // check if already exists in indexDB
  exists(`board-${day}-${month}-${year}.json-all_skins`).then((value) =>
    value
      ? getFromIDB(`board-${day}-${month}-${year}.json-all_skins`).then(
          (value) => (all_skins.value = value)
        )
      : fetch(SERVER_URL + `board/all_skins/past/${year}/${month}/${day}`).then(
          (response) => {
            response.json().then((value) => {
              // console.log("fetchAllSkins", value[0].weapon_name, typeof(value[0]));
              let output = [];
              value.forEach((w) => output.push(w.weapon_name));
              console.log("FETCH ALL SKINS: ", output);
              all_skins.value = output;
              // putItem(`${currentBoardString.value}-all_skins`, JSON.stringify(output));
              // exists()
              return output;
            });
          }
        )
  );

  return;

  fetch(SERVER_URL + `board/all_skins/past/${year}/${month}/${day}`).then(
    (response) => {
      response.json().then((value) => {
        // console.log("fetchAllSkins", value[0].weapon_name, typeof(value[0]));
        let output = [];
        value.forEach((w) => output.push(w.weapon_name));
        console.log("FETCH ALL SKINS: ", output);
        all_skins.value = output;
        // putItem(`${currentBoardString.value}-all_skins`, JSON.stringify(output));
        // exists()
        return output;
      });
    }
  );
}

function fetchDailyBoard() {
  // fetch the DAILY board
  console.log("FETCHING DAILY BOARD");
  return fetch(SERVER_URL + "board");
}

function createResetBoardEvent() {
  // event to be emitted when the board is reset
  const resetBoard = new CustomEvent("resetBoard");
  return resetBoard;
}

function createReturnToDailyEvent() {
  return new CustomEvent("returnToDaily");
}

document.addEventListener("resetBoard", (e) => {
  // handle resetting the board

  // for each part of the game state, check if there already exists a value in localStorage
  const b = currentBoardString.value;

  // exists(`${b}-guesses`) ? guesses.value = get(`${b}-guesses`) : guesses.value = MAX_GUESSES;
  // exists(`${b}-backgroundColors`) ? backgroundColors.value = get(`${b}-backgroundColors`) : backgroundColors.value = [['', '', ''],['', '', ''],['', '', ''],];
  // exists(`${b}-searchDisable`) ? searchDisable.value = get(`${b}-searchDisable`) : searchDisable.value = [[false, false, false],[false, false, false],[false, false, false],];
  // exists(`${b}-imageHTML`) ? imageHTML.value = get(`${b}-imageHTML`) : imageHTML.value = [[null,null,null],[null,null,null],[null,null,null]];
  const date = extractDate(b);

  exists(`${b}-guesses`).then((value) =>
    value
      ? getFromIDB(`${b}-guesses`).then((value) => (guesses.value = value))
      : (guesses.value = MAX_GUESSES)
  );
  exists(`${b}-all_skins`).then((value) =>
    value
      ? getFromIDB(`${b}-all_skins`).then(
          (value) => (all_skins.value = JSON.parse(value))
        )
      : fetchAllSkins(date[0], date[1], date[2])
  );
  exists(`${b}-backgroundColors`).then((value) =>
    value
      ? getFromIDB(`${b}-backgroundColors`).then(
          (value) => (backgroundColors.value = JSON.parse(value))
        )
      : (backgroundColors.value = STRING_DEFAULT)
  );
  exists(`${b}-searchDisable`).then((value) =>
    value
      ? getFromIDB(`${b}-searchDisable`).then(
          (value) => (searchDisable.value = JSON.parse(value))
        )
      : (searchDisable.value = BOOL_DEFAULT)
  );
  exists(`${b}-imageHTML`).then((value) =>
    value
      ? getFromIDB(`${b}-imageHTML`).then((value) => {
          imageHTML.value = JSON.parse(value); // Remove the images from each square
          // FIXME: This is a bandaid solution. It seems to work, but I don't like it
          for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
              const element = document.getElementById(
                rowColtoString(r, c) + "-img"
              );
              if (element !== null) {
                Array.from(element.children).forEach((c) => c.remove());
              }
            }
          }
        })
      : (imageHTML.value = NULL_DEFAULT)
  );

  currentBoardFileName.value = currentBoardString.value;
});

function fetchPastBoard(boardName) {
  // fetch information for a past board
  // first, we need to clean the input
  console.log("TESTING FETCH PAST: ", boardName);
  const temp = boardName.split(".")[0].split("-");
  const day = temp[1];
  const month = temp[2];
  const year = temp[3];
  fetch(SERVER_URL + `board/past/${year}/${month}/${day}`).then((response) => {
    if (!response.ok) {
      throw new Error("Network response error when getting game board");
    }
    response.json().then((value) => {
      console.log("TESTING NEW PAST BOARD FUNCTION: ", value);
      // board_data.value = value;
      board_data.value["board"] = value[0];
      board_data.value["row_queries"] = value[1];
      board_data.value["col_queries"] = value[2];
      console.log(
        "board: ",
        // board_data.value[1][0],
        value[0],
        value[1],
        value[2],
        board_data.value["board"],
        board_data.value["row_queries"],
        board_data.value["col_queries"]
      );

      // FIXME : Finish implementing this.
      // i.e. save the current board TODO and make sure that you reset the images and the disabled, and the guesses

      const date = extractDate(currentBoardString.value);

      fetchAllSkins(date[0], date[1], date[2]);

      document.dispatchEvent(createResetBoardEvent());
    });
  });
}

function fetchDailyBoardName() {
  return fetch(SERVER_URL + "board/today")
    .catch((error) => console.log(error))
    .then((response) => {
      console.log(SERVER_URL + "board/today");
      console.log(response);
      console.log(response.value);
      return response.json();
    })
    .then((value) => {
      console.log("Returning this value, ", value);
      return value;
    })
    .catch((error) =>
      console.log(
        "Something went wrong when fetching daily board name: ",
        error
      )
    );
}

/**
 * Extract the date from a board name
 *
 * @param s - input string
 */
function extractDate(s) {
  let o = s.split(".")[0].split("-");
  return [o[1], o[2], o[3]];
}

onMounted(() => {
  fetchDailyBoard()
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

  // Saving the name of the "daily" board, i.e. the front page
  // Retrieving any info about the daily board
  fetchDailyBoardName().then((boardName) => {
    currentBoardString.value = boardName;
    currentBoardFileName.value = boardName;
    dailyBoardName.value = boardName;

    const date = extractDate(boardName);

    fetchAllSkins(date[0], date[1], date[2]);

    putItem("dailyBoardName", boardName);

    exists(`${boardName}-guesses`).then((value) =>
      console.log("TESTING IF EXISTS, ", value)
    );

    exists(`${boardName}-guesses`).then((value) =>
      value
        ? getFromIDB(`${boardName}-guesses`).then(
            (value) => (guesses.value = value)
          )
        : null
    );

    exists(`${boardName}-searchDisable`).then((value) =>
      value
        ? getFromIDB(`${boardName}-searchDisable`).then(
            (value) => (searchDisable.value = JSON.parse(value))
          )
        : null
    );
    exists(`${boardName}-imageHTML`).then((value) =>
      value
        ? getFromIDB(`${boardName}-imageHTML`).then(
            (value) => (imageHTML.value = JSON.parse(value))
          )
        : null
    );

    exists(`${boardName}-backgroundColors`).then((value) =>
      value
        ? getFromIDB(`${boardName}-backgroundColors`).then(
            (value) => (backgroundColors.value = JSON.parse(value))
          )
        : null
    );
    exists(`${boardName}-all_skins`).then((value) =>
      value
        ? getFromIDB(`${boardName}-all_skins`).then(
            (value) => (all_skins.value = JSON.parse(value))
          )
        : null
    );
  });
});

document.addEventListener("returnToDaily", (e) => {
  console.log("Daily board name: ", dailyBoardName.value);
  currentBoardString.value = dailyBoardName.value;
  currentBoardFileName.value = dailyBoardName.value;
  document.dispatchEvent(createResetBoardEvent());
  fetchDailyBoard()
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
});

function returnToDaily() {
  console.log("returning!");
  document.dispatchEvent(createReturnToDailyEvent());
}

const HARD_CUTOFF = 30;
const MED_CUTOFF = 100;

function getBoardDifficulty() {
  const b = board_data.value["board"];
  console.log("Get board diff: ", b);
  const NUM_CELLS = 9;
  let total = 0;
  for (let r = 0; r < b.length; r++) {
    for (let c = 0; c < b[r].length; c++) {
      total += b[r][c].length;
    }
  }
  const average = total / NUM_CELLS;

  console.log("AVERAGE", average);
  if (average < HARD_CUTOFF) {
    return "Hard";
  } else if (average < MED_CUTOFF) {
    return "Medium";
  } else if (!isNaN(average)) {
    return "Easy";
  }

  return null;
}
</script>

<template>
  <div class="container" style="color: white">
    <div class="top-bar">
      <h1>
        CS//<span style="color: cornflowerblue">Grid</span>//<span
          style="color: orange"
          >Game</span
        >
      </h1>
      <div style="display: flex; justify-content: center; gap: 10px">
        <PastBoards />
        <button
          v-if="currentBoardString != dailyBoardName"
          @click="returnToDaily()"
        >
          Return to Board of the Day
        </button>
      </div>
    </div>
    <div v-if="currentBoardString != dailyBoardName">
      <div style="padding-top: 50px">
        Playing board from {{ currentParsedBoardString }}
      </div>
    </div>
    <!-- <video autoplay muted loop style="object-fit: fill; height: 100%; width: 100%; filter: invert() blur(20px); position: absolute; left: 0%; top: 0%; z-index: -100;">
      <source src="../assets/output.mp4" type="video/mp4">
    </video> -->
    <!-- <video autoplay muted loop style="width: 100%; filter: invert() blur(5px); position: absolute; left: 50%; top: -10%; z-index: -100;">
      <source src="../assets/output.mp4" type="video/mp4">
    </video>
    <video autoplay muted loop style="width: 100%; filter: invert() blur(5px); position: absolute; left: -50%; bottom: -10%; z-index: -100;">
      <source src="../assets/output.mp4" type="video/mp4">
    </video>
    <video autoplay muted loop style="width: 100%; filter: invert() blur(5px); position: absolute; left: 50%; bottom: -10%; z-index: -100;">
      <source src="../assets/output.mp4" type="video/mp4">
    </video> -->
    <div v-if="board_data" class="gridgame-board">
      <div id="difficulty">
        <div v-if="getBoardDifficulty() == 'Easy'">
          This board's difficulty is
          <span
            style="
              color: black !important;
              background-color: green;
              border-radius: 5px;
              padding: 2px;
            "
            >EASY</span
          >
        </div>
        <div v-else-if="getBoardDifficulty() == 'Medium'">
          This board's difficulty is
          <span
            style="
              color: black !important;
              background-color: yellow;
              border-radius: 5px;
              padding: 2px;
            "
            >MEDIUM</span
          >
        </div>
        <div v-else-if="getBoardDifficulty() == 'Hard'">
          This board's difficulty is
          <span
            style="
              color: black !important;
              background-color: red;
              border-radius: 5px;
              padding: 2px;
            "
            >HARD</span
          >
        </div>
      </div>
      <!-- We want a 4x4 table 
      Simplest approach: have one div contain 4 smaller flexboxes, which contain all info for a row
      So the outer is a vertically stacked flexbox, and then 4 inner horizontal flexboxes-->
      <div class="board-row" style="color: orange">
        <div class="question" style="opacity: 0">...</div>
        <div class="question">{{ board_data["col_queries"][0] }}</div>
        <div class="question">{{ board_data["col_queries"][1] }}</div>
        <div class="question">{{ board_data["col_queries"][2] }}</div>
      </div>
      <div class="board-row" style="color: cornflowerblue">
        <div class="question">{{ board_data["row_queries"][0] }}</div>
        <SkinSquare
          v-for="c in 3"
          :row="0"
          :col="c - 1"
          :items="all_skins"
          :disabled="searchDisable[0][c - 1]"
          :backgroundColor="backgroundColors[0][c - 1]"
          :shakeText="shakeAnimation[0][c - 1]"
          :imageHtml="imageHTML[0][c - 1]"
        />
      </div>
      <div class="board-row" style="color: cornflowerblue">
        <div class="question">{{ board_data["row_queries"][1] }}</div>
        <SkinSquare
          v-for="c in 3"
          :row="1"
          :col="c - 1"
          :items="all_skins"
          :disabled="searchDisable[1][c - 1]"
          :backgroundColor="backgroundColors[1][c - 1]"
          :shakeText="shakeAnimation[1][c - 1]"
          :imageHtml="imageHTML[1][c - 1]"
        />
      </div>
      <div class="board-row" style="color: cornflowerblue">
        <div class="question">{{ board_data["row_queries"][2] }}</div>
        <SkinSquare
          v-for="c in 3"
          :row="2"
          :col="c - 1"
          :items="all_skins"
          :disabled="searchDisable[2][c - 1]"
          :backgroundColor="backgroundColors[2][c - 1]"
          :shakeText="shakeAnimation[2][c - 1]"
          :imageHtml="imageHTML[2][c - 1]"
        />
      </div>
      <div class="bottom-bar">
        <h2>Guesses left: {{ guesses }}</h2>
      </div>
    </div>
    <div v-else>
      <!-- Optionally show something else if board_data is undefined -->
      <p>Loading or No Data Available</p>
    </div>
  </div>
</template>

<style scoped>
.top-bar {
}
.bottom-bar {
  background: radial-gradient(circle, black 0, transparent 20%);
}
.gridgame-board {
  display: flex;
  flex-direction: column;
  min-height: 70vh;
  gap: 4px;
  height: auto;
}
.board-row {
  display: flex;
  flex-direction: row;
  gap: 4px;
}

@media (min-width: 750px) {
  .question {
    width: 20%;
    aspect-ratio: 1/1;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: large;
    background: radial-gradient(circle, black 0, transparent 80%);
  }

  .container {
    position: relative;
    border-radius: 50px;
    background: radial-gradient(circle, black 0, transparent 80%);
    border-radius: 261px;
    max-width: 1250px;
  }
}

@media (max-width: 750px) {
  .question {
    width: 20%;
    aspect-ratio: 1/1;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: small;
    background: radial-gradient(ellipse, black, transparent);
  }
  .container {
    position: relative;
    border-radius: 50px;
    background: radial-gradient(circle, black, transparent);
    border-radius: 100px;
    max-width: 1250px;
  }
}

#difficulty {
  padding: 10px 0;
}

.square {
  width: 20%;
  aspect-ratio: 1/1;
  border-width: 2px;
  border-color: rgb(201, 201, 153);
  border-radius: 10px;
  border-style: solid;
  position: relative;
  overflow: hidden;
  background-color: rgb(45, 45, 45);
  transition: background-color 0.5s;
}

.square:hover {
  background-color: rgb(112, 112, 112);
}
</style>
