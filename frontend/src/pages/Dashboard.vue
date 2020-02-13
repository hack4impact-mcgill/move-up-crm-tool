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
            color="primary"
            to="/clients"
          />
        </div>
        <div class="col">
          <q-btn
            icon="accessibility"
            label="Volunteers"
            class="dashboard-button"
            stack
            color="primary"
            to="/volunteers"
          />
        </div>
        <div class="col">
          <q-btn
            icon="accessibility"
            label="Donors"
            stack
            class="dashboard-button"
            color="primary"
            to="/donors"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
</script>

<style lang="scss" scoped>
.dashboard-button {
  width: 180px;
  height: 120px;
}
</style>