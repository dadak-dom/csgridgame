<script setup>

import {ref, onMounted, onBeforeUnmount} from "vue";

const images = import.meta.glob('../assets/images/*.png', { eager: true })
// console.log('IMAGES:', typeof(images))
// console.log(Object.entries(images)[0])
const imageList = Object.entries(images)
console.log("IMAGE LIST", imageList[0][1].default);
const offset = ref(100);
// const windowHeight = ref(window.innerHeight);

const windowHeight = ref(window.innerHeight)

const updateHeight = () => {
  windowHeight.value = window.innerHeight;
  console.log("RESIZE")
  if (document.body.clientWidth > 750) {
    // anim = 2;
    animSize.value = 2;
  }
  else {
    // anim = 1;
    animSize.value = 1;
  }
}

onMounted(() => {
  window.addEventListener('resize', updateHeight)
  document.getElementById("background-video").playbackRate = 0.5;
  if (document.body.clientWidth > 750) {
    animSize.value = 2
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateHeight)
})

const animSize = ref(2);

if (document.body.clientWidth < 750) {
  animSize.value = 1;
}



</script>

<template>
  <!-- <div class="animation-wrapper">
    <div class="animation-row" v-for="index in (Math.floor(windowHeight / 40))">
      <div 
        class="skin"
        v-for="(image, i) in imageList"
        :key="path"
        :style="{ // animationDelay: `${i * 0.5 }s`,
                  top: `${index * 40}px`,
                  left: `${-50  + i * 2}%`
                  // animationName: (index % 2 != 0 ? 'moveLeft' : 'moveRight')
         }"
      >
        <img :src="image[1].default" />
      </div>
    </div>
  </div> -->
  <div class="background-wrapper">
    <!-- <video autoplay muted loop id="background-video" v-for="i in animSize">
      <source src="../assets/videos/background_video.mp4" type="video/mp4">
    </video> -->
  </div>
</template>


<style scoped>

.background-wrapper {
  /* width: 200%; */
  /* height: 200%; */
  /* overflow: hidden; */
  overflow-x: hidden;
  /* position: absolute; */
  /* left: -100%; */
  /* max-width: 1250px; */
  /* clip-path: margin-box; */
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

#background-video {
  
  /* width: 400vw; */
  /* height: 100%; */
  /* top: 10%; */
  filter: grayscale() blur(10px);
  /* clip-path: 0 0; */
  /* clip-path: view-box; */
}

.animation-wrapper {
  position: relative;
  width: 100vw;
  height: 100px;
  /* overflow: hidden; */
  /* filter: blur(2px) */
}

.animation-row {
  position: relative;
  display: flex;
  align-items: center;
}

.skin {
  position: fixed;
  top: 0;
  animation: spin 20s linear infinite;
  animation-duration: 20s;
  animation-fill-mode: both;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  filter: blur(2px) grayscale();
}

img {
  /* height: 40px; */
  /* width: 40px; */
  /* margin-right: 10px; optional spacing between skins */
}

@keyframes moveRight {
  0% {
    transform: translateX(-100vw);
  }
  100% {
    transform: translateX(100vw);
  }
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes moveLeft {
  0% {
    transform: translateX(100vw);
  }
  100% {
    transform: translateX(-100vw);
  }
}


</style>

