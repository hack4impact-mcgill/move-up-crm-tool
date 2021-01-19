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
    <!-- Copy Volunteer Emails Button -->
    <div class="q-pa-md email-btn">
      <q-btn
        icon="email"
        label="Copy Selected Emails"
        stack
        color="accent"
        style="padding: 7px;"
        @click="copySelectedEmails"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "Volunteers",
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
        }
      ]
    };
  },
  methods: {
    //Get all volunteers from backend
    getVolunteers() {
      this.$axios
        .get("/mentors") //volunteers == mentors
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
    copySelectedEmails: function() {
      const selectedEmails = this.selected.map(item => item.email);
      const selectedEmailsString = selectedEmails.join(", ");
      navigator.clipboard.writeText(selectedEmailsString);

      this.$q.notify({
        color: "grey-10",
        position: "top",
        textColor: "white",
        icon: "assignment_turned_in",
        message: "Emails copied to clipboard"
      });
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
