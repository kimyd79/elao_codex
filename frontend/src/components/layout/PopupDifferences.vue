<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">      
      <ui-container-box :columns=14 vertical class="modal-container">

        <div class="popup-header">
            <div class="popup-header__title"> 
                Differences               
            </div>
            <div class="popup-header__close">
                <lego-icon small v-on:click="clickClose">close</lego-icon>
            </div>
            <ui-form-item :columns=13 label="Select Defferences" required left-label :label-width=160 :label-padding=16>
                    <lego-dropdown :items="listDefferences" v-model="differenceKind" width="500px" />
            </ui-form-item>

            <ui-container-box :columns="13" horizontal align-center class="page-form-area">

                    <ui-form-item :columns="70" label="Select N" align-left>
                        <lego-dropdown :items="listN" v-model="statisticsRow" width="100px" />
                    </ui-form-item>
   
                    <ui-form-item :columns="70" align-left >
                        <span style="color:#553ca5"> <b>* Search-1</b><br>
                        <span style="color:gray"> {{ this.subTitle1 }}</span><br><br> 
                        <b>* Search-2</b><br>
                        <span style="color:gray">{{ this.subTitle2 }}</span></span>
                    </ui-form-item> 
                
            </ui-container-box>
        </div>
       
        <ui-container-box :columns="13" horizontal align-center class="page-form-area">
            <div class="vld-parent">
                <component :is="currentView" v-on:popupClose="currentView=null"></component>
                <vue-element-loading :active="isActiveStatistic" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                <div class="add_scroll">
                    <table class="page-summary-table">
                        <thead>
                            <tr>
                                <th rowspan="2" style="width: 60px; color: rgb(85,60,165)"><b>{{ this.TopN }}</b></th>
                                <th rowspan="2" style="width: 580px; color: rgb(85,60,165)"><b>{{ this.content }}</b></th>
                                <th rowspan="2" style="width: 100px; color: rgb(85,60,165)"><b>count_1 </b></th>
                                <th rowspan="2" style="width: 100px; color: rgb(85,60,165)"><b>percent_1</b></th>
                                <th rowspan="2" style="width: 100px; color: rgb(85,60,165)"><b>count_2 </b></th>
                                <th rowspan="2" style="width: 100px; color: rgb(85,60,165)"><b>percent_2 </b></th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="(item, index) in items">
                                <td>{{ item.index }}</td>
                                
                                <td><VueCustomTooltip :label="item.result">
                                    {{ item.result_count != 0 ? item.result.substr(0,70)+(item.result.length > 70 ? " ..." : "" ) : "-"}}
                                    </VueCustomTooltip>
                                </td>
                                <td v-on:click="getDetail(item.result, item.date, '1')"><u>{{ item.result_count }}</u></td>
                                <td v-on:click="getDetail(item.result, item.date, '1')"><u>{{ item.ratio }}</u></td>
                                <td v-on:click="getDetail(item.result, item.date2, '2')"><u>{{ item.result_count2 }}</u></td>
                                <td v-on:click="getDetail(item.result, item.date2, '2')"><u>{{ item.ratio2 }}</u></td>
                            </tr>

                        </tbody>
                    </table>
                </div>
            </div>
       </ui-container-box> 
        <!-- Chart Area-->
        
        <span class="page-title__2label">Charts</span>
        <div class="vld-parent">
            <vue-element-loading :active="isActiveMultiLine" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />

            <ui-form-row>
                <ui-form-item :columns="12" label="Timeline" align-left required-left>
                    <lego-radio v-model="timeCondition" value="1">HH</lego-radio>
                    <lego-radio v-model="timeCondition" value="2">HHMM</lego-radio>
                    <lego-radio v-model="timeCondition" value="3">HHMMSS</lego-radio>                
                </ui-form-item>            
            </ui-form-row>
            <ui-form-row>
            <lego-button @click="resetZoom()" small>resetZoom</lego-button>
            <!-- <lego-button @click="multilineChartData()" small>chart</lego-button>
            <lego-button @click="getStatistics()" small>statistic</lego-button> -->
            </ui-form-row>            
            
            <chart-line ref='mlChart' :chart-data="mlChartData" :options="mlOptions"></chart-line>

            <div class="popup-buttons">
                <lego-button main v-on:click="clickClose">Close</lego-button>            
            </div>
        </div>

      </ui-container-box>
    </div>
</div>
</template>

