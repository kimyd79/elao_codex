<script>

import { Bar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: 'ChartBar',
  
  extends: Bar,
  mixins: [reactiveProp],
  props: ['chartData', 'options'],
  
  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>

<style>
</style>

