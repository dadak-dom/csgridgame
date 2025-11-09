<template>
  <div class="autocomplete">
    <input
      v-model="search"
      @input="onChange"
      @focus="isOpen = true"
      type="text"
      :disabled="disabled"
      class="text-input"
    />
    
    <div v-if="isOpen" class="modal-overlay" @click.self="isOpen = false">
      <div class="modal-content">
        <p class="user-search"> {{ search }}<span class="blinking-cursor">|</span></p>
        <ul class="autocomplete-results">
          <li
            v-for="(result, i) in results"
            :key="i"
            @click="setResult(result)"
            class="autocomplete-result"
          >
            {{ result }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
// const guessEvent = new CustomEvent("userGuessed", {
//   detail: {
//     name :
//   }
// });
export default {
  name: "SearchAutocomplete",
  props: {
    disabled: {
      type: Boolean,
      required: true,
      default: () => false,
    },
    items: {
      type: Array,
      required: false,
      default: () => [],
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
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  destroyed() {
    document.removeEventListener("click", this.handleClickOutside);
  },
  data() {
    return {
      search: "",
      results: [],
      isOpen: false,
    };
  },
  methods: {
    setResult(result) {
      console.log("chosen", result);
      this.search = result;
      this.isOpen = false;
      // Need to implement something that checks whether the player has already guessed a skin
      document.dispatchEvent(this.createGuessEvent(result));
      setTimeout(() => {
        console.log("Am I disabled?", this.disabled);
        if (!this.disabled) {
          this.search = "";
        }
      }, 100);
    },
    filterResults() {
      this.results = this.items.filter(
        (item) => item.toLowerCase().indexOf(this.search.toLowerCase()) > -1
      );
    },
    onChange() {
      this.filterResults();
      this.isOpen = true;
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.isOpen = false;
      }
    },
    createGuessEvent(skin) {
      const guessEvent = new CustomEvent("userGuessed", {
        detail: {
          name: skin,
          row: this.row,
          col: this.col,
        },
      });
      return guessEvent;
    },
    testFunc(event) {
      console.log("PLEASE WORK");
    },
  },
};
</script>

<style>
.autocomplete {
  position: relative;
  height: 100%;
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
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-height: 60vh;
  overflow-y: auto;
  width: 90%;
  max-width: 400px;
}

/* Results styling */
.user-search {
  color: black;
}

.text-input {
  opacity: 0;
  height: 100%;
  width: 100%;
}

.autocomplete-results {
  list-style: none;
  padding: 0;
  margin: 0;
}

.autocomplete-result {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  color: #e4840f;
  background-color: #4a506b;
}

.autocomplete-result:hover {
  background-color: #4aae9b;
  color: white;
}

@keyframes blink {
  from {opacity: 1.0;}
  to {opacity: 0.0;}
}

.blinking-cursor {
  color: black;
  opacity: 1.0;
  animation: blink 1s ease-in-out 0s infinite both;
}


</style>
