<template>
  <div class="vld-parent">
    <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>  
    <div id="statistics">
        <table class="page-summary-table">
          <thead>
            <tr>
              <th rowspan="2" style="width: 180px;">{{ this.title }}</th>
              <th rowspan="2" style="width: 460px;">{{ this.content }}</th>
              <th rowspan="2" style="width: 100px;">Result</th>            
            </tr>          
          </thead>
          <tbody>
            
            <tr v-for="(item, index) in items" >
              <td >{{ index+1 }}</td>    

              <!-- TODO: content 종류에 따라 style= "text-align:left;" 적용할 것 -->          
              <td v-on:click="getDetail(item)">{{ item.result }}</td>
              <td>{{ item.result_count }}</td>            
            </tr>
            
          </tbody>
        </table>
    </div>    
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import VueElementLoading from 'vue-element-loading'

export default {
    name: 'Statistics',
    props: ['statisticsRow', 'statisticsKind'],

    components: { 

      VueElementLoading,
    },
    
    data: function() {
      return {
        title: "",
        content: "",
        items: [
          { result: '...', result_count: '....',},          
        ],
        // Loading Spinner data
        isActive: false,

      }
    },

    created() {
      console.log(this.statisticsRow, this.statisticsKind)
    },

    computed: mapGetters({
      isSearch: "getToggleSearch",
      
      dateFromValue: "getFromDate",
      dateToValue: "getToDate",
      timeFromValue: "getFromTime",
      timeToValue: "getToTime",

      conditionValue: "getCondition",
      searchValue: "getSearchKeyword",

      ttFromValue: "getFromTimeTaken",
      ttToValue: "getToTimeTaken",

    }),

    methods: {

      getDetail(item){
        alert('getDetail : '+item)
        console.log(item)
      },
      // TODO : 데이터 가져오기 (기본 조건값 필요 - 그래야 변경분 반영된다.)    
      setItems(results) {

        this.items = []

        for (let i = 0; i < results.length; i++) {
            this.items.push({
                result: results[i].result,
                result_count: results[i].result_count
            })
        }
      },

      getFilter() {
      
        let filter = {
          dateFromValue: this.dateFromValue,
          dateToValue: this.dateToValue,
          timeFromValue: this.timeFromValue,
          timeToValue: this.timeToValue,

          conditionValue: this.conditionValue,
          searchValue: this.searchValue,

          ttFromValue: this.ttFromValue,
          ttToValue: this.ttToValue,
        }
        
        return filter
    },

      getStatistics(){          
          
          var url = "http://127.0.0.1:8000/logdetail/statistics_top"

          // CASE#1 - Top 5 일때
          // type=1. Status Codes Top5
          // type=2. Requests Top5
          // type=3. 최다 404 발생 URL Top5
          // type=4. Time Taken Top5
          // type=5. Visitors Top5
        
          // CASE#2 - Top 1 일때
          // type=1. 전체 처리량(건수)
          // type=2. 최다접속 IP주소
          // type=3. 최다접속 사용자 요청(request)
          // type=4. 최다 404 발생 URL          

          // TODO : title, content
          if ( this.statisticsRow == 5){
            
            this.title = "Top 5"

            switch(this.statisticsKind){
              case 1:
                this.content = "HTTP Status Codes(count)"
                break;
              case 2:
                this.content = "Requests URI(count)"
                break;
              case 3:
                this.content = "404 Requests URI(count)"
                break;
              case 4:
                this.content = "Requests Time-taken(ms/㎲)"
                break;
              case 5:
                this.content = "Visitors(count)"
                break;
              default:
            }

          }else if ( this.statisticsRow == 1){

            this.title = "Top"
            switch(this.statisticsKind){
              case 1:
                this.content = "Total Request(count)"
                break;
              case 2:
                this.content = "Top Visitor(count)"
                break;
              case 3:
                this.content = "Top Requests URI(count)"
                break;
              case 4:
                this.content = "Top 404 Requests URI(count)"
                break;
              default:
            }
          }
              
          let logfile_id = this.$store.state.logFileID
          console.log(logfile_id)

          var url = "http://127.0.0.1:8000/logdetail/statistics_top"+this.statisticsRow+"/"  // 1 or 5

          let postData = {
                
                logfile_id: logfile_id,
                type: this.statisticsKind,
                
                filter: this.getFilter()
            };

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          // Start Loading Spinner
          this.isActive = true 
          
          axios.post(url, postData, axiosConfig)
          .then(res => {
              console.log(res)
              this.setItems(res.data.results);
              //Stop Loading Spinner
              this.isActive = false 
          })
          .catch(err => {
              console.error(err); 
              //Stop Loading Spinner
              this.isActive = false 
          })
      },
    },

    
  watch: {
    isSearch() {

      this.getStatistics();
    }
  }

}
</script>

<style scoped>

</style>