<script>
import axios from "axios";
import {
    // TODO: Remove Others
    setCommonStatisticInfo,
    getMultiLineChartTemplateDiff,
    getMultiLineChartOptionsDiff,
    getMultiLineChartTemplateStatusDiff,
    getLineChartDataDiff,
    //getSearchFilter
} from "@/common"

import {
    mapGetters
} from "vuex";
import VueElementLoading from 'vue-element-loading'
import UIFormRow from './form/UIFormRow.vue';
import ChartLine from "@/components/layout/ChartLine";
import DetailPopup from './DetailPopup';
import moment from 'moment'
export default {

    components: {
        VueElementLoading,
        UIFormRow,
        ChartLine,  
        DetailPopup,  
        moment       
    },
  
    data() {
        return {

            // For Statistics N
            statisticsRow: 5,

            // statisticsKind = 30. Defference : Total Number of Requests (count)
            // statisticsKind = 31. Defference : TPS / Top N URI at TPS highest point
            // statisticsKind = 32. Defference : TPS / Top N Visitors(IP) at TPS highest point
            // statisticsKind = 33. Defference : timeTaken /  Top N URI at TimeTaken highest point
            // statisticsKind = 34. Defference : timeTaken / Top N Visitors(IP) at TimeTaken highest point
            // statisticsKind = 35. Defference : status(4xx,5xx) / Top N URI at ErrorCode highest point
            // statisticsKind = 36. Defference : status(4xx,5xx) / Top N Visitors(IP) at ErrorCode highest point

            statisticsKind: 30,

            // kind = 0 : request  
            // kind = 1 : TPS  
            // kind = 2 : timeTaken  
            // kind = 3 : status
            multilineChartKind: 0,

            // differenceKind = 0 : 전체 request 건수 비교 > 30%
            // differenceKind = 1 : TPS 최고점 TOP N개 URI 비율 비교(1분 단위) Request URI Top N at TPS peak
            // differenceKind = 2 : TPS 최고점 TOP N개 IP 비율 비교(1분 단위)
            // differenceKind = 3 : 처리시간 최고점 TOP N개 URI 비율 비교(1분 단위)
            // differenceKind = 4 : 처리시간 최고점 TOP N개 IP 비율 비교(1분 단위)
            // differenceKind = 5 : 오류코드(4xx,5xx) 합계 > 10% 경우, 최고점 TOP N개 URI 비율 비교
            // differenceKind = 6 : 오류코드(4xx,5xx) 합계 > 10% 경우, 최고점 TOP N개 IP 비율 비교
            differenceKind: '',
            
            title: ' URI at TPS peak',
            subTitle1: '...',
            subTitle2: '...',
            TopN: '',
            content: '',
            tmp_res1: [],
            tmp_res2: [], 
            timetakenUnit: "",
            currentView: null,

            // For Chart
            resetZoomV: "1",
            timeCondition: "2", // "Minute(분) 기준"

            mlChartData: null,
            mlOptions: getMultiLineChartOptionsDiff('- No Data -'),

            // columns: [
            //     {label: 'No', key: "no", alignCenter: true, width: 10 },
            //     {label: 'Request URI', key: "uri", alignCenter: true, width: 80 },
            //     {label: 'Count_1', key: "count_1", alignCenter: true, width: 15 },
            //     {label: '%_1', key: "percent_1", alignCenter: true, width: 15 },
            //     {label: 'Count_2', key: "count_2", alignCenter: true, width: 15 },
            //     {label: '%_2', key: "percent_2", alignCenter: true, width: 15 },
            // ],
            // items: [
            //     {no:'1', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'10', count_2:'97', percent_2:'40',},
            //     {no:'2', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'20', count_2:'97', percent_2:'30',},
            //     {no:'3', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'30', count_2:'97', percent_2:'10',},
            //     {no:'4', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'97', percent_1:'40', count_2:'0', percent_2:'0',},
            //     {no:'New', uri:'GET /restservice/ci/company/CP0115/gbm/GB007922?extragbm=GB007928&virtualyn=YES HTTP/1.1', count_1:'0', percent_1:'0', count_2:'97', percent_2:'10',},                
            // ],

            items: [{
                index: '',
                result: '- No Data -',
                result_count: '...',
                ratio: '...',
                date: '',
                result_count2: '...',
                ratio2: '...',
                date2: ''
            }, ],

            mlChartData: null,

            logfile_id: '',
            project_id: '',

            // For Loading Spinner
            isActiveMultiLine: false,
            isActiveStatistic: false,

        }
    },

    created() {
        // TODO: Check! mapGetter로 가능?
        this.logfile_id = this.$store.state.logFileID
        this.project_id = this.$store.state.projectID
        this.differenceKind = "0"
        this.getStatistics();
        this.multilineChartData();
    },
    computed: {
        ...mapGetters({
            isSearch1: "getToggleSearch1",
            isSearch2: "getToggleSearch2",

            dateFromValue: "getFromDate",
            dateToValue: "getToDate",
            timeFromValue: "getFromTime",
            timeToValue: "getToTime",

            conditionValue: "getCondition",
            searchValue: "getSearchKeyword",
            excludeSearch: "getExcludeSearch",

            ttFromValue: "getFromTimeTaken",
            ttToValue: "getToTimeTaken",

            dateFromValue2: "getFromDate2",
            dateToValue2: "getToDate2",
            timeFromValue2: "getFromTime2",
            timeToValue2: "getToTime2",

            conditionValue2: "getCondition2",
            searchValue2: "getSearchKeyword2",
            excludeSearch2: "getExcludeSearch2",

            ttFromValue2: "getFromTimeTaken2",
            ttToValue2: "getToTimeTaken2",

            //logfile_id: "getLogFileID",
            //project_id: "getProjectID",
            logFormat: "getLogFormat",

        }),

        listN() {
            let rtn = [];
            rtn.push({
                value: "1",
                text: "1"
            });
            rtn.push({
                value: "5",
                text: "5"
            });
            rtn.push({
                value: "10",
                text: "10"
            });
            rtn.push({
                value: "20",
                text: "20"
            });
            return rtn;
        },

        listDefferences() {
            let rtn = [];
            rtn.push({
                value: "0",
                text: "Compare the total number of requests > 30%"
            });
            rtn.push({
                value: "1",
                text: "TOP "+this.statisticsRow+" URI at TPS highest point(every minute)"
            });
            rtn.push({
                value: "2",
                text: "TOP  "+this.statisticsRow+" Visitors(IP) at TimeTaken highest point(every minute)"
            });
            rtn.push({
                value: "3",
                text: "TOP "+this.statisticsRow+" URI at TimeTaken highest point(every minute)"
            });
            rtn.push({
                value: "4",
                text: "TOP  "+this.statisticsRow+" Visitors(IP) at ErrorStatus highest point(every minute)"
            });
            rtn.push({
                value: "5",
                text: "TOP "+this.statisticsRow+" URI at ErrorStatus highest point(every minute)"
            });
            rtn.push({
                value: "6",
                text: "TOP  "+this.statisticsRow+" Visitors(IP) at ErrorStatus highest point(every minute)"
            });
            return rtn;
        },
    },
    watch: {
        statisticsRow() {
            this.getStatistics();
        },
        timeCondition() {
            this.multilineChartData();
        },
        differenceKind() {
            this.setSearchKind();
            this.getStatistics();
            this.multilineChartData();
        }
    },

    methods: {

        setSearchKind() {
            // statisticsKind = 30. Defference : Total Number of Requests (count)
            // statisticsKind = 31. Defference : TPS Requests Top N at TPS peak
            // statisticsKind = 32. Defference : TPS Visitors Top N at TPS peak
            // statisticsKind = 33. Defference : timeTaken Requests Top N at TPS peak
            // statisticsKind = 34. Defference : timeTaken Visitors Top N at TPS peak
            // statisticsKind = 35. Defference : status Requests Top N at TPS peak
            // statisticsKind = 36. Defference : status Visitors Top N at TPS peak

            // multilineChartKind = 0 : request
            // multilineChartKind = 1 : TPS 
            // multilineChartKind = 2 : timeTaken  
            // multilineChartKind = 3 : status       

            // differenceKind = 0 : 전체 request 건수 비교 > 30%
            // differenceKind = 1 : TPS 최고점 TOP N개 URI 비율 비교(1분 단위)
            // differenceKind = 2 : TPS 최고점 TOP N개 IP 비율 비교(1분 단위)
            // differenceKind = 3 : 처리시간 최고점 TOP N개 URI 비율 비교(1분 단위)
            // differenceKind = 4 : 처리시간 최고점 TOP N개 IP 비율 비교(1분 단위)
            // differenceKind = 5 : 오류코드(4xx,5xx) 합계 > 10% 경우, 최고점 TOP N개 URI 비율 비교
            // differenceKind = 6 : 오류코드(4xx,5xx) 합계 > 10% 경우, 최고점 TOP N개 IP 비율 비교
            if (this.differenceKind == 0 ){
                this.statisticsKind = 30
                this.multilineChartKind = 0
            } else if (this.differenceKind == 1 ){
                this.statisticsKind = 31
                this.multilineChartKind = 1
            } else if (this.differenceKind == 2 ){
                this.statisticsKind = 32
                this.multilineChartKind = 1
            } else if (this.differenceKind == 3 ){
                this.statisticsKind = 33
                this.multilineChartKind = 2
            } else if (this.differenceKind == 4 ){
                this.statisticsKind = 34
                this.multilineChartKind = 2
            } else if (this.differenceKind == 5 ){
                this.statisticsKind = 35
                this.multilineChartKind = 3
            } else if (this.differenceKind == 6 ){
                this.statisticsKind = 36
                this.multilineChartKind = 3
            } 
        },

        resetZoom() {       

        this.$refs.mlChart._data._chart.resetZoom();

        },

        getFilter1() {

            let filter = {
                dateFromValue: this.dateFromValue,
                dateToValue: this.dateToValue,
                timeFromValue: this.timeFromValue,
                timeToValue: this.timeToValue,

                conditionValue: this.conditionValue,
                searchValue: this.searchValue,
                excludeSearch: this.excludeSearch,

                ttFromValue: this.ttFromValue,
                ttToValue: this.ttToValue,
                project_id: this.project_id,
            }

            return filter
        },

        getFilter2() {

            let filter = {
                dateFromValue: this.dateFromValue2,
                dateToValue: this.dateToValue2,
                timeFromValue: this.timeFromValue2,
                timeToValue: this.timeToValue2,

                conditionValue: this.conditionValue2,
                searchValue: this.searchValue2,
                excludeSearch: this.excludeSearch2,

                ttFromValue: this.ttFromValue2,
                ttToValue: this.ttToValue2,
                project_id: this.project_id,
            }

            return filter
        },

        showAlert() {
        
            this.$swal('Hello Vue world!!!');
            },

            clickClose: function () {
            
                this.$emit('popupClose');
            
        },

        getDetail(result, date, id) {
            this.$store.state.popupKind = 'Differences';
            this.$store.state.popupHeader = 'Differnce Detail';
            this.$store.state.detailcondition = this.statisticsKind;
            this.$store.state.detailsearchKeyword = result;
            this.$store.state.popupBody = 'searchKeyword : ' + this.$store.state.detailsearchKeyword;
            this.$store.state.popupButton = 'Close';
            this.$store.state.popupDate = date;
            this.$store.state.popupDiffId = id;
            if(date != '') this.currentView = 'DetailPopup';
        },

        getXaxisDatetimeFilter(filter1, filter2) {

            var x_min1 = filter1.dateFromValue+filter1.timeFromValue
            var x_max1 = filter1.dateToValue+filter1.timeToValue
            var x_min2 = filter2.dateFromValue+filter2.timeFromValue
            var x_max2 = filter2.dateToValue+filter2.timeToValue

            //시간 차이 구하기
            // const moment = require('moment');

            var dateStart = moment(x_min1, 'YYYYMMDDhhmmss')
            var dateEnd = moment(x_max1, 'YYYYMMDDhhmmss')
            var dateDif1 = dateEnd.diff(dateStart, 'seconds')       

            dateStart = moment(x_min2, 'YYYYMMDDhhmmss')
            dateEnd = moment(x_max2, 'YYYYMMDDhhmmss')
            var dateDif2 = dateEnd.diff(dateStart, 'seconds')     

            // Chart X축 min/max기준을 조회기간이 긴 조회조건으로 동일하게 설정. scale 맞추기.
            if(dateDif1 > dateDif2){
                x_max2 = moment(x_max2, 'YYYYMMDDhhmmss').add(dateDif1-dateDif2, 'seconds')
            } else if(dateDif1 < dateDif2) {
                x_max1 = moment(x_max1, 'YYYYMMDDhhmmss').add(dateDif2-dateDif1, 'seconds')
            } 

            let x_datetime = {
                x_min1: x_min1,
                x_max1: x_max1,
                x_min2: x_min2,
                x_max2: x_max2
            }

            return x_datetime
        },

        setStatisticItems(results1, totalCnt1, resultType1, results2, totalCnt2, resultType2) {

            this.items = []

            //Search-1
            for (let i = 0; i < results1.length; i++) {

                var ratio = ""
                var result_count = ""

                // 소수 3째자리에서 반올림
                let pos = Math.pow(10, 3);
                let val = Math.round((results1[i].result_count / totalCnt1) * pos * 100) / pos;
                let percentile = val.toFixed(2);
                ratio = percentile + "%";

                // 숫자 3자리(천단위) 마다 "," 표시
                result_count = results1[i].result_count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

                this.items.push({
                    index: i+1,
                    result: results1[i].result,
                    result_count: result_count,
                    ratio: ratio,
                    date: results1[i].result_date
                })

                if (results1[i].timetakenUnit == 'D') {
                    this.timetakenUnit = "( ㎲ )"
                } else if (results1[i].timetakenUnit == 'T') {
                    this.timetakenUnit = "( s )"
                }
            }

            //Search-2
            for (let i = 0; i < results2.length; i++) {

                var ratio = ""
                var result_count = ""              

                // 소수 3째자리에서 반올림
                let pos = Math.pow(10, 3);
                let val = Math.round((results2[i].result_count / totalCnt2) * pos * 100) / pos;
                let percentile = val.toFixed(2);
                ratio = percentile + "%";

                // 숫자 3자리(천단위) 마다 "," 표시
                result_count = results2[i].result_count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

                // 같은 result가 존재하는지 확인. 존재 시 같은 row에 count_2, percent_2입력, 미존재 시 New row 생성. 
                let check = 0;
                for (let j = 0; j < this.items.length; j++) {
                    if(this.items[j].result == results2[i].result){
                        this.items[j].result_count2 = result_count
                        this.items[j].ratio2 = ratio
                        this.items[j].date2 = results2[i].result_date
                        check=1
                        break
                    }
                }

                if(check==0){
                    this.items.push({
                    index: 'New',
                    result: results2[i].result,
                    result_count2: result_count,
                    ratio2: ratio,
                    date2: results2[i].result_date
                    })
                }

                if (results2[i].timetakenUnit == 'D') {
                    this.timetakenUnit = "( ㎲ )"
                } else if (results2[i].timetakenUnit == 'T') {
                    this.timetakenUnit = "( s )"
                }
            }
            //Stop Loading Spinner
            this.isActiveStatistic = false
        },
   
        async getStatistics() {

            let commonInfo = setCommonStatisticInfo(this.statisticsKind, this.project_id, this.getFilter1(), this.statisticsRow);

            this.TopN = "Top " + this.statisticsRow
            this.content = commonInfo.content

            // Start Loading Spinner
            this.isActiveStatistic = true

            await axios.post(commonInfo.url, commonInfo.postData, commonInfo.axiosConfig)
                .then(res => {
                    // console.log(res)
                    this.tmp_res1 = res
                })
                .catch(err => {
                    console.error(err);
                    //Stop Loading Spinner
                    this.isActiveStatistic = false
                })

            commonInfo = setCommonStatisticInfo(this.statisticsKind, this.project_id, this.getFilter2(), this.statisticsRow);

            await axios.post(commonInfo.url, commonInfo.postData, commonInfo.axiosConfig)
                .then(res => {
                    // console.log(res)
                    this.tmp_res2 = res
                })
                .catch(err => {
                    console.error(err);
                    //Stop Loading Spinner
                    this.isActiveStatistic = false
                })

            // console.log("statistics_res1", this.tmp_res1)
            // console.log("statistics_res2", this.tmp_res2) 

            // Search-1:tmp_res1, Search-2:tmp_res2 한번에 조회해서 subTitle, Statistic 데이터 입력
            let dateTmp1 = this.tmp_res1.data.results[0].result_date
            let peakTime1 = dateTmp1.substr(0,4)+"/"+dateTmp1.substr(4,2)+"/"+dateTmp1.substr(6,2)+" "+dateTmp1.substr(8,2)+":"+dateTmp1.substr(10,2)
            let dateTmp2 = this.tmp_res2.data.results[0].result_date
            let peakTime2 = dateTmp2.substr(0,4)+"/"+dateTmp2.substr(4,2)+"/"+dateTmp2.substr(6,2)+" "+dateTmp2.substr(8,2)+":"+dateTmp2.substr(10,2)

            // 숫자 3자리(천단위) 마다 "," 표시
            let request_total1 = this.tmp_res1.data.totalCnt.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
            let request_total2 = this.tmp_res2.data.totalCnt.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

            if( this.statisticsKind == 30 ){
                this.subTitle1 = "Reqeust Counts : " + request_total1 + " / Comapre to Search-2 : " + Math.round((this.tmp_res1.data.totalCnt / this.tmp_res2.data.totalCnt) * 10000) / 100 + "%"
                this.subTitle2 = "Reqeust Counts : " + request_total2 + " / Comapre to Search-1 : " + Math.round((this.tmp_res2.data.totalCnt / this.tmp_res1.data.totalCnt) * 10000) / 100 + "%"
            } else {
                this.subTitle1 = "Highest point : " + peakTime1 + " , Reqeust Counts : " + request_total1
                this.subTitle2 = "Highest point : " + peakTime2 + " , Reqeust Counts : " + request_total2
            }  

            this.setStatisticItems(this.tmp_res1.data.results, this.tmp_res1.data.totalCnt, this.tmp_res1.data.resultType, this.tmp_res2.data.results, this.tmp_res2.data.totalCnt, this.tmp_res2.data.resultType)
        },

        // 시계열 분석용 Line Chart
        async multilineChartData() {

            this.isActiveMultiLine = true

            try {
                let filter1 = this.getFilter1();
                let filter2 = this.getFilter2();

                let x_datetime = this.getXaxisDatetimeFilter(filter1, filter2)
                
                // kind = 0 : request
                // kind = 1 : TPS
                // kind = 2 : timeTaken  
                // kind = 3 : status 
                
                let res1 = await getLineChartDataDiff(this.multilineChartKind, this.timeCondition, this.project_id, filter1)
                let res2 = await getLineChartDataDiff(this.multilineChartKind, this.timeCondition, this.project_id, filter2)

                // console.log("res1", res1)
                // console.log("res2", res2)                   

                if (this.multilineChartKind == 0){
                    this.mlChartData = getMultiLineChartTemplateDiff('Search-1(request)', res1.xy, 'Search-2(request)', res2.xy)                    
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(request) / Search-2(request)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "request")
                } else if (this.multilineChartKind == 1){
                    this.mlChartData = getMultiLineChartTemplateDiff('Search-1(TPS)', res1.xy, 'Search-2(TPS)', res2.xy)                    
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(TPS) / Search-2(TPS)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "TPS")
                } else if (this.multilineChartKind == 2){
                    this.mlChartData = getMultiLineChartTemplateDiff('Search-1(Duration(s))', res1.xy, 'Search-2(Duration(s))', res2.xy)                    
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(Duration(s)) / Search-2(Duration(s))', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "Duration(s)")
                } else if (this.multilineChartKind == 3) {
                    this.mlChartData = getMultiLineChartTemplateStatusDiff('Search-1(Status400)', res1.xy_400, 'Search-1(Status500)', res1.xy_500, 'Search-2(Status400)', res2.xy_400, 'Search-2(Status500)', res2.xy_500)                   
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(Status) / Search-2(Status)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, 'request(Count)')
                }

            } catch (err) {
                console.error(err); // TypeError: failed to fatch

            } finally {
                this.isActiveMultiLine = false

            }
        },
  },
};
</script>

<style scoped>
.table-summary {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-end;
    align-items: center;

    font-size: 14px;
    padding: 12px 48px;
    background-color: #F6F6F6;
}
.table-summary-title {
    display: flex;
    font-weight: bold;
    margin-right: auto;
}
.table-summary-item {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
}
.table-summary-item + .table-summary-item {
    margin-left: 48px;
}

.popup-container {
    padding: 32px;
    border: 1px solid #D0D0D0;
    background-color: white;
}

.popup-header {
    position: relative;
    display: flex;
    flex-flow: column nowrap;

}

.popup-header__title {
    font-size: 24px;
    font-weight: bold;
}

.popup-header__close {
    position: absolute;
    top: 0;
    right: 0;
}

.popup-header__close:hover {
    cursor: pointer;
}

.popup-body {
    font-size: 18px;
    margin: 20px 0;
    word-break: break-all;
}

.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 0px;
}

.popup-form .ui-form-item {
    margin-top: 32px;
}

.modal-mask {
    position: fixed;
    z-index: 9997;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity .3s ease;
}

.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}

.modal-container {
    width: 50%;
    height: 80%;
    margin: 0px auto;
    padding: 20px 20px 20px 20px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
    overflow-y: auto; 
    max-height: 900px;
}

.modal-header {
    margin-top: 0;
    color: #42b983;
}

.modal-body {
    margin: 20px 0;
}

.modal-button {
    float: right;
}

.modal-enter,
.modal-leave {
    opacity: 0;
}

.modal-enter .modal-container,
.modal-leave .modal-container {
    transform: scale(1.1);
}

.add_scroll {
    max-height: 260px;
    overflow-y: auto;
}

</style>