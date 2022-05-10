<script>
import setTooltip from "@/assets/js/tooltip.js";
import MapLocations from "./components/MapLocations.vue";
export default {
  name: "MapsPage",
  components: {
    MapLocations
  },
  data() {
    return {
      n_maps: [],
      all_users: {},
      selected_users: [],
      selected_users_locations: {},
      personal_locations: [],
      loaded: false
    };
  },
  beforeMount() {
    this.getUsers();
    this.getPersonalLocations();
  },
  methods: {
    async getUsers() {
      await fetch( `${window.hostname}/users` )
        .then( response => response.json() )
        .then( data => { this.all_users = data } )
        .then( () => { this.loaded = true; } )
        .catch( error => console.log( error ) );
    },
    async getLocations(user_id) {
      await fetch( `${window.hostname}/users/${user_id}/locations` )
        .then( response => response.json() )
        .then( data => { this.selected_users_locations[user_id] = data } )
        .then( () => { this.loaded = true; } )
        .catch( error => console.log( error ) );
    },
    async getPersonalLocations() {
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
          this.personal_locations = data;
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
    onClick() {
      var values = [document.getElementById("user1").value,
                    document.getElementById("user2").value,
                    document.getElementById("user3").value,
                    document.getElementById("user4").value,
                    document.getElementById("user5").value]
      for (var i = 0; i < 5; i++) {
        if (values[i] != "---"){
          this.n_maps.push(MapLocations)
          this.selected_users.push(values[i])
        }
      }
      this.selected_users.forEach(element => {
        this.getLocations(element);
      });
      console.log(this.all_users);
      console.log(this.selected_users);
      console.log(this.selected_users_locations);
    },
  },
};
</script>

<template>
  <div>
    <div class="card-header pb-0 px-3">
      <h6 class="mb-0">Escoge usuarios a buscar</h6>
      <div class="row">
        <div class="col pb-3">
          <label>Usuario 1:</label>
          <select id="user1" class="form-select" placeholder="Usuario 1">
            <option value="---" selected>---</option>
            <option v-for="user in all_users" :key="user" :value="user.id" class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
              {{ user.name }}
            </option>
          </select>
        </div>
        <div class="col pb-3">
          <label>Usuario 2:</label>
          <select id="user2" class="form-select" placeholder="Usuario 2">
            <option value="---" selected>---</option>
            <option v-for="user in all_users" :key="user" :value="user.id" class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
              {{ user.name }}
            </option>
          </select>
        </div>
        <div class="col pb-3">
          <label>Usuario 3:</label>
          <select id="user3" class="form-select" placeholder="Usuario 3">
            <option value="---" selected>---</option>
            <option v-for="user in all_users" :key="user" :value="user.id" class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
              {{ user.name }}
            </option>
          </select>
        </div>
        <div class="col pb-3">
          <label>Usuario 4:</label>
          <select id="user4" class="form-select" placeholder="Usuario 4">
            <option value="---" selected>---</option>
            <option v-for="user in all_users" :key="user" :value="user.id" class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
              {{ user.name }}
            </option>
          </select>
        </div>
        <div class="col pb-3">
          <label>Usuario 5:</label>
          <select id="user5" class="form-select" placeholder="Usuario 5">
            <option value="---" selected>---</option>
            <option v-for="user in all_users" :key="user" :value="user.id" class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
              {{ user.name }}
            </option>
          </select>
        </div>
        <button type="button" class="btn btn-outline-success btn-sm" @click="onClick">Buscar</button>
      </div>
    </div>
    <div class="container-fluid mt-4">
      <div class="card-header pb-0">
        <div class="row">
          <!-- <div class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
            <h6 class="mb-0"> Tus ubicaciones </h6>
            <map-locations :locations="personal_locations"/>
          </div> -->
          <div v-for="(user_locations, user_id) in selected_users_locations" :key="user_id" class="col-12 col-md-3 col-xl-4 pb-6 min-height-300">
            <h6 class="mb-0">Usuario {{ all_users[user_id - 1].name}}</h6>
            <map-locations :locations="user_locations"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>