<script setup>
/*
 Everything that occurs EXCLUSIVELY in a square (skin image, typing a guess, etc.)
 Should be done in here. 
 Everything else (keeping track of guesses, whatever...) should be done in the parent (GameBoard)
 */
import SearchAutocomplete from "./SearchAutocomplete.vue";
import SkinImage from "./SkinImage.vue";

const square = "square"; // Makes the CSS actually work
</script>

<template>
  <div :class="['square', { shake: shakeText }]" :style="{ backgroundColor }">
    <SkinImage
      :row="row"
      :col="col"
      :imageHtml="imageHtml"
      class="skin-image"
    />
    <SearchAutocomplete
      :items="items"
      :row="row"
      :col="col"
      :disabled="disabled"
    />
  </div>
</template>

<script>
export default {
  name: "SkinSquare",
  props: {
    row: {
      type: Number,
      required: true,
    },
    col: {
      type: Number,
      required: true,
    },
    backgroundColor: {
      type: String,
      required: true,
    },
    items: {
      type: Array,
      required: false,
      default: () => [],
    },
    disabled: {
      type: Boolean,
      required: true,
    },
    shakeText: {
      type: Boolean,
      required: true,
    },
    imageHtml: {
      type: String,
      required: false,
    },
  },
  methods: {
    // getImage(skin_name) {
    //   console.log("IN SKINIMAGE COMP:", skin_name);
    // },
  },
};
</script>

<style>
img {
  background-size: contain;
}
.square {
  position: relative;
  cursor: pointer;
}
.skin-image {
  position: absolute;
  /* left: 50%; */
  /* top: 50%; */
  /* transform: translate(-50%, -50%); */
  aspect-ratio: 1/1;
  width: 100%;
  /* margin: auto; */
}
.shake {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) infinite both;
  /* animation: shake infinite cubic-bezier(0.36, 0.07, 0.19, 0.97) both; */
  transform: translate3d(0, 0, 0);
  background-color: grey;
}

@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
    background-color: grey;
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
    background-color: rgb(136, 35, 35);
  }
}
</style>
