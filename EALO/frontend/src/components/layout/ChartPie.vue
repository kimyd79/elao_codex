<script>

import { Pie, Doughnut, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: 'ChartPie',
  
  extends: Doughnut , // Pie 가능
  mixins: [reactiveProp],
  props: ['chartData', 'options'],
  
  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>

<style>
</style>

