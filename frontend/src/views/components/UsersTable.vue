<script>
import VsudAvatar from "@/components/VsudAvatar.vue";
import VsudButton from "@/components/VsudButton.vue";
import img1 from "../../assets/img/team-2.jpg";
import img2 from "../../assets/img/team-3.jpg";
import img3 from "../../assets/img/team-4.jpg";
import img4 from "../../assets/img/team-3.jpg";
import img5 from "../../assets/img/team-2.jpg";
import img6 from "../../assets/img/team-4.jpg";

export default {
  name: "UsersTable",
  components: {
    VsudAvatar, VsudButton
  },
  data() {
    return {
      img1,
      img2,
      img3,
      img4,
      img5,
      img6,
      loaded: false,
      pages: 0,
      currentPage: 0,
      users_per_page: 5,
      users: [],
    };
  },
  mounted () {
    this.getPages()
    .then(() => {
      this.getUsers()
    });
  },
  methods: {
    async getPages() {
      await fetch( `${window.hostname}/count/users` )
      .then( response => response.json() )
      .then( data => {
        this.pages = Math.ceil( data.count / this.users_per_page );
      } )
      .catch( error => console.log( error ) );
    },
    async getUsers () {
      const skip = this.currentPage * this.users_per_page;
      const limit = this.users_per_page;

      var requestOptions = {
        method: 'GET',
        redirect: 'follow'  
      };

      // await fetch(`${window.hostname}/users?skip=${skip}&limit=${limit}/`, requestOptions)
      await fetch(`${window.hostname}/users/`, requestOptions)
        .then(response => response.json())
        .then(data => { this.users = data; console.log(this.users); })
        .then(() => { this.loaded = true; })
        .catch(error => console.log('error', error));
    },

    async nextPage() {
      if ( this.currentPage < this.pages - 1 ) {
        this.currentPage++;
        this.getUsers();
      }
    },

    async previousPage() {
      if ( this.currentPage > 0 ) {
        this.currentPage--;
        this.getUsers();
      }
    },

    async pingUser(receiver_id) {
      const token = this.$cookies.get("token");
      if (token) {
        const user_id = this.$cookies.get("user_id");
        //agregar start ticket indices

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        let raw = JSON.stringify({});
        let requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        };
        await fetch(`${window.hostname}/pings/${user_id}/${receiver_id}`, requestOptions)
        .then(response => response.json())
        .then(() => {
          alert('Ping enviado correctamente');
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
  <div class="card mb-4">
    <div class="card-header pb-0">
      <h6>Usuarios de GeoMeetr</h6>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div
        v-if="loaded"
        class="table-responsive p-0"
      >
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Nombre
              </th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Usuario
              </th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Teléfono
              </th>

              <th class="text-secondary opacity-7"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <vsud-avatar :img="img1" size="sm" border-radius="lg" class="me-3" alt="user1" />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">{{ user.name }}</h6>
                    <p class="text-xs text-secondary mb-0">{{ user.email }}</p>
                  </div>
                </div>
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold">{{ user.username }}</span>
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold">{{ user.phone }}</span>
              </td>
              <td class="align-middle text-center text-sm">
                <button type="button" class="btn btn-outline-success btn-sm" @click="pingUser(user.user_id)">Pinguear</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <Strong> Página {{ currentPage+1 }} de {{ pages }}</Strong>
      <vsud-button
        v-if="currentPage > 0"
        class="my-4 mb-2"
        variant="gradient"
        color="danger"
        full-width
        @click="previousPage"
      > Anterior
      </vsud-button>
      <vsud-button
        v-if="currentPage < pages - 1"
        class="my-4 mb-2"
        variant="gradient"
        color="info"
        full-width
        @click="nextPage"
      > Siguiente
      </vsud-button>
    </div>
  </div>
</template>
