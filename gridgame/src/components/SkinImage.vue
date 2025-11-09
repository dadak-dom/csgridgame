<!-- Implement the actual images here... -->

<template>
  <div>
    <div v-if="imageHtml == null" :id="row + '' + col + '-img'">{{imageHtml}}</div>
    <!-- FIXME : Having trouble getting the image to get saved -->
    <div v-if="imageHtml != null && !checkImage(row + col + '-img')" v-html="imageHtml"></div>
  </div>
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
    imageHtml: {
      type: String,
      required: false,
    }
  },
  methods: {
    getImage(skin_name) {
      console.log("IN SKINIMAGE COMP:", skin_name);
    },

    // check if an image has been inserted, 
    checkImage(id) {
      const e = document.getElementById(id);
      if(e != null) {console.log("e.children", e.children);}
      if (e != null && e.children.length > 0) {
        return true;
      }
      return false;
    }
  },
};
</script>

<style>
div {
  /* background-size: contain; */
  width: 100%;
}
</style>
