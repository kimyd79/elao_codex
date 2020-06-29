<script>

import { Bar } from 'vue-chartjs'

export default {
  name: 'ChartBar',
  
  extends: Bar,
  data: () => ({
    chartdata: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: 'DataSet1',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            },
            {
                label: 'DataSet2',
                data: [10, 5, 10, 2, 10, 20],
                backgroundColor: [
                    'rgba(155, 199, 132, 0.2)',
                    'rgba(154, 12, 235, 0.2)',
                    'rgba(155, 06, 86, 0.2)',
                    'rgba(175, 92, 192, 0.2)',
                    'rgba(53, 02, 255, 0.2)',
                    'rgba(155, 19, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
    }
  }),

  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>

<style>
</style>

