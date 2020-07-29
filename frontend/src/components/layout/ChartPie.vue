<script>

import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: 'ChartPie',
  
  extends: Pie,
  mixins: [reactiveProp],
  props: ['chartData', 'options'],
  
  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>

<style>
</style>

