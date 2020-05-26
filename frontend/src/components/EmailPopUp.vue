<template>
  <q-card class="bg-white text-white event-popup">
    <q-bar class="email-bar">
      <div class="text-h6">New Message</div>
      <q-space />
      <q-btn dense flat icon="close" v-close-popup></q-btn>
    </q-bar>
    <q-card-section>
      <!-- Email form  -->
      <q-form @submit="sendEmail" class="q-gutter-md">
        <q-select
          v-model="selectedEmails"
          label="To"
          :options="filterOptions"
          multiple
          use-chips
          use-input
          input-debounce="0"
          @new-value="createRecipient"
          @filter="filterEmails"
          stack-label
          lazy-rules
          :rules="[
            val =>
              (val && val.length > 0) || 'Please enter at least one recipient'
          ]"
        />
        <q-input
          v-model="subject"
          label="Subject"
          lazy-rules
          :rules="[val => (val && val.length > 0) || 'Please enter a subject']"
        />
        <q-input v-model="msg" label="Body" type="textarea"></q-input>
        <q-btn
          class="send-btn text-white"
          :disabled="submitting"
          type="submit"
          label="Send"
        />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "EmailPopup",
  data() {
    return {
      submitting: false,
      selectedEmails: [],
      allClientEmails: [],
      subject: null,
      msg: null,
      filterOptions: this.allEmails
    };
  },
  // Selected email and all clients' emails from Clients page
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
    // Allowing user to add new email recipients that is on the list
    createRecipient(newRecipient, done) {
      if (newRecipient.length > 0) {
        if (!this.allClientEmails.includes(newRecipient)) {
          this.allClientEmails.push(newRecipient);
          this.selectedEmails.push(newRecipient);
        }
        done(newRecipient, "toggle");
      }
    },
    // Allowing user to find an email quicker by filtering through the list of all emails
    filterEmails(val, update) {
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
    },
    // calling flask-email API
    sendEmail() {
      this.submitting = true;
      this.$axios
        .post("/send-email", {
          recipients: this.selectedEmails,
          subject: this.subject,
          body: this.msg
        })
        .then(() => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Successfully Sent Email"
          });
          this.submitting = false;
          this.$emit("dialog-closed");
        })
        .catch(() => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Something went wrong, please try again"
          });
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
