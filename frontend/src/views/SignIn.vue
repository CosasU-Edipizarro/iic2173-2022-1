<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import VsudInput from "@/components/VsudInput.vue";
import VsudButton from "@/components/VsudButton.vue";
import bgImg from "@/assets/img/curved-images/curved9.jpg"
const body = document.getElementsByTagName("body")[0];

export default {
  name: "SigninPage",
  components: {
    Navbar,
    VsudInput,
    VsudButton,
  },
  data() {
    return {
      bgImg: bgImg,
      hola: '', 
      user: {
        username: '',
        password: ''
      }
    }
  },
  created () {
    this.checkIfToken();
  },
  beforeMount() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
    body.classList.remove("bg-gray-100");
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
    this.$store.state.showFooter = true;
    body.classList.add("bg-gray-100");
  },
  methods: {
    async submitSignin () {
      const username = this.user.username;
      const password = this.user.password;
      await fetch(`${window.hostname}/auth/login`,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "username": username, "password": password })
      })
      .then(response => response.json())
      .then( (data) => {
        console.log(data);
        this.$cookies.set('token', data["access_token"], { maxAge: 60 * 60 * 24 * 7 });
        return fetch(`${window.hostname}/users/user` , {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            Authorization: `Bearer ${this.$cookies.get('token')}`,
            }
        })
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        this.$cookies.set('user_id', data["user_id"], { maxAge: 60 * 60 * 24 * 7 });
      }) 
      .then(() => { this.checkIfToken(); })
    },

    checkIfToken () {
      const token = this.$cookies.get('token');
      if (token) {
        this.$router.push('/');
      }
    }
  },
};
</script>


<template>
  <div>
    <div class="container top-0 position-sticky z-index-sticky">
      <div class="row">
        <div class="col-12">
          <navbar
            is-blur="blur blur-rounded my-3 py-2 start-0 end-0 mx-4 shadow"
            btn-background="bg-gradient-success"
            :dark-mode="true"
          />
        </div>
      </div>
    </div>
    <main class="mt-0 main-content main-content-bg">
      <section>
        <div class="page-header min-vh-75">
          <div class="container">
            <div class="row">
              <div class="mx-auto col-xl-4 col-lg-5 col-md-6 d-flex flex-column">
                <div class="mt-8 card card-plain">
                  <div class="pb-0 card-header text-start">
                    <h3 class="font-weight-bolder text-info text-gradient">Bienvenido</h3>
                    <p class="mb-0">Ingresa tu usuario y contraseña para iniciar sesion</p>
                  </div>
                  <div class="card-body">
                    <div class="text-start">
                      <label>Usuario</label>
                      <vsud-input v-model="user.username" type="username" placeholder="Usuario..." name="username"/>

                      <label>Contraseña</label>
                      <vsud-input v-model="user.password" type="password" placeholder="Contraseña..." name="password"/>
                      <div class="text-center">
                        <vsud-button
                          class="my-4 mb-2"
                          variant="gradient"
                          color="info"
                          full-width
                          @click="submitSignin"
                        >Iniciar sesion</vsud-button>
                      </div>
                    </div>
                  </div>
                  <div class="px-1 pt-0 text-center card-footer px-lg-2">
                    <p class="mx-auto mb-4 text-sm">
                      ¿No tienes una cuenta?
                      <a
                        class="text-info text-gradient font-weight-bold"
                        href="/#/sign-up"
                      >Registrarse</a>
                    </p>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="top-0 oblique position-absolute h-100 d-md-block d-none me-n8">
                  <div
                    class="bg-cover oblique-image position-absolute fixed-top ms-auto h-100 z-index-0 ms-n6"
                    :style="{
                      backgroundImage:
                        `url(${bgImg})`,
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>