<!-- Implement the actual images here... -->

<template>
  <div :id="row + '' + col + '-img'"></div>
</template>

<script>
export default {
  name: "SkinImage",
  props: {
    skin_name: {
      type: String,
      required: false,
    },
    row: {
      type: Number,
      required: true,
    },
    col: {
      type: Number,
      required: true,
    },
  },
  methods: {
    getImage(skin_name) {
      console.log("IN SKINIMAGE COMP:", skin_name);
    },
  },
};
</script>

<style>
img {
  background-size: contain;
}
</style>
