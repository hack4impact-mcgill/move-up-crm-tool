<template>
  <q-card class="event-popup">
    <q-card-section class="row items-center">
      <div class="text-h6">New Coffee Date</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup @click="cancelCoffeeDate" />
    </q-card-section>

    <!-- If user has not opted in -->
    <q-card-section v-if="!user.coffee_dates">
      <p>You have not yet opted in to coffee dates. Would you like to opt in?</p>
      <q-btn color="primary" label="Yes" @click="optInCoffeeDates" />
    </q-card-section>

    <!-- User has opted in to coffee dates -->
    <q-card-section v-else>
      <q-form @submit="confirmCoffeeDate" class="q-gutter-sm">
        <!-- return event description with the other coffee date person -->
        <q-field filled label="Event Description" stack-label>
          <template v-slot:control>
            <div class="self-center q-gutter-sm full-width no-outline" tabindex="0">
              <!-- {{ coffeeDateEvent.description }} -->
            </div>
          </template>
        </q-field>

        <q-field filled label="Event Category" stack-label>
          <template v-slot:control>
            <div class="self-center q-gutter-sm full-width no-outline">Coffee Date</div>
          </template>
        </q-field>

        <!-- return event location for coffee date -->
        <q-field filled label="Event Location" stack-label>
          <template v-slot:control>
            <div class="self-center q-gutter-sm full-width no-outline">
              <!-- {{ coffeeDateEvent.location }} -->
            </div>
          </template>
        </q-field>

        <q-input filled v-model="coffeeTime" label="Time" mask="time" :rules="['time']">
          <template v-slot:append>
            <q-icon name="access_time" class="cursor-pointer"></q-icon>
          </template>
        </q-input>

        <q-input filled v-model="coffeeDate" label="Date" mask="date" :rules="['date']">
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer"></q-icon>
          </template>
        </q-input>

        <q-btn color="primary" type="submit" label="Confirm" />
        <!-- once confirmed this should be add to calendar -->
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import moment from "moment";
export default {
  name: "CoffeeDatePopUp",
  data() {
    return {
      description: "",
      coffeeDateEvent: {},
      coffeeDate: moment(new Date()).format("YYYY/MM/DD"),
      coffeeTime: moment(new Date()).format("h:mm"),
      eventTitle: "",
      eventCategory: "",
      eventLocation: "",
      eventTime: "",
      eventDate: "",
      categories: [],
      user: {}
    };
  },
  created: function() {
    this.$axios.get("/events/categories").then(resp => {
      this.categories = resp.data;
    });
    const user = this.$store.state.currentUser;
    this.$axios.get("/users/" + user.id).then(resp => {
      this.user = resp.data;
      if (user.coffee_dates) {
        this.$axios.get("/events/find-coffee-date/" + user.id).then(resp => {
          this.coffeeDateEvent = resp.data;
          let date_time = new Date(this.coffeeDateEvent.date_time);
          console.log(date_time);
          this.coffeeDate = moment(
            new Date(this.coffeeDateEvent.date_time)
          ).format("YYYY/MM/DD");
          this.coffeeTime =
            date_time.getUTCHours() + ":" + date_time.getUTCMinutes();
        });
      }
    });
  },
  methods: {
    // User confirms coffee date
    addUserToEvent: function() {
      let user = this.$store.state.currentUser;
    },
    // User cancels coffee date
    cancelCoffeeDate: function() {
      this.$axios
        .delete(
          "/events/delete/" + this.coffeeDateEvent.id + "/" + this.user.id
        )
        .then(_resp => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Coffee Date Cancelled"
          });
        });
    },
    confirmCoffeeDate: function() {
      this.$q.notify({
        color: "green-4",
        position: "top",
        textColor: "white",
        icon: "cloud_done",
        message: "Coffee Date Confirmed"
      });
      this.$emit("dialog-closed");
    },
    optInCoffeeDates: function() {
      let data = {
        id: this.user.id,
        coffee: "true"
      };
      this.$axios
        .post("/account/coffee", data, {
          headers: {
            Authorization: this.$store.state.token
          }
        })
        .then(_resp => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Opted In Successfully"
          });
          // let parent know to close the dialog
          this.$emit("dialog-closed");
        })
        .catch(_err => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Something went wrong, please try again"
          });
        });
    },
    createEvent: function() {
      //   const user = this.$store.state.currentUser;
      //   const date_time = moment(
      //     new Date(this.eventDate + " " + this.eventTime)
      //   ).format("DD-MM-YYYY h:mma");
      //   const data = {
      //     event_name: this.eventTitle,
      //     description: this.description,
      //     location: this.eventLocation,
      //     category: this.eventCategory,
      //     date_time: date_time,
      //     host_email: this.$store.state.currentUser.email
      //   };
      //   this.$axios
      //     .get("/events", data, {
      //       headers: {
      //         Authorization: this.$store.state.token
      //       }
      //     })
      //     .then(_resp => {
      //       this.$q.notify({
      //         color: "green-4",
      //         position: "top",
      //         textColor: "white",
      //         icon: "cloud_done",
      //         message: "Coffee Date Confirmed"
      //       });
      //       // let parent know to close the dialog
      //       this.$emit("dialog-closed");
      //     })
      //     .catch(_err => {
      //       this.$q.notify({
      //         color: "red-4",
      //         position: "top",
      //         textColor: "white",
      //         icon: "error",
      //         message: "Something went wrong, please try again"
      //       });
      //     });
    }
  }
};
</script>

<style lang="scss" scoped>
.event-popup {
  min-width: 500px;
}
</style>