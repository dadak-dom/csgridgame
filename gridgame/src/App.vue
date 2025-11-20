<script setup>
import GameBoard from "./components/GameBoard.vue";
import SearchAutocomplete from "./components/SearchAutocomplete.vue";
import BackgroundAnimation from "./components/BackgroundAnimation.vue";
import Tutorial from "./components/Tutorial.vue";
import Spacer from "./components/Spacer.vue";
import Footer from "./components/Footer.vue";

/*
TODO: Finish the tutorial beautification process. Make sure that it works on mobile
TODO: Make it more clear when the game is over. Idea: add X's over the spaces that were not filled in after you run out of guesses
TODO: Once a game has finished, create a modal that pops up encouraging someone to copy-paste their score
🟥 🟨 🟦 🟪 ⬜ - use these in the modal for the copy/paste! or these: https://www.piliapp.com/emoji/list/heart/ 
TODO: Remove all the debug notes from the console so that people can't cheat that way
*/
// const SERVER_URL = process.env.GRIDGAME_SERVER_URL;
</script>

<template>
  <!-- <BackgroundAnimation /> -->
  <div id="app">
    <GameBoard />
    <Spacer />
    <Tutorial />
    <Footer />
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

<style scoped></style>
