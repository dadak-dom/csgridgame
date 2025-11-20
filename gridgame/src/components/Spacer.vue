<script setup></script>

<template>
  <div class="outer-flex">
  <div class="inner-flex">
    <img src="../assets/images/13-MP9 Bulldozer.png" class="spacer-image"></img>
    <img src="../assets/images/9-Glock-18 Fade.png" class="spacer-image"></img>
    <img src="../assets/images/8-AUG Hot Rod.png" class="spacer-image"></img>
  </div>
  </div>
</template>

<style scoped>
.outer-flex {
  display: flex;
  justify-content: center;
  max-width: 1250px;
}
.inner-flex {
  color: white;
  position: relative;
  z-index: 100;
  /* padding-top: 10%;
  padding-bottom: 10%; */
  max-width: 400px;
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh;
  position: relative;
}
.spacer-image {
  transform: rotateX(45deg);
  animation: spin 4s infinite ease-in-out;
  /* width: 15%; */
  position: relative;
  width: 30%;
  aspect-ratio: 1/1;
}

@keyframes spin {
  from {transform: rotateY(0deg);}
  to {transform: rotateY(360deg);}
}
</style>
