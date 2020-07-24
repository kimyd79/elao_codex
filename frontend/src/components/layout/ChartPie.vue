<script>

import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: 'ChartPie',
  
  extends: Pie,
  mixins: [reactiveProp],
  props: ['options'],
  
  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

// import { Pie } from 'vue-chartjs'

// export default {
//   name: 'ChartPie',
  
//   extends: Pie,
//   data: () => ({
//     chartdata: {
//       labels: ['Red', 'Yellow', 'Blue'],
//       datasets: [{
//         data: [10, 20, 30],
//             backgroundColor: [
//               'rgba(255, 99, 132, 1)',
//               'rgba(54, 162, 235, 1)',
//               'rgba(255, 206, 86, 1)',                   
//             ],                
//       }]
//     },
//     options: {
//       responsive: true,
//       maintainAspectRatio: false
//     }
//   }),

//   mounted () {
//     this.renderChart(this.chartdata, this.options)
//   }
// }

</script>

<style>
</style>

