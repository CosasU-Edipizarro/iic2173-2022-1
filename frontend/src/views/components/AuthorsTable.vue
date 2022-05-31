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
  name: "AuthorsTable",
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
      senders: {},
      loaded: false
    };
  },
  beforeMount() {
    this.getUsers();
    this.getUserPings();
  },
  methods: {
    async getUsers () {
      var requestOptions = {
        method: 'GET',
        redirect: 'follow'  
      };
      await fetch(`${window.hostname}/users/`, requestOptions)
        .then(response => {
          let data = response.json()
          console.log(data)
          response.json()
          return data
        })
        .then(data => { this.all_users = data; console.log(this.users); })
        .then(() => { this.loaded = true; })
        .catch(error => console.log('error', error));
    },
    async getUserPings() {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        await fetch( `${window.hostname}/pings/received/${user_id}` )
          .then( response => response.json() )
          .then( data => { this.senders = data; console.log("SENDERS"); console.log(this.senders) } )
          .then( () => { this.loaded = true; } )
          .catch( error => console.log( error ) );
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
    //
    /*
    async acceptPing(_id) {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        await fetch(`${window.hostname}/pings/${user_id}/${receiver_id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: token
          },
        })
        .then(response => response.json())
        .then(() => {
          alert('Ping enviado correctamente');
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    }
    async denyPing(_id) {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        await fetch(`${window.hostname}/pings/${user_id}/${receiver_id}`, {
          method: "POST",//su DELETE
          headers: {
            "Content-Type": "application/json",
            Authorization: token
          },
        })
        .then(response => response.json())
        .then(() => {
          alert('Ping enviado correctamente');
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    }*/
  },
};
</script>

<template>
  <table class="table align-items-center mb-0">
    <thead>
      <tr>
        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Nombre</th>
        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
          Índice SIDI
        </th>
        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
          Índice SIIN
        </th>
        <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
          Índice DINDIN
        </th>
      </tr>
      
    </thead>
    <tbody>
      <tr v-for="user in senders" :key="user">
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
          <span class="text-secondary text-xs font-weight-bold">{{user.sidi}}</span>
        </td>
        <td class="align-middle text-center">
          <span class="text-secondary text-xs font-weight-bold">{{user.siin}}</span>
        </td>
        <td class="align-middle text-center">
          <span class="text-secondary text-xs font-weight-bold">{{user.dindin}}</span>

        </td>

        <td class="align-middle text-center text-sm">
          <button type="button" class="btn btn-outline-success btn-sm">Aceptar</button>
        </td>
        
        <td class="align-middle">
          <button type="button" class="mb-0 btn btn-link pe-3 ps-0 ms-auto" href="javascript:;">Rechazar</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
