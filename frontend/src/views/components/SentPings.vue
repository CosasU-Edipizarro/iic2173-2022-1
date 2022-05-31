<script>
import VsudAvatar from "@/components/VsudAvatar.vue";
import VsudBadge from "@/components/VsudBadge.vue";
import img1 from "../../assets/img/team-2.jpg";
import img2 from "../../assets/img/team-3.jpg";
import img3 from "../../assets/img/team-4.jpg";
import img4 from "../../assets/img/team-3.jpg";
import img5 from "../../assets/img/team-2.jpg";
import img6 from "../../assets/img/team-4.jpg";

export default {
  name: "SentPings",
  components: {
    VsudAvatar,
    VsudBadge,
  },
  data() {
    return {
      img1,
      img2,
      img3,
      img4,
      img5,
      img6,
      receivers: {},

      loaded: false
    };
  },
  beforeMount() {
    this.getUsers();
    this.getUserSents();
  },
  methods: {
    async getUsers() {
      await fetch( `${window.hostname}/users` )
        .then( response => response.json() )
        .then( data => { this.all_users = data } )
        .then( () => { this.loaded = true; } )
        .catch( error => console.log( error ) );
    },
    async getUserSents() {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id"); 
        await fetch( `${window.hostname}/pings/sent/${user_id}` )
          .then( response => response.json() )
          .then( data => { this.receivers = data; console.log("RECEIVERS"); console.log(this.receivers) } )
          .then( () => { this.loaded = true; } )
          .catch( error => console.log( error ) );
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
  },
};
</script>

<template>
  <table class="table align-items-center mb-0">
    <thead>
      <tr>
        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
          Nombre
        </th>
        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
          Índice DINDIN
        </th>
        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
          Estado
        </th>
      </tr>
    </thead>
    
    <tbody>
      <tr v-for="user in receivers" :key="user">
        <td>
          <div class="d-flex px-2 py-1">
            <div>
              <vsud-avatar :img="img1" size="sm" border-radius="lg" class="me-3" alt="user1" />
            </div>
            <div class="d-flex flex-column justify-content-center">
              <h6 class="mb-0 text-sm">{{user.name}}</h6>
              <p class="text-xs text-secondary mb-0">{{user.email}}</p>
            </div>
          </div>
        </td>
        <td class="align-middle text-center">
          <span class="text-secondary text-xs font-weight-bold">{{user.dindin}}</span>
        </td>
        <td class="align-middle text-center">
          <span class="text-secondary text-xs font-weight-bold">Completado</span>

        </td>
      </tr>
    </tbody>
  </table>
</template>
