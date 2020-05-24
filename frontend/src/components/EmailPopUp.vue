<template>
  <q-card class="bg-white text-white event-popup">
    <q-bar class="email-bar">
      <div class="text-h6">New Message</div>
      <q-space />
      <q-btn dense flat icon="close" v-close-popup></q-btn>
    </q-bar>
    <q-card-section>
      <div>
        <q-select
          v-model="selectedEmails"
          multiple
          :options="filterOptions"
          use-chips
          use-input
          input-debounce="0"
          @new-value="createValue"
          @filter="filterFn"
          stack-label
          label="To"
        />
        <!--           @new-value="createValue"
        @filter="filterFn"-->
      </div>
      <q-input v-model="subject" label="Subject" />
      <q-input v-model="msg" type="textarea" />
      <q-btn class="send-btn text-white" type="submit" label="Send" />
    </q-card-section>
  </q-card>
</template>

<script>
// const allClientEmails = this.allEmails;
export default {
  name: "EmailPopup",
  data() {
    return {
      test: null,
      selectedEmails: [],
      allClientEmails: [],
      subject: null,
      msg: null,
      filterOptions: this.allEmails
    };
  },
  props: {
    selected: Array,
    allEmails: Array
  },
  created: function() {
    this.selected.forEach(element => {
      this.selectedEmails.push(element.email);
    });
    this.allClientEmails = this.allEmails;
  },

  methods: {
    createValue(val, done) {
      // Calling done(var) when new-value-mode is not set or is "add", or done(var, "add") adds "var" content to the model
      // and it resets the input textbox to empty string
      // ----
      // Calling done(var) when new-value-mode is "add-unique", or done(var, "add-unique") adds "var" content to the model
      // only if is not already set and it resets the input textbox to empty string
      // ----
      // Calling done(var) when new-value-mode is "toggle", or done(var, "toggle") toggles the model with "var" content
      // (adds to model if not already in the model, removes from model if already has it)
      // and it resets the input textbox to empty string
      // ----
      // If "var" content is undefined/null, then it doesn't tampers with the model
      // and only resets the input textbox to empty string

      if (val.length > 0) {
        if (!this.allClientEmails.includes(val)) {
          this.allClientEmails.push(val);
        }
        done(val, "toggle");
      }
    },
    filterFn(val, update) {
      update(() => {
        if (val === "") {
          this.filterOptions = this.allClientEmails;
        } else {
          const needle = val.toLowerCase();
          this.filterOptions = this.allClientEmails.filter(
            v => v.toLowerCase().indexOf(needle) > -1
          );
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.event-popup {
  min-width: 750px;
}
.email-bar {
  background-color: #404040;
  font-weight: bolder;
  padding: 10px 15px;
  height: auto;
}
.send-btn {
  float: right;
  margin: 10px 0px;
  background-color: #404040;
}
</style>