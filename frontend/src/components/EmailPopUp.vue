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
          :options="allClientEmails"
          use-chips
          use-input
          input-debounce="0"
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
    // this.allEmails.forEach(e => {
    //   this.allClientEmails.push(e);
    // });
    this.allClientEmails = this.allEmails;
    console.log("hello " + this.allClientEmails);
  },
  methods: {
    log(email) {
      console.log(`${email} has been removed`);
    }
    // filterFn(val, update) {
    //   update(() => {
    //     if (val === "") {
    //       this.filterOptions = this.allClientEmails;
    //     } else {
    //       const needle = val.toLowerCase();
    //       this.filterOptions = this.allClientEmails.filter(
    //         v => v.toLowerCase().indexOf(needle) > -1
    //       );
    //     }
    //   });
    // }
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