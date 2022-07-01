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
      let other_user_uuid;
      let chat_token;
      if (token) {
        let myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);
        let requestOptions = {
          method: 'GET',
          mode: "cors",
          headers: myHeaders,
          redirect: 'follow'
        };
        await fetch(`${window.auth_hostname}/chat/token/${sender_id}`, requestOptions)
          .then(response => response.json())
          .then(async (data) => {
            other_user_uuid = data.other_user_uuid;
            chat_token = data.token;
            this.$cookies.set('chat_token', data.token, { maxAge: 60 * 60 * 24 * 7 });
            this.$cookies.set('own_uuid', data.own_uuid, { maxAge: 60 * 60 * 24 * 7 });
            this.$cookies.set('other_user_uuid', data.other_user_uuid, { maxAge: 60 * 60 * 24 * 7 });
            this.$cookies.set('username', data.username, { maxAge: 60 * 60 * 24 * 7 });
            this.$cookies.set('other_user_username', data.other_user_username, { maxAge: 60 * 60 * 24 * 7 });
            let myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", `Bearer ${chat_token}`);
            let requestOptions = {
              method: 'GET',
              mode: "cors",
              headers: myHeaders,
              redirect: 'follow'
            };
            await fetch(`${window.chat_hostname}/rooms/${other_user_uuid}`, requestOptions)
              .then(response => response.json())
              .then(async (data) => {
                await this.$cookies.set('room_id', data.content, { maxAge: 60 * 60 * 24 * 7 })
                  .then(this.$router.push('/chat')
                );
            });
        });
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
