<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-lg-7 mb-lg-0 mb-4">
        <div class="card">
          <div class="card-body p-3">
            <div class="row">
              <div class="col-lg-6">
                <div class="d-flex flex-column h-100">
                  <p class="mb-1 pt-2 text-bold">Bienvenido a GeoMeetr</p>
                  <h5 class="font-weight-bolder">Un lugar para conocer gente nueva!</h5>
                  <p class="mb-5">
                    Registra los lugares que has visitado para mostrar a tus conocidos. Forma nuevas amistades con gente de tu alrededor. 
                  </p>
                  <a
                    class="text-body text-sm font-weight-bold mb-0 icon-move-right mt-auto"
                    href="/#/sign-up"
                  >
                    Únete a la comunidad
                    <i
                      class="fas fa-arrow-right text-sm ms-1"
                      aria-hidden="true"
                    ></i>
                  </a>
                </div>
              </div>
              <div class="col-lg-5 ms-auto text-center mt-5 mt-lg-0">
                <div class="bg-gradient-success border-radius-lg h-100">
                  <img
                    src="../assets/img/shapes/waves-white.svg"
                    class="position-absolute h-100 w-50 top-0 d-lg-block d-none"
                    alt="waves"
                  />
                  <div
                    class="position-relative d-flex align-items-center justify-content-center h-100"
                  >
                    <img
                      class="w-100 position-relative z-index-2 pt-4"
                      src="../assets/img/illustrations/rocket-white.png"
                      alt="rocket"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-5">
        <div class="card h-100 p-3">
          <div
            class="overflow-hidden position-relative border-radius-lg bg-cover h-100"
            style="
              background-image: url('https://demos.creative-tim.com/soft-ui-dashboard/assets/img/ivancik.jpg');
            "
          >
            <span class="mask bg-gradient-dark"></span>
            <div
              class="card-body position-relative z-index-1 d-flex flex-column h-100 p-3"
            >
              <h5 class="text-white font-weight-bolder mb-4 pt-2">
                Políticias de uso
              </h5>
              <p class="text-white">
                Infórmate acerca de nuestras políticas de uso y la utilización de los datos recopilados.
              </p>
              <a
                class="text-white text-sm font-weight-bold mb-0 icon-move-right mt-auto"
                href="javascript:;"
              >
                Leer más
                <i
                  class="fas fa-arrow-right text-sm ms-1"
                  aria-hidden="true"
                ></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- <div class="mt-4 row">
      <div class="mb-4 col-lg-5 mb-lg-0">
        <div class="card z-index-2">
          <div class="p-3 card-body">
            <active-users-chart />
          </div>
        </div>
      </div>
      <div class="col-lg-7">
        <div class="card z-index-2">
          <gradient-line-chart />
        </div>
      </div>
    </div>
    <div class="row my-4">
      <div class="col-lg-8 col-md-6 mb-md-0 mb-4">
        <projects-card />
      </div>
      <div class="col-lg-4 col-md-6">
        <Orders-card />
      </div>
    </div> -->
  </div>
</template>
<script>
import Card from "@/examples/Cards/Card.vue";
import ActiveUsersChart from "@/examples/Charts/ActiveUsersChart.vue";
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
import OrdersCard from "./components/OrdersCard.vue";
import ProjectsCard from "./components/ProjectsCard.vue";
import US from "../assets/img/icons/flags/US.png";
import DE from "../assets/img/icons/flags/DE.png";
import GB from "../assets/img/icons/flags/GB.png";
import BR from "../assets/img/icons/flags/BR.png";

export default {
  name: "DashboardDefault",
  components: {
    Card,
    ActiveUsersChart,
    GradientLineChart,
    ProjectsCard,
    OrdersCard,
  },
  data() {
    return {
      stats: {
        iconBackground: "bg-gradient-success",
        money: {
          title: "Today's Money",
          value: "$53,000",
          percentage: "+55%",
          iconClass: "ni ni-money-coins",
        },
        users: {
          title: "Today's Users",
          value: "2,300",
          percentage: "+3%",
          iconClass: "ni ni-world",
        },
        clients: {
          title: "New Clients",
          value: "+3,462",
          percentage: "-2%",
          iconClass: "ni ni-paper-diploma",
          percentageColor: "text-danger",
        },
        sales: {
          title: "Sales",
          value: "$103,430",
          percentage: "+5%",
          iconClass: "ni ni-cart",
        },
      },
      sales: {
        us: {
          country: "United States",
          sales: 2500,
          value: "$230,900",
          bounce: "29.9%",
          flag: US,
        },
        germany: {
          country: "Germany",
          sales: "3.900",
          value: "$440,000",
          bounce: "40.22%",
          flag: DE,
        },
        britain: {
          country: "Great Britain",
          sales: "1.400",
          value: "$190,700",
          bounce: "23.44%",
          flag: GB,
        },
        brasil: {
          country: "Brasil",
          sales: "562",
          value: "$143,960",
          bounce: "32.14%",
          flag: BR,
        },
      },
    };
  },
};
</script>
