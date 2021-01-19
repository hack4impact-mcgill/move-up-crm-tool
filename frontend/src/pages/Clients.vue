<!--Client Table-->
<template>
  <div class="q-pa-md q-gutter-sm">
    <q-table
      class="table-width"
      title="Clients"
      :data="clients"
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
      <!-- Expand Button -->
      <q-td slot="body-cell-expand" slot-scope="props" :props="props">
        <q-btn @click="rowExpand(props.row)" flat icon="aspect_ratio" />
      </q-td>
    </q-table>
    <!-- Copy Client Emails Button -->
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
import ClientPopup from "../components/ClientPopup.vue";

export default {
  name: "Clients",
  data() {
    return {
      showEmailPopup: false,
      allEmails: [],
      clients: [],
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
        {
          name: "notes",
          align: "left",
          label: "Notes",
          field: "notes"
        },
        {
          name: "expand",
          align: "right",
          label: "",
          field: "expand"
        }
      ]
    };
  },
  methods: {
    //Custom Dialog Box
    rowExpand(row) {
      this.$q
        .dialog({
          component: ClientPopup,
          name: row.name,
          email: row.email,
          notes: row.notes,
          attachments: row.attachments,
          parent: this,
          app: this.app
        })
        .onOk(() => {})
        .onCancel(() => {})
        .onDismiss(() => {});
    },
    //Get all clients from backend
    getClients() {
      this.$axios
        .get("/clients")
        .then(res => {
          this.clients = res.data;
          // Add all of clients' emails into allEmails list
          this.clients.forEach(element => {
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
    this.getClients();
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
