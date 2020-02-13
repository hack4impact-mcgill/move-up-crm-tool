<template>
  <q-layout view="lHh Lpr lFf" id="container">
    <q-header>
      <q-toolbar class="bg-secondary">
        <q-toolbar-title>Move Up</q-toolbar-title>
        <div>
          <q-btn flat round color="background" label="LOG OUT" @click="logout" />
        </div>
        <div>
          <q-btn flat round color="background" icon="home" to="/home" />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
</script>

<style lang="scss" scoped>
</style>