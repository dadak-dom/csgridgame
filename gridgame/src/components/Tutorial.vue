<script setup></script>

<template>
  <div class="outer">
    <h1 id="tutorial-start">How do I play?</h1>
    <div class="outer-flex">
      <div class="instructions">
        <div class="step">
          ★ For each cell in the grid above, name a skin for which the
          corresponding row and column hold true
        </div>
        <div class="step">
          <div>
            ★ For example: A skin that is
            <span
              style="
                color: rgb(136, 71, 255);
                /* margin-left: 5px;
                margin-right: 5px; */
              "
            >
              Restricted
            </span>
            and starts with the letter F... the Glock-18 Fade!
            <!-- <img style="width: 5%" src="../assets/images/9-Glock-18 Fade.png" /> -->
          </div>
        </div>
        <div class="step">
          ★ Each square has between 1 and 200 correct answers
        </div>
        <div class="step">
          ★ The goal of this game is to find the
          <span style="color: rgb(0, 255, 0)">most expensive</span> skin for a
          given tile
        </div>

        <div class="step">
          ★ The background of a correctly guessed tile indicates the ranking of
          your guess. <span style="background-color: #b39700">Yellow</span> is
          best, followed by <span style="background-color: #921010">red</span>,
          <span style="background-color: #8d129a">pink</span>,
          <span style="background-color: #38009d">purple</span>,
          <span style="background-color: #001a9c">blue</span>,
          <span style="background-color: #1f4e83">light-blue</span>, and
          <span style="background-color: #636b6d">grey</span>.
        </div>
        <div class="step">
          ★ Note: once a skin has been used, it <u>cannot be used again</u>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.outer-flex {
  display: flex;
  text-align: left;
  gap: 10px;
}
.outer {
  color: white;
  position: relative;
  z-index: 100;
  width: 80%;
  left: 50%;
  transform: translateX(-50%);
}
.instructions {
  display: flex;
  justify-content: left;
  flex-direction: column;
  float: left;
  position: relative;
}
.step {
  /* border: 1px rgb(255, 77, 0) solid; */
  padding-top: 1vh;
  padding-bottom: 1vh;
  float: left;
  position: relative;

  /* font-family: "Times New Roman", Times, serif; */
}
</style>
