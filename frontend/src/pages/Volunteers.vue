<!--Volunteers Table-->
<template>
  <div class="q-pa-md q-gutter-sm">
    <q-table
      class="table-width"
      title="Volunteers"
      :data="volunteers"
      :columns="columns"
      :filter="filter"
      selection="multiple"
      :selected.sync="selected"
      row-key="email"
      wrap-cells
    >
      <template v-slot:top-right>
        <q-input
          borderless
          dense
          debounce="300"
          v-model="filter"
          placeholder="Search"
        >
          <template v-slot:append>
            <q-icon name="search"></q-icon>
          </template>
        </q-input>
      </template>
    </q-table>
    <!-- Email Volunteer Button -->
    <div class="q-pa-md email-btn">
      <q-btn
        icon="email"
        label="Email Selected Volunteers"
        stack
        color="accent"
        style="padding: 7px;"
        @click="getSelectedEmail"
      />

      <q-dialog v-model="showEmailPopup">
        <EmailPopup
          :selected="selected"
          :allEmails="allEmails"
          @dialog-closed="showEmailPopup = false"
        />
      </q-dialog>
    </div>
  </div>
</template>

<script>
import EmailPopup from "../components/EmailPopup.vue";

export default {
  name: "Volunteers",
  components: { EmailPopup },
  data() {
    return {
      showEmailPopup: false,
      allEmails: [],
      volunteers: [],
      filter: "",
      selected: [],
      //Columns of Table
      columns: [
        {
          name: "name",
          required: true,
          label: "Name",
          align: "left",
          field: row => row.name
        },
        {
          name: "email",
          align: "left",
          label: "Email",
          field: "email"
        },
      ]
    };
  },
  methods: {
    //Get all volunteers from backend
    getVolunteers() {
      this.$axios
        .get("/mentors")  //volunteers == mentors
        .then(res => {
          this.volunteers = res.data;
          // Add all of volunteers' emails into allEmails list
          this.volunteers.forEach(element => {
            this.allEmails.push(element.email);
          });
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
    },
    getSelectedEmail: function() {
      this.showEmailPopup = true;
    }
  },
  created() {
    this.getVolunteers();
  }
};
</script>

<style scoped lang="sass">
.email-btn
  float: right
  margin: 30px

.table-width
  margin: 25px
</style>
