<script setup>
import { ref } from "vue";
const showModal = ref(false);

// TODO - Make this only show up when the game is over - should also only happen when transitioning from 1 to 0 guesses (OR IF THE ENTIRE BOARD IS FILLED!)
// TODO - Make a function that converts the colors to the emoji hearts. Also, make it so that there's a button that adds it to clipboard
document.addEventListener("noGuessesLeft", (e) => {
  showModal.value = true;
});
</script>

<template>
  <div class="modal-overlay" v-if="showModal">
    <div class="modal-content">
      <div style="display: flex; justify-content: right">
        <div class="x-button" @click.self="showModal = false">✖️</div>
      </div>
      <div>{{ backgroundColors[0][0] }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GameEndModal",
  props: {
    backgroundColors: {
      type: Array,
      required: true,
    },
  },
  methods: {},
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
  overflow-y: hidden;
  width: 90%;
  max-width: 400px;
}
.past-boards-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.x-button {
  transform: scale(1);
  transition: transform 0.2s ease-in-out;
  width: unset;
}

.x-button:hover {
  transform: scale(1.5);
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
