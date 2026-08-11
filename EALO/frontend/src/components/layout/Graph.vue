<script>

import { Line } from 'vue-chartjs'

export default {
  name: 'Graph',
  
  extends: Line,
  data: () => ({
    chartdata: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      datasets: [{
          label: 'My First dataset',
          backgroundColor: 'rgb(255, 99, 132)',
          borderColor: 'rgb(255, 99, 132)',
          fill: false,
          data: [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],                
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),

  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>

<style>
</style>

