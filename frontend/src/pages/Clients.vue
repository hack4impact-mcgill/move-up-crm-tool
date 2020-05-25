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
      <!--Expand Button-->
      <q-td slot="body-cell-expand" slot-scope="props" :props="props">
        <q-btn @click="row_expand(props.row)" flat icon="aspect_ratio" />
      </q-td>
    </q-table>
    <!-- Email Client Button -->
    <div class="q-pa-md email-btn">
      <q-btn
        icon="email"
        label="Email Selected Clients"
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
import ClientPopup from "../components/ClientPopup.vue";
import EmailPopup from "../components/EmailPopup.vue";

export default {
  components: { EmailPopup },
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
    row_expand(row) {
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
    getSelectedEmail: function() {
      this.showEmailPopup = true;
    }
  },
  created() {
    this.getClients();
  }
};
</script>

<style lang="sass">
.email-btn
  float: right
  margin: 30px

.table-width
  margin: 25px
</style>
