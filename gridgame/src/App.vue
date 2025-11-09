<script setup>
import GameBoard from "./components/GameBoard.vue";
import SearchAutocomplete from "./components/SearchAutocomplete.vue";
import BackgroundAnimation from "./components/BackgroundAnimation.vue";
import Tutorial from "./components/Tutorial.vue";

// const SERVER_URL = process.env.GRIDGAME_SERVER_URL;
</script>

<template>
  <!-- <BackgroundAnimation /> -->
  <div id="app">
    <GameBoard />
    <!-- <button @click="fetchBoard">Fetch board</button>
    <button @click="genBoard">Generate new board</button>
    <button @click="queryCheck">Check queries</button> -->
    <!-- <p v-if="data">{{ data }}</p> -->
     <Tutorial />
  </div>
</template>

<script>
export default {
  name: "App",
  components: {
    SearchAutocomplete,
    GameBoard,
  },
  methods: {
    // async fetchBoard() {
    //   const response = await fetch(SERVER_URL + "board");
    //   console.log(await response.json());
    //   this.data = response;
    // },
    // genBoard() {
    //   fetch(SERVER_URL + "genboard");
    // },
    // queryCheck() {
    //   fetch(SERVER_URL + "queries").then((response) => {
    //     response.json().then((value) => {
    //       console.log(value);
    //     });
    //   });
    // },
  },
};
</script>

<style scoped>
/* TODO: Add mobile styling */
/* .logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
} */
</style>
