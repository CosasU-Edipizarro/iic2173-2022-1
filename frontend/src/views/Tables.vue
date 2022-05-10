<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Pings pendientes</h6>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
              <authors-table />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthorsTable from "./components/AuthorsTable.vue";

export default {
  name: "TablesPage",
  components: {
    AuthorsTable,
  },
};
</script>
