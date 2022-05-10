<script>
import setTooltip from "@/assets/js/tooltip.js";
import BillingCard from "./components/BillingCard.vue";
import MapDisplay from "./components/MapDisplay.vue";
import VsudInput from "@/components/VsudInput.vue";

export default {
  name: "BillingPage",
  components: {
    BillingCard,
    VsudInput,
    MapDisplay,
  },
  data() {
    return {
      location: {
        name: "",
        coords: "",
      },
      locations: [],
      locationsUpdater: 0,
      loaded: false,
    };
  },
  beforeMount() {
    this.getLocations()
    .then( () => { this.fixLocationsCoords(); })
    .then( () => { this.loaded = true; });
    setTooltip();
  },
  methods: {
    async createLocation() {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        const data = this.location;
        console.log("Data createLocation");
        console.log(data);
        console.log(data);
        await fetch(`${window.hostname}/users/${user_id}/locations`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: token
          },
          body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .then(() => {
          this.locationsUpdater++;
          alert('Ubicación agregada correctamente');
          this.$forceUpdate();
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
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
          // this.locations.push(data);
          this.locations = data;
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
    fixLocationsCoords() {
      this.locations.forEach(location => {
        location.coords = location.coords.split(",");
      });
    }
  }
};
</script>

<template>
  <div class="container-fluid mt-4">
    <div class="card-header pb-0 px-3">
      <h6 class="mb-0">Añade un nuevo lugar</h6>
    </div>
    <div class="row mt-4">
      <div class="col-md-7">
        <map-display />
      </div>
      <div class="col-md-5 mt-4">
        <label>Nombre del lugar</label>
        <vsud-input v-model="location.name" type="text" placeholder="Avenida..." name="name" />
        <label>Coordenadas</label>
        <vsud-input v-model="location.coords" type="text" placeholder="Latitud, Longitud" name="coords" />
        <button type="button" class="mb-0 btn btn-outline-success btn-sm" @click="createLocation">Añadir lugar</button>
      </div>
    </div>

    <div v-if="loaded" class="row mt-4">
      <billing-card :key="locationsUpdater"/>
    </div>
    <div v-if="loaded" class="col-md-7">
      <map-locations :locations="locations" />
    </div>
  </div>
</template>