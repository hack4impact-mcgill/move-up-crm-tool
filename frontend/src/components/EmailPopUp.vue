<template>
  <q-card class="bg-white text-primary event-popup">
    <q-bar class="email-bar">
      <div class="text-h6">New Message</div>
      <q-space />
      <q-btn dense flat icon="close" v-close-popup></q-btn>
    </q-bar>
    <q-card-section>
      <div>
        <q-chip
          removable
          color="primary"
          @remove="removeChip($event)"
          v-for="email in emails"
          :key="email"
        >{{ email }}</q-chip>
      </div>
      <q-input v-model="text" label="Subject" />
      <q-input v-model="text" type="textarea" />
      <q-btn class="send-btn text-black" color="primary" type="submit" label="Send" />
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "EmailPopUp",
  data() {
    return {
      emails: []
    };
  },
  props: {
    selected: []
  },
  created: function() {
    this.selected.forEach(element => {
      this.emails.push(element.email);
    });
    console.log(this.emails);
  },
  methods: {
    log(email) {
      console.log(`${email} has been removed`);
    },
    removeChip(event) {
      event.value = false;
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
}
</style>