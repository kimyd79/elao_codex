<script>

import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ['options'],
  mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, this.options)
  }
}

// import { Line } from 'vue-chartjs'

// export default {
//   name: 'ChartLine',
  
//   extends: Line,
//   data: () => ({
//     chartdata: {
//       labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
//       datasets: [{
//           label: 'My First dataset',
//           backgroundColor: 'rgb(255, 99, 132)',
//           borderColor: 'rgb(255, 99, 132)',
//           fill: false,
//           data: [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],                
//       }]
//     },
//     options: {
//       responsive: true,
//       maintainAspectRatio: false
//     }
//   }),

//   mounted () {
//     this.renderChart(this.chartdata, this.options)
//   },

//   watch: {
//     chartdata () {
//       this.$data._chart.update()
//     }
//   }
// }

</script>

<style>
</style>

