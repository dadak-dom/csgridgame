<script setup>
</script>

<template>
 <div class="outer">
  <h1>How do I play?</h1>
  <div class="instructions">
    <div class="step">test</div>
    <div class="step">test</div>
  </div>
 </div>
</template>

<style scoped>
.outer {
  color: white;
  position: relative;
  z-index: 100;
  padding-top: 200px;
  max-width: 1250px;
}
.instructions {
  display: flex;
  justify-content: left;
  flex-direction: column;
}
.step {
  border: 1px red solid;
  padding-top: 100px;
  padding-bottom: 100px;
}
</style>
