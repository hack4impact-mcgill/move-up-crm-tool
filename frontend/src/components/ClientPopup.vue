<!--Component for Client Popup-->
<template>
  <q-dialog ref="dialog" full-width @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <!--contents of dialog box-->
      <!--Header: Name and Close Icon-->
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ name }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <!--Body: Email, notes and Attachments-->
      <q-card-section>
        <p>Email: {{ email }}</p>
        <p>Notes: {{ notes }}</p>
        <p>Attachments:</p>
        <!-- Check for files in attachments -->
        <div v-if="url(attachments)">
          <!--Create hyperlinks for each file-->
          <li v-for="file in attachments" :key="file.url">
            <a v-bind:href="file.url" target="_blank">{{
              getName(file.url)
            }}</a>
          </li>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  props: {
    name: String,
    email: String,
    notes: String,
    attachments: Array
  },
  methods: {
    //Check for files, display nothing if null
    url: function(attachments) {
      if (attachments === null) {
        return false;
      } else {
        return true;
      }
    },
    //Get name of file from url in airtable
    getName: function(url) {
      return url.split("/")[6];
    },
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    },
    onDialogHide() {
      this.$emit("hide");
    },
    onOKClick() {
      this.$emit("hide");
    },
    onCancelClick() {
      this.hide();
    }
  }
};
</script>
