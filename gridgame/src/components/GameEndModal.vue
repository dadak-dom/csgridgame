<script setup>
import { ref } from "vue";
const showModal = ref(false);
const copiedText = ref(false); // should become true when the text gets copied

// TODO - Make this only show up when the game is over - should also only happen when transitioning from 1 to 0 guesses (OR IF THE ENTIRE BOARD IS FILLED!)
// TODO - Make a function that converts the colors to the emoji hearts. Also, make it so that there's a button that adds it to clipboard
document.addEventListener("noGuessesLeft", (e) => {
  console.debug("Open GameEndModal")
  showModal.value = true;
});

function copyText(score) {
  const text = document.getElementById("results-text");
  // text.select();
  // text.setSelectionRange(0, 99999);
  let o = `Beat my score of ${score} on CSGridGame!\n\n`
  navigator.clipboard.writeText(o + text.innerText + "\n🌐→cdgridgame.com");
  console.debug("copy-paste-text: ", o + text.innerText)
  copiedText.value = true;
  setTimeout(() => copiedText.value = false, 2000)
}

function backgroundColorsToString(backgroundColorsArray) {
  let output = "";
  for(let r = 0; r < backgroundColorsArray.length; r++) {
    for (let c = 0; c < backgroundColorsArray[r].length; c++) {
      let color = backgroundColorsArray[r][c]
      if (color == "#570102") {
        output += "✖️ "
      }
      else if(color == "#b39700") {
        output += "💛 "
      }
      else if(color == "#921010") {
        output += "❤️ "
      }
      else if(color == "#8d129a") {
        output += "🩷 "
      }
      else if(color == "#38009d") {
        output += "💜 "
      }
      else if(color == "#001a9c") {
        output += "💙 "
      }
      else if(color == "#1f4e83") {
        output += "🩵 "
      }
      else if(color == "#636b6d") {
        output += "🩶 "
      }
      console.debug("copy-paste-output: ", output)
    }
    output += "\n"
  }
  return output;
}

</script>

<template>
  <div class="modal-overlay" v-if="showModal">
    <div class="modal-content">
      <div class="modal-content-inner">
      <div style="display: flex; justify-content: right">
        <!-- <div class="x-button" @click.self="showModal = true">✖️</div> -->
         <img class="x-button" @click.self="showModal = false" src="../assets/icons/xmark-circle.svg"/>
      </div>
      <div id="score-text">Good work! You got {{ score }} points.</div>
      <div id="score-text">Share your score to compete with your friends!</div>
      <div class="copy-paste-score-box">
        <div id="copy-paste-icon" @click="copyText(score)">
          <img class="icon" src="../assets/icons/copy.svg" v-if="!copiedText"></img>
          <img class="icon" src="../assets/icons/check-square.svg" v-else></img>
          <div id="copy" v-if="!copiedText">Copy</div>
          <div id="copy" v-else style="color: green">Copied!</div>
        </div>
        <div id="results-text-wrapper">
          <div id="results-text">
            {{ backgroundColorsToString(backgroundColors) }}
          </div>
        </div>
      </div>
      </div>
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
    score: {
      type: Number,
      required: true,
    }
  },
  methods: {},
};
</script>

<style>
#score-text {
  color: white;
  padding: 10px 0;
}

#results-text {
  white-space: pre-line;
  /* margin-top: 30px; */
}

#copy {
  justify-self: right;
  filter:invert()
}

.icon {
  width: 20%;
}

#results-text-wrapper {
  background-color: #303033;
  position: relative;
  width: fit-content;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px;
  margin-top: 20px;
  border-radius: 10px;
}

#copy-paste-icon {
  /* width: 5%; */
  justify-self: left;
  margin-left: 5%;
  margin-top: 5%;
  padding: 5px 10px;
  filter:invert();
  background-color: #5a5c66;
  border-radius: 10px;
  position: relative;
  width: 40%;
  display: flex;
  cursor: pointer;
}

.copy-paste-score-box {
  background-color: #51535e;
  /* display: grid; */
  border-radius: 10px;
  position: relative;
  left: 5%;
  width: 90%;
  padding: 10px 0 30px 0;
}

.modal-content-inner {
  /* margin: 10px; */
  background-color: #303033;
  border-radius: 10px;
  position: relative;
  padding-bottom: 20px;
}

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
  background: #242323;
  padding: 20px;
  border-radius: 8px;
  max-height: 80vh;
  /* min-height: 40vh; */
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
  /* width: unset; */
  position: relative;
  width: 10%;
  filter: invert();
  cursor: pointer;
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
