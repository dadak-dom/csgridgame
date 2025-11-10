<script setup></script>

<template>
  <div class="outer">
    <h1>How do I play?</h1>
    <div class="instructions">
      <div class="step">
        For each cell in the grid above, name a skin for which the corresponding
        row and column hold true
      </div>
      <div class="step">Once a skin has been used, it cannot be used again</div>
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
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
