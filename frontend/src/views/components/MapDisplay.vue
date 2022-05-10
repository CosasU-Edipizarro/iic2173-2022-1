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
      marker: [-33.498769, -70.610787],
      markers: []
    };
  },
  mounted() {
    this.receiveCoords();
    this.receiveLocations();
  },
  methods: {
    changeLocation(event) {
      this.marker = event.target._latlng;
    },
    receiveCoords() {
      if (this.coords) {
        this.marker = this.coords[0];
        this.markers = this.coords;
      }
    },
    receiveLocations() {
      if (this.locations) {
        const markers = [];
        this.locations.forEach(location => {
          markers.push(location.coords);
        });
        this.markers = markers;
        this.marker = markers[0];
      }
    },
  },
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

      <l-marker :lat-lng="marker" draggable @moveend=changeLocation>
        <l-icon :icon-url="iconUrl" :icon-size="iconSize" />
        <l-popup>
          Coordenadas (Latitud-Longitud):
          <br>
          {{ marker }}
        </l-popup>
      </l-marker>

    </l-map>
  </div>
</template>