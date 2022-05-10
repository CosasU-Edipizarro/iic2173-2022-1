<script>
import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LControlLayers,
  LTooltip,
  LPopup,
} from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
export default {
  name: "MapDisplay",
  components: {
    LMap,
    LIcon,
    LTileLayer,
    LMarker,
    LControlLayers,
    LTooltip,
    LPopup,
  },
  props: {
    coords: {
      type: Object,
      default: null,
    },
    locations: {
      type: Object,
      default: null,
    }
  },
  data() {
    return {
      zoom: 13,
      iconWidth: 25,
      iconHeight: 40,
      marker: [],
      markers: []
    };
  },
  beforeMount() {
    this.receiveLocations();
    this.receiveCoords();
  },
  methods: {
    receiveCoords() {
      if (this.coords) {
        this.marker = this.coords[0];
        this.markers = this.coords;
      }
    },
    receiveLocations() {
      if (this.locations.length == 0) {
        console.log("AIUDA")
        this.markers = [[-33.498769, -70.610787]];
        this.marker = [-33.498769, -70.610787];
      } else if (this.locations) {
        const temp_markers = [];
        this.locations.forEach(location => {
          temp_markers.push(location.coords.split(","));
        });
        this.markers = temp_markers;
        this.marker = temp_markers[0];
      }
    },
  }
};
</script>

<template>
  <div style="height: 100%; width: 100%;">
    <l-map
      v-model="zoom"
      v-model:zoom="zoom"
      :center="marker"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></l-tile-layer>
      <l-control-layers />

      <l-marker v-for="(mark) in markers" :lat-lng="mark" :key="mark">
        <p> {{ mark }} </p>
        <l-icon :icon-url="iconUrl" :icon-size="iconSize" />
        <l-popup>
          Coordenadas (Latitud-Longitud):
          <br>
          {{ mark }}
        </l-popup>
      </l-marker>

    </l-map>
  </div>
</template>