<!-- Button that, when clicked, shows a list of past boards that can be loaded -->

<script setup>
  import {ref} from "vue";
  // import { SERVER_URL   } from "./GameBoard.vue";

  //FIXME : SERVERURL should be in a constants file or a .env file or something
  // const SERVER_URL = "http://localhost:8000/";
  const SERVER_URL = import.meta.env.VITE_GRIDGAME_SERVER_URL;
  const pastBoardList = ref(null); // this one contains the nice list for user viewing
  const pastRawBoardList = ref(null); // contains raw format (e.g. 8-14-2025) for August 14th, 2025

  const guessCache = ref({});

  const showModal = ref(false);
  function rawDateMapper(boardName) {
    // FIXME: Not sure if I need this
    // helper function
    // given a board name, extract the date
    // board-DAY-MONTH-YEAR.json -> DAY-MONTH-YEAR
    return boardName.split('.')[0].split('-')
  }
  function dateMapper(boardName) {
      // helper function, takes the board names and outputs a 
      // more readable version
      let temp = boardName.split('.')[0].split('-');
      let output = "";
      switch(temp[2]) {
        case "1":
          output += "January";
          break;
        case "2":
          output += "February";
          break;
        case "3":
          output += "March";
          break;
        case "4":
          output += "April";
          break;
        case "5":
          output += "May";
          break;
        case "6":
          output += "June";
          break;
        case "7":
          output += "July";
          break;
        case "8":
          output += "August";
          break;
        case "9":
          output += "September";
          break;
        case "10":
          output += "October";
          break;
        case "11":
          output += "November";
          break;
        case "12":
          output += "December";
          break;
      }

      output += ' ' + temp[1] + ', ' + temp[3];
      return output;
  }

  function getPastBoards() {
  fetch(SERVER_URL + "board/past/list").then((response) => {
    response.json().then((value) => {
      pastRawBoardList.value = value;
      pastBoardList.value = value.map(b => dateMapper(b));
      showModal.value = true;

      // Preload guesses and populate the cache
      value.forEach(rawName => {
        get2(`${rawName}-guesses`)
          .then((val) => {
            guessCache.value[rawName] = val;
          })
          .catch(() => {
            guessCache.value[rawName] = null;
          });
        });
      });
    });
  }


  function get2(key) {
  // return JSON.parse(localStorage.getItem(key));
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
        console.log("Running get2 on key: ", key ," result: ", d)
        if (d != undefined) {
          resolve(d.data);
        } else {
          resolve(null);
        }
      };

      getRequest.onerror = () => {
        reject(getRequest.error);
      };
    };
  });
}

  function peakAtGuesses(rawBoardName) {
    // get the guesses on the board, if they exist
    console.log("RUNNING PEAK AT GUESS FOR ", rawBoardName)
    get2(`${rawBoardName}-guesses`).then((value) => guessCache.value[rawBoardName] = value).catch(guessCache.value[rawBoardName] = null )

  }
</script>

<template>
  <button @click="getPastBoards()">Click here for past boards!</button>
  <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
    <div class="modal-content">
      <ul class="past-boards-list">
        <li v-for="(b, i) in pastBoardList"
        :key="i"
        @click="setResult(pastRawBoardList[i], b); showModal = false"
        class="past-boards-list-item">
          {{ b }} <span v-if="guessCache[pastRawBoardList[i]] != null" style="float:right"> {{ guessCache[pastRawBoardList[i]] }} guesses left</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "PastBoards",
  // props: {
  //   server_url: {
  //     type: String,
  //     required: true,
  //   },
  //   row: {
  //     type: Number,
  //     required: true,
  //   },
  //   col: {
  //     type: Number,
  //     required: true,
  //   },
  // },
  methods: {
    setResult(raw, parsed) {
      console.log("Past board chosen: ", raw)
      console.log("Raw: ", 
      //pastRawBoardList.value[result], 
      "\nPretty: ",
      // pastBoardList.value[result]
      );
      document.dispatchEvent(this.createPastBoardEvent(raw, parsed));
    },
    createPastBoardEvent(raw, parsed) {
      console.log("Emitting an event with the boardname: ", raw);
      const pastBoardEvent = new CustomEvent("pastBoardChosen", {
        detail: {
          rawBoardName: raw,
          parsedBoardName: parsed,
        }
      });
      return pastBoardEvent;
    }
  },
};
</script>

<style>
/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* Modal content box */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-height: 60vh;
  overflow-y: auto;
  width: 90%;
  max-width: 400px;
}
.past-boards-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.past-boards-list-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  color: #e4840f;
  background-color: #4a506b;
  text-align: left;
}

</style>
