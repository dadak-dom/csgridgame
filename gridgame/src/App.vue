<script setup>
import GameBoard from "./components/GameBoard.vue";
import HelloWorld from "./components/HelloWorld.vue";
import SearchAutocomplete from "./components/SearchAutocomplete.vue";
</script>

<template>
  <div id="app">
    <GameBoard />
    <button @click="fetchBoard">Fetch board</button>
    <button @click="genBoard">Generate new board</button>
    <button @click="queryCheck">Check queries</button>
    <p v-if="data">{{ data }}</p>
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
    async fetchBoard() {
      const response = await fetch("http://127.0.0.1:8000/board");
      console.log(await response.json());
      this.data = response;
    },
    genBoard() {
      fetch("http://127.0.0.1:8000/genboard");
    },
    queryCheck() {
      fetch("http://127.0.0.1:8000/queries").then((response) => {
        response.json().then((value) => {
          console.log(value);
        });
      });
    },
  },
};
</script>

<style scoped>
.logo {
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
}
</style>
