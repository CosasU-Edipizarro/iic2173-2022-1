<template>
  <div>
    <div
      id="sidenav-collapse-main"
      class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
    >
      <ul class="navbar-nav">
        <li class="nav-item">
          <sidenav-collapse nav-text="Inicio" :to="{ name: 'Dashboard' }">
            <template #icon>
              <icon name="dashboard" />
            </template>
          </sidenav-collapse>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Ubicaciones" :to="{ name: 'Billing' }">
            <template #icon>
              <icon name="billing" />
            </template>
          </sidenav-collapse>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Mapa" :to="{ name: 'Maps' }">
            <template #icon>
              <icon name="virtual-reality" />
            </template>
          </sidenav-collapse>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Pings" :to="{ name: 'Tables' }">
            <template #icon>
              <icon name="tables" />
            </template>
          </sidenav-collapse>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Usuarios" :to="{ name: 'Userlist' }">
            <template #icon>
              <icon name="rtl-page" />
            </template>
          </sidenav-collapse>
        </li>

        <li class="mt-3 nav-item">
          <h6
            class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
            :class="$store.state.isRTL ? 'me-4' : 'ms-2'"
          >Sesión</h6>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Perfil" :to="{ name: 'Profile' }">
            <template #icon>
              <icon name="customer-support" />
            </template>
          </sidenav-collapse>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Ingresar" :to="{ name: 'Sign In' }">
            <template #icon>
              <icon name="sign-in" />
            </template>
          </sidenav-collapse>
        </li>
        <li class="nav-item">
          <sidenav-collapse nav-text="Registrarse" :to="{ name: 'Sign Up' }">
            <template #icon>
              <icon name="sign-up" />
            </template>
          </sidenav-collapse>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import Icon from "@/components/Icon.vue";
import SidenavCollapse from "./SidenavCollapse.vue";
import SidenavCard from "./SidenavCard.vue";

export default {
  name: "SidenavList",
  components: {
    Icon,
    SidenavCollapse,
    SidenavCard,
  },
  props: {
    cardBg: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      title: "GeoMeetr",
      controls: "dashboardsExamples",
      isActive: "active",
    };
  },
  methods: {
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return routeArr[1];
    },
  },
};
</script>
