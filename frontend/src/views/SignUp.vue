<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import VsudInput from "@/components/VsudInput.vue";
import VsudButton from "@/components/VsudButton.vue";
import bgImg from "@/assets/img/curved-images/curved6.jpg"
export default {
  name: "SignUp",
  components: {
    Navbar,
    VsudInput,
    VsudButton,
  },
  data() {
    return {
      bgImg: bgImg,
      user: {
        name: '',
        username: '',
        email: '',
        phone: '',
        hashed_password: ''
      }
    }
  },
  created() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
    this.$store.state.showFooter = true;
  },
  methods: {
    async submitSignup() {
      var myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      let raw = JSON.stringify({
        "name": this.user.username,
        "username": this.user.username,
        "email": this.user.email,
        "phone": this.user.phone,
        "hashed_password": this.user.hashed_password
      });

      let requestOptions = {

        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
      };

      await fetch(`${window.hostname}/users/`, requestOptions)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        this.$cookies.set('token', data["access_token"], { maxAge: 60 * 60 * 24 * 7 });
        return fetch(`${window.hostname}/users/user_info` , {
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
      .then(() => {
        alert('Usuario creado correctamente');
        this.$router.push('/dashboard');
      })
      .catch(error => { console.log(error); alert(error) });
    }
  }
};
</script>

<template>
  <div>
    <navbar btn-background="bg-gradient-primary" />
    <div
      class="pt-5 m-3 page-header align-items-start min-vh-50 pb-11 border-radius-lg"
      :style="{
        backgroundImage:   `url(${bgImg})`,
      }"
    >
      <span class="mask bg-gradient-dark opacity-6"></span>
      <div class="container">
        <div class="row justify-content-center">
          <div class="mx-auto text-center col-lg-5">
            <h1 class="mt-5 mb-2 text-white">Bienvenido!</h1>
            <p class="text-white text-lead">
              Rellena este formulario para crear una nueva cuenta y unirte.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row mt-lg-n10 mt-md-n11 mt-n10 justify-content-center">
        <div class="mx-auto col-xl-4 col-lg-5 col-md-7">
          <div class="card z-index-0">
            <div class="pt-4 text-center card-header">
              <h5>Regístrate</h5>
            </div>
            
            <div class="card-body">
              <div>
                <div class="mb-3">
                  <vsud-input v-model="user.name" type="text" placeholder="Nombre" aria-label="Name" />
                </div>
                <div class="mb-3">
                  <vsud-input v-model="user.username" type="text" placeholder="Nombre de Usuario" aria-label="Username" />
                </div>
                <div class="mb-3">
                  <vsud-input v-model="user.email" type="email" placeholder="Correo" aria-label="Email" />
                </div>
                <div class="mb-3">
                  <vsud-input v-model="user.phone" type="text" placeholder="Teléfono" aria-label="Phone" />
                </div>
                <div class="mb-3">
                  <vsud-input v-model="user.hashed_password" type="password" placeholder="Contraseña" aria-label="Password" />
                </div>

                <div class="text-center">
                  <vsud-button
                    color="dark"
                    full-width
                    variant="gradient"
                    class="my-4 mb-2"
                    @click="submitSignup"
                  >
                    Registrarse
                  </vsud-button>
                </div>
                <p class="text-sm mt-3 mb-0">
                  ¿Ya tienes una cuenta?
                  <a
                    class="text-info text-gradient font-weight-bold"
                    href="/#/sign-in"
                  >Ingresar</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
