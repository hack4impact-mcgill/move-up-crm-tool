<!--Client Table-->
<template>
  <div class="q-pa-md q-gutter-sm">
    <q-table
      class="table-width"
      title="Clients"
      :data="clients"
      :columns="columns"
      row-key="email"
      wrap-cells
    >
      <!--Expand Button-->
      <q-td slot="body-cell-expand" slot-scope="props" :props="props">
        <q-btn @click="row_expand(props.row)" flat icon="aspect_ratio" />
      </q-td>
    </q-table>
  </div>
</template>

<script>
import axios from "axios";
import ClientPopup from "../components/ClientPopup.vue";
export default {
  data() {
    return {
      showEmailPopUp: false,
      clients: [],
      //Columns of Table
      columns: [
        {
          name: "name",
          required: true,
          label: "Name",
          style: "width: 150px",
          align: "left",
          field: row => row.name,
          //Name column color
          classes: "bg-dark ellipsis",
          headerClasses: "bg-accent text-white"
        },
        {
          name: "email",
          style: "width: 200px",
          align: "left",
          label: "Email",
          field: "email"
        },
        {
          name: "notes",
          style: "width: 400px",
          align: "left",
          label: "Notes",
          field: "notes"
        },
        {
          name: "expand",
          style: "width: 100px",
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
      const path = "http://localhost:5000/clients";
      axios.get(path).then(res => {
        this.clients = res.data;
      });
    }
  },
  created() {
    this.getClients();
  }
};
</script>

<!--max-width: 1300px
    margin-top: 100px-->

<style lang="sass">
.table-width
  margin: 25px
</style>