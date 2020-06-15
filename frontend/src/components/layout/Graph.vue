<template>
  <div id="graph" class="page-summary-title">
    <br />
    <br />Sample : Chartjs graph
    <line-chart :chart-data="datacollection"></line-chart>
    <button @click="fillData()">Randomize</button>
  </div>
</template>

<script>
import LineChart from "./Graph.js";

export default {
  name: "Graph",
  components: {
    LineChart
  },
  data() {
    return {
      datacollection: null
    };
  },
  mounted() {
    this.fillData();
  },
  methods: {
    fillData() {
      this.datacollection = {
        labels: [this.getRandomInt(), this.getRandomInt()],
        datasets: [
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: [this.getRandomInt(), this.getRandomInt()]
          },
          {
            label: "Data Two",
            backgroundColor: "#ff55ff",
            data: [this.getRandomInt(), this.getRandomInt()]
          }
        ]
      };
    },
    getRandomInt() {
      //return Math.floor(Math.random() * (50 - 5 + 1)) + 5;
      return Math.floor(Math.random() * (5 - 5 + 1)) + 5;
    }
  }
};
</script>

<style scoped>
</style>