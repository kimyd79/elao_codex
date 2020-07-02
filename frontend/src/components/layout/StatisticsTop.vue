<template>
    <div id="statistics">
        <table class="page-summary-table">
          <thead>
            <tr>
              <th rowspan="2" style="width: 180px;" v-on:click="getStatistics">Request Top 1/5</th>
              <th rowspan="2" style="width: 460px;">Request URI</th>
              <th rowspan="2" style="width: 100px;">Count</th>            
            </tr>          
          </thead>
          <tbody>
            <tr v-for="(item, index) in items">
              <td>{{ index }}</td>
              <td>{{ item.content }}</td>
              <td>{{ item.result }}</td>            
            </tr>
            
            <!--
            <tr>
              <td>2</td>
              <td>/test2</td>
              <td>100</td>            
            </tr>
            <tr>
              <td>3</td>
              <td>/test3</td>
              <td>50</td>            
            </tr>
            <tr>
              <td>4</td>
              <td>/test4</td>
              <td>50</td>            
            </tr>
            <tr>
              <td>5</td>
              <td>/test5</td>
              <td>50</td>
            </tr>-->
            
          </tbody>
        </table>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'Statistics',
    props: ['statisticsRow', 'statisticsKind'],

    data: function() {
      return {
        items: [
          { content: 'Foo1', result: 'Foo1',},
          { content: 'Foo2', result: 'Foo2',},
          { content: 'Foo3', result: 'Foo3',},
          { content: 'Foo4', result: 'Foo4',},
        ]
      }
    },

    created() {
      console.log(this.statisticsRow, this.statisticsKind)
    },

    methods: {
      // TODO : 데이터 가져오기 (기본 조건값 필요 - 그래야 변경분 반영된다.)    
      setItems(results) {

        this.items = []

        for (let i = 0; i < results.length; i++) {
            this.items.push({
                content: results[i].fstatus,
                result: results[i].fstatus_count
            })
        }
      },

      getStatistics(){          
          
          // TODO
          var url = "http://172.16.1.110:8000/logdetail/statistics_top5/"

          let logfile_id = 'e005c4ee-2df8-4c53-9d35-ec7bd7629b76'
          let type = '1'

          let postData = {
                
                logfile_id: logfile_id,
                type: type
            };

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          axios.post(url, postData, axiosConfig)
          .then(res => {
              console.log(res)
              this.setItems(res.data.results);
          })
          .catch(err => {
              console.error(err); 
          })
      },
    }

}
</script>

<style scoped>

</style>