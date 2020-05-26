<template>
  <q-layout view="lHh Lpr lFf" id="container">
    <q-header>
      <q-toolbar class="bg-primary">
        <q-toolbar-title>
          <b>Move Up</b>
        </q-toolbar-title>
        <SignIn />
        <q-btn flat round color="background" icon="home" to="/home" class="q-mx-md" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import SignIn from "../pages/SignIn.vue";

export default {
  components: { SignIn }
};
</script>

<style lang="scss" scoped></style>
