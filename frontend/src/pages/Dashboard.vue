<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md">
      <div class="row q-col-gutter-md justify-center">
        <div class="col">
          <q-btn
            icon="accessibility"
            label="Clients"
            class="dashboard-button"
            stack
            color="secondary"
            to="/clients"
          />
        </div>
        <div class="col">
          <q-btn
            icon="accessibility"
            label="Volunteers"
            class="dashboard-button"
            stack
            color="secondary"
            to="/volunteers"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script></script>

<style lang="scss" scoped>
.dashboard-button {
  width: 220px;
  height: 160px;
  margin: 45px;
  font-size: 17px;
}
</style>
