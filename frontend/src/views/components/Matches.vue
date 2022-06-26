<script>
import VsudAvatar from "@/components/VsudAvatar.vue";
import img1 from "../../assets/img/team-2.jpg";

export default {
  name: "Matches",
  components: {
    VsudAvatar,
  },
  data() {
    return {
      img1,
      friends: {},
      loaded: false
    };
  },
  beforeMount() {
    this.getUserMatches();
  },
  methods: {
    async getUserMatches() {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        await fetch( `${window.hostname}/pings/accepted/${user_id}` )
          .then( response => response.json() )
          .then( data => { this.friends = data; console.log("FRIENDS"); console.log(this.friends) } )
          .then( () => { this.loaded = true; } )
          .catch( error => console.log( error ) );
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
    async goToChat(sender_id) {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        //ir a la sala ¿?¿?¿'¡?¡?¿?¿
      }
    },
  }
};
</script>

<template>
  <table class="table align-items-center mb-0">
    <thead>
      <tr>
        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Nombre</th>
      </tr>
      
    </thead>
    <tbody>
      <tr v-for="user in friends" :key="user">
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

        <td class="align-middle text-center text-sm">
          <button type="button" class="btn btn-outline-success btn-sm" @click="goToChat(user.user_id)">Chatear</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
