<script>
export default {
  name: "BillingCard",
  data() {
    return {
      locations: [],
      loadedAddress: false,
    };
  },
  async beforeMount() {
    this.getLocations().
    then(() => {
      this.getAddress();
    });
  },
  methods: {
    async getLocations() {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        await fetch(`${window.hostname}/users/${user_id}/locations`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: token
          }
        })
        .then(response => response.json())
        .then(data => {
          console.log('Tus lugares:');
          console.log(data);
          this.locations = data;
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
    async getAddress(location, index) {
      let coords = location.coords
      coords = coords.replace(/\s/g, '')
      console.log('COORDS:');
      console.log(coords);
      const URL = `${window.hostname}/externalapi/getstreet/${coords}`
      console.log(URL);
      await fetch(URL)
        .then(response => response.json())
        .then(data => {
          console.log("RESPIESTA:");
          console.log(data);
          this.locations[index].address = data.data.address;
          })
        .then(() => { this.loadedAddress = true; });
    }
  }
};
</script>

<template>
  <div class="card">
    <div class="card-header pb-0 px-3">
      <h6 class="mb-0">Tus lugares</h6>
    </div>
    <div 
      v-if="locations.length > 0"
      class="card-body pt-4 p-3"
    >
      <ul 
        v-for="(location, index) in locations"
        :key="index"
        class="list-group"
      >
        <li class="list-group-item border-0 d-flex p-4 mb-2 bg-gray-100 border-radius-lg">
          <div class="d-flex flex-column">
            <span class="mb-2 text-xs">
              Nombre:
              <span class="text-dark font-weight-bold ms-sm-2"> {{ location.name }}</span>
            </span>
            <span class="mb-2 text-xs">
              Coordenadas:
              <span class="text-dark ms-sm-2 font-weight-bold"> {{ location.coords }}</span>
            </span>
            <span v-if="loadedAddress" class="mb-2 text-xs">
              Dirección:
              <span class="text-dark ms-sm-2 font-weight-bold"> {{ location.address }}</span>
            </span>
            <button @click="getAddress(location, index)"> Actualizar dirección </button>

          </div>
          <!-- <div class="ms-auto text-end">
            <a class="btn btn-link text-danger text-gradient px-3 mb-0" href="javascript:;">
              <i class="far fa-trash-alt me-2" aria-hidden="true"></i>Borrar
            </a>
            <a class="btn btn-link text-dark px-3 mb-0" href="javascript:;">
              <i class="fas fa-pencil-alt text-dark me-2" aria-hidden="true"></i>Editar
            </a>
          </div> -->
        </li>
      </ul>
    </div>
  </div>
</template>
