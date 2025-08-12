<template>
  <div class="autocomplete">
    <input
      v-model="search"
      @input="onChange"
      type="text"
      :disabled="disabled"
    />
    <ul v-show="isOpen" class="autocomplete-results">
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
}

.autocomplete-results {
  padding: 0;
  margin: 0;
  border: 1px solid #eeeeee;
  height: 120px;
  min-height: 1em;
  max-height: 6em;
  overflow: auto;
}

.autocomplete-result {
  list-style: none;
  text-align: left;
  padding: 4px 2px;
  cursor: pointer;
}

.autocomplete-result:hover {
  background-color: #4aae9b;
  color: white;
}
</style>
