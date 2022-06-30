<script>
import VsudAvatar from "@/components/VsudAvatar.vue";
import img1 from "../../assets/img/team-2.jpg";

export default {
  name: "AuthorsTable",
  components: {
    VsudAvatar,
  },
  data() {
    return {
      img1,
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
        mode: "cors",
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
    async acceptPing(sender_id) {
      const token = this.$cookies.get("token");
      let user_id;
      let other_user_uuid;
      let chat_token;
      let room_id;

      if (token) {
        user_id = this.$cookies.get("user_id");
        let myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", token);
        let raw = JSON.stringify({"sender_id": sender_id, "receiver_id": user_id});
        let requestOptions = {
          method: 'PATCH',
          mode: "cors",
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        };
        await fetch(`${window.hostname}/pings/`, requestOptions)
          .then(response => response.json())
          .then(() => {
            alert('Ping aceptado correctamente');
          })
          .then(async () => {
            let myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);
            requestOptions = {
              method: 'GET',
              mode: "cors",
              headers: myHeaders,
              redirect: 'follow'
            };
            console.log("PRE-get chat token");
            await fetch(`${window.auth_hostname}/chat/token/${sender_id}`, requestOptions)
              .then(response => response.json())
              .then(async (data) => {
                other_user_uuid = data.other_user_uuid;
                chat_token = data.token;

                console.log("CHAT TOKEN");
                console.log(chat_token);

                let myHeaders2 = new Headers();
                myHeaders2.append("Content-Type", "application/json");
                myHeaders2.append("Authorization", `Bearer ${chat_token}`);
                let raw = JSON.stringify({
                  "name": `Chat ${user_id} - ${sender_id}`,
                  "level_admin": 100,
                  "type": "user2user"
                });
                let requestOptions = {
                  method: 'POST',
                  mode: "cors",
                  headers: myHeaders2,
                  body: raw,
                  redirect: 'follow'
                };
                await fetch(`${window.chat_hostname}/rooms`, requestOptions)
                  .then(response => response.json())
                  .then(data => {
                    console.log("inside rooms");
                    console.log(data);
                    room_id = data.content.room.id;
                  })
                  .then(async () => {
                    console.log("inside async 2");
                    let myHeaders3 = new Headers();
                    myHeaders3.append("Content-Type", "application/json");
                    myHeaders3.append("Authorization", `Bearer ${chat_token}`);
                    let raw = JSON.stringify({"entity_UUID": other_user_uuid, "permissions": "rwa", "level": 100});
                    let requestOptions = {
                      method: 'PUT',
                      mode: "cors",
                      headers: myHeaders3,
                      body: raw,
                      redirect: 'follow'
                    };
                    console.log("PRE-put room");
                    await fetch(`${window.chat_hostname}/rooms/${room_id}/members`, requestOptions)
                      .then(response => {
                        console.log(response.json());
                        console.log("agregado");
                      })
                  })
              })
          })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    },
    async denyPing(sender_id) {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", token);
        let raw = JSON.stringify({"sender_id": sender_id, "receiver_id": user_id});
        let requestOptions = {
          method: 'DELETE',
          mode: "cors",
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        };
        await fetch(`${window.hostname}/pings/`, requestOptions)
        .then(response => response.json())
        .then(() => {
          alert('Ping rechazado correctamente');
        })
        .catch(error => { console.log(error); alert(error) });
      } else {
        alert("Debes iniciar sesión para acceder a esta página");
      }
    }
  }
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
          <button type="button" class="btn btn-outline-success btn-sm" @click="acceptPing(user.user_id)">Aceptar</button>
        </td>
        
        <td class="align-middle text-center text-sm">
          <button type="button" class="btn btn-outline-danger btn-sm" @click="denyPing(user.user_id)">Rechazar</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
