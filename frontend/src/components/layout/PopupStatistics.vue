<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">      
        <ui-container-box :columns=14 vertical class="modal-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Statistic Differences : {{ this.content }}
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickClose">close</lego-icon>
                </div>

                <ui-container-box :columns="13" horizontal align-center class="page-form-area" >

                    <div><b>* Select N</b></div>
                    <lego-dropdown :items="listN" v-model="statisticsRow" width="100px" align-left/>

                    <div class="table-summary" >
                        <div class="table-summary-items" >
                            <div style="color:#553ca5"><b>* Search-1</b></div>
                            <div>{{ this.subTitle1 }}</div>
                            <div>{{ this.dateTime1 }}</div>
                        </div>
                        <div class="table-summary-items" >
                            <div style="color:#553ca5"><b>* Search-2</b></div>
                            <div>{{ this.subTitle2 }}</div>
                            <div>{{ this.dateTime2 }}</div>
                        </div>
                    </div>
                    
                </ui-container-box>
            </div>
        
            <ui-container-box :columns="13" horizontal align-center>
                <div class="vld-parent">
                    <component :is="currentView" v-on:popupClose="currentView=null"></component>
                    <vue-element-loading :active="isActiveStatistic" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                    <div class="add_scroll">
                        <table class="page-summary-table">
                            <thead>
                                <tr>
                                    <th class="sticky-th" rowspan="2" style="width: 60px; color: rgb(85,60,165)"><b>{{ this.TopN }}</b></th>
                                    <th class="sticky-th" rowspan="2" style="width: 580px; color: rgb(85,60,165)"><b>{{ this.content }}</b></th>
                                    <th class="sticky-th" colspan="2" style="width: 200px; color: rgb(85,60,165)"><b>Search-1 </b></th>
                                    <th class="sticky-th" colspan="2" style="width: 200px; color: rgb(85,60,165)"><b>Search-2</b></th>
                                </tr>
                                <tr>
                                    <th class="sticky-th-two" style="width: 100px; color: rgb(85,60,165)"><b>{{ this.result }}</b></th>
                                    <th class="sticky-th-two" style="width: 100px; color: rgb(85,60,165)"><b>percent</b></th>
                                    <th class="sticky-th-two" style="width: 100px; color: rgb(85,60,165)"><b>{{ this.result }}</b></th>
                                    <th class="sticky-th-two" style="width: 100px; color: rgb(85,60,165)"><b>percent </b></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in items">
                                    <td>{{ item.index }} </td>                                    
                                    <td v-on:click="setMultiLineChart(item.result)"><VueCustomTooltip :label="item.result">
                                        {{ item.result_count != 0 ? item.result.substr(0,70)+(item.result.length > 70 ? " ..." : "" ) : "-"}}
                                        </VueCustomTooltip>
                                    </td>
                                    <td style="cursor:pointer" v-on:click="getDetail(item.result, 1)"><u>{{ item.result_count }}</u></td>
                                    <td style="cursor:pointer" v-on:click="getDetail(item.result, 1)"><u>{{ item.ratio }}</u></td>
                                    <td style="cursor:pointer" v-on:click="getDetail(item.result, 2)"><u>{{ item.result_count2 }}</u></td>
                                    <td style="cursor:pointer" v-on:click="getDetail(item.result, 2)"><u>{{ item.ratio2 }}</u></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

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
                        <lego-button @click="setScaleY(1)" small>setScaleY</lego-button>
                        </ui-form-row>            
                        
                        <chart-line ref='mlChart' :chart-data="mlChartData" :options="mlOptions"></chart-line>  
                    </div>

                    <div class="popup-buttons">
                        <lego-button main v-on:click="clickClose">Close</lego-button>            
                    </div>
                </div>
            </ui-container-box> 

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
    getLineChartDataDiff,
    setDetailCondition
} from "@/common"

import {
    mapGetters
} from "vuex";
import VueElementLoading from 'vue-element-loading'
import UIFormRow from './form/UIFormRow.vue';
import ChartLine from "@/components/layout/ChartLine";
import DetailPopup from './DetailPopup';
import DetailPopup2 from './DetailPopup2';
import moment from 'moment';
export default {

    props: ['row', 'kind'],

    components: {
        VueElementLoading,
        UIFormRow,
        ChartLine,
        DetailPopup,
        DetailPopup2,
        moment
    },
  
    data() {
        return {

            // kind = 0 : request  
            // kind = 1 : TPS  
            // kind = 2 : timeTaken  
            // kind = 3 : status
            // kind = 4 : request / timeTaken

            // multilineChartKind: this.kind,
            multilineChartKind: 1,

            // For Chart
            resetZoomV: "1",
            timeCondition: "1", // "Hour(시) 기준"

            mlChartData: null,
            mlOptions: getMultiLineChartOptionsDiff(this.content),
            // mlOptions: getMultiLineChartOptionsDiff('- No Data -'),
            initailChartData: '',

            // For Statistics,
            statisticsRow: this.row,
            statisticsKind: this.kind,
          
            title: ' URI at TPS peak',
            subTitle1: '...',
            subTitle2: '...',
            dateTime1: '...',
            dateTime2: '...',
            TopN: '',
            content: '',
            result: '',
            tmp_res1: [],
            tmp_res2: [], 
            timetakenUnit: "",
            currentView: null,

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

            logfile_id: '',
            project_id: '',

            // For Loading Spinner
            isActiveStatistic: false,
            isActiveMultiLine: false,
        }
    },

    created() {
        // TODO: Check! mapGetter로 가능?
        this.logfile_id = this.$store.state.logFileID
        this.project_id = this.$store.state.projectID

        this.getStatistics();
        this.multilineChartData();

        let search1_datetime1 = this.dateFromValue.substr(0,4)+"/"+this.dateFromValue.substr(4,2)+"/"+this.dateFromValue.substr(6,2)+" "+this.timeFromValue.substr(0,2)+":"+this.timeFromValue.substr(2,2)+":"+this.timeFromValue.substr(4,2)
        let search1_datetime2 = this.dateToValue.substr(0,4)+"/"+this.dateToValue.substr(4,2)+"/"+this.dateToValue.substr(6,2)+" "+this.timeToValue.substr(0,2)+":"+this.timeToValue.substr(2,2)+":"+this.timeToValue.substr(4,2)
        let search2_datetime1 = this.dateFromValue2.substr(0,4)+"/"+this.dateFromValue2.substr(4,2)+"/"+this.dateFromValue2.substr(6,2)+" "+this.timeFromValue2.substr(0,2)+":"+this.timeFromValue2.substr(2,2)+":"+this.timeFromValue2.substr(4,2)
        let search2_datetime2 = this.dateToValue2.substr(0,4)+"/"+this.dateToValue2.substr(4,2)+"/"+this.dateToValue2.substr(6,2)+" "+this.timeToValue2.substr(0,2)+":"+this.timeToValue2.substr(2,2)+":"+this.timeToValue2.substr(4,2)
        this.dateTime1 = "Date/Time : " + search1_datetime1 + " ~ " + search1_datetime2
        this.dateTime2 = "Date/Time : " + search2_datetime1 + " ~ " + search2_datetime2
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

            detailconditionValue: "getDetailCondition",
            detailsearchValue: "getDetailSearchKeyword",

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

    },
    watch: {
        statisticsRow() {
            this.getStatistics();
        },
        timeCondition() {
            this.multilineChartData();
        },
        initailChartData(){
            this.setMultiLineChart(this.initailChartData)
        }
    },

    methods: {
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

        getFilterChart1() {
            var filters="";
            filters = this.getFilter1();

            if ( this.detailcondition != '') {
               filters['detailconditionValue'] = this.detailconditionValue;
            }
            if ( this.detailsearch != '') {
                filters['detailsearchValue'] = this.detailsearchValue;
            }

            return filters
        },

        getFilterChart2() {
            var filters="";
            filters = this.getFilter2();

            if ( this.detailcondition != '') {
               filters['detailconditionValue'] = this.detailconditionValue;
            }
            if ( this.detailsearch != '') {
                filters['detailsearchValue'] = this.detailsearchValue;
            }

            return filters
        },

        showAlert() {
        
            this.$swal('Hello Vue world!!!');
        },

        clickClose: function () {
            
            this.$emit('popupClose');
            
        },

        getDetail(result, idx) {
            this.$store.dispatch("setPopupKind", 'Statistics');
            this.$store.dispatch("setDetailCondition", this.statisticsKind);
            this.$store.dispatch("setDetailSearchKeyword", result);
            this.$store.dispatch("setPopupBody", 'searchKeyword : ' + result);
            this.$store.dispatch("setPopupButton", 'Close');
            if (idx == 1){
                this.$store.dispatch("setPopupHeader", 'Statistics Detail(Search-1)');
                this.currentView = 'DetailPopup';
            } else {
                this.$store.dispatch("setPopupHeader", 'Statistics Detail(Search-2)');
                this.currentView = 'DetailPopup2';
            }
        },

        setStatisticItems(results1, totalCnt1, resultType1, results2, totalCnt2, resultType2) {

            this.items = []

            //Search-1
            for (let i = 0; i < results1.length; i++) {

                var ratio = ""
                var result_count = ""

                // 비율값이 없는 조건
                if( this.statisticsKind == 4 || this.statisticsKind == 10 || this.statisticsKind == 11 ){
                    ratio = '-'
                } else {
                    // 소수 3째자리에서 반올림
                    let pos = Math.pow(10, 3);
                    let val = Math.round((results1[i].result_count / totalCnt1) * pos * 100) / pos;
                    let percentile = val.toFixed(2);
                    ratio = percentile + "%";
                }                

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
                
                // 비율값이 없는 조건
                if( this.statisticsKind == 4 || this.statisticsKind == 10 || this.statisticsKind == 11 ){
                    ratio = '-'
                } else {
                    // 소수 3째자리에서 반올림
                    let pos = Math.pow(10, 3);
                    let val = Math.round((results2[i].result_count / totalCnt2) * pos * 100) / pos;
                    let percentile = val.toFixed(2);
                    ratio = percentile + "%";
                }

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
            this.initailChartData = this.items[0].result
            //Stop Loading Spinner
            this.isActiveStatistic = false
        },
   
        async getStatistics() {

            let commonInfo = setCommonStatisticInfo(this.statisticsKind, this.project_id, this.getFilter1(), this.statisticsRow);

            this.TopN = "Top " + this.statisticsRow
            this.content = commonInfo.content
            this.result = commonInfo.content.match(/\((.*?)\)/)[0].replaceAll(/\(|\)/g, "")
            // this.$store.dispatch("detailsearchKeyword", userName)

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
            

            // TODO: search-1, 2 결과값 0 일 경우 error 처리.
            if( this.tmp_res1.data.results.length == 0 || this.tmp_res2.data.results.length == 0 ){
                this.$swal({
                            title: 'Notification',
                            html: 'No data was retrieved..!!',
                            icon: 'error',
                            confirmButtonColor: '#553ca5',                
                            confirmButtonText: 'OK',
                        });
                this.items= [{
                    index: '',
                    result: '- No Data -',
                    result_count: '...',
                    ratio: '...',
                    date: '',
                    result_count2: '...',
                    ratio2: '...',
                    date2: ''
                }], 
                //Stop Loading Spinner
                this.isActiveStatistic = false
                
            } else {
                // Search-1:tmp_res1, Search-2:tmp_res2 한번에 조회해서 subTitle, Statistic 데이터 입력
                // 숫자 3자리(천단위) 마다 "," 표시
                let request_total1 = this.tmp_res1.data.totalCnt.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
                let request_total2 = this.tmp_res2.data.totalCnt.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

                if( this.statisticsKind == 8 ){
                    this.subTitle1 = "Total number of Bytes : " + request_total1 
                    this.subTitle2 = "Total number of Bytes : " + request_total2
                } else {
                    this.subTitle1 = "Total number of Requests : " + request_total1 
                    this.subTitle2 = "Total number of Requests : " + request_total2
                }

                this.setStatisticItems(this.tmp_res1.data.results, this.tmp_res1.data.totalCnt, this.tmp_res1.data.resultType, this.tmp_res2.data.results, this.tmp_res2.data.totalCnt, this.tmp_res2.data.resultType)
            }
        },

        setMultiLineChart(detailsearchKeyword){
            this.$store.dispatch("setDetailSearchKeyword", detailsearchKeyword);
            this.$store.dispatch("setDetailCondition", this.kind);
            this.multilineChartData()     
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

        
        // 시계열 분석용 Line Chart
        async multilineChartData() {

            this.isActiveMultiLine = true

            try {

                setDetailCondition();
                this.$store.dispatch("setDetailSearchKeyword", decodeURIComponent(this.$store.state.detailsearchKeyword));

                let filter1 = this.getFilterChart1();
                let filter2 = this.getFilterChart2();
                // console.log("filter1", filter1)
                // console.log("filter2", filter2)

                var x_datetime = this.getXaxisDatetimeFilter(filter1, filter2)
                
                // kind = 0 : request
                // kind = 1 : TPS
                // kind = 2 : timeTaken  
                // kind = 3 : status(4xx, 5xx) 
                // kind = 4 : Request + timeTaken 
                // kind = 5 : status(2xx, 3xx, 4xx, 5xx) 
                let res1 = await getLineChartDataDiff(0, this.timeCondition, this.project_id, filter1)
                let res2 = await getLineChartDataDiff(0, this.timeCondition, this.project_id, filter2)
          

                // console.log("res1", res1)
                // console.log("res2", res2)                   

                // this.content = 'Request'
                this.mlChartData = getMultiLineChartTemplateDiff('Search-1(request)', res1.xy, 'Search-2(request)', res2.xy)                    
                this.mlOptions = getMultiLineChartOptionsDiff(this.detailsearchValue, x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "request")
                // this.mlOptions = getMultiLineChartOptionsDiff(this.$store.state.detailsearchKeyword, x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "request")
                this.$refs.mlChart.renderChart(this.mlChartData, this.mlOptions);
                


            } catch (err) {
                console.error(err); // TypeError: failed to fatch

            } finally {
                this.isActiveMultiLine = false

            }
        },

        async setScaleY(chart = 1, direction) { // direction 0 : left, 1 : right

            if ( direction == undefined ){
                direction = 0;
            }

            const { value: scale_y } = await this.$swal({
                title: 'Enter value of scale Y',
                input: 'text',
                inputLabel: 'Scale Y',
                inputValue: '',
                showCancelButton: true,
                confirmButtonColor: '#553ca5',
                cancelButtonColor: '#dddddd',
                confirmButtonText: 'OK',                        
                reverseButtons: true,
                inputValidator: (value) => {
                    if (!value) {
                    return 'You need to input y scale value!'
                    }
                }
            })

            if (scale_y) {
                this.$swal(`Set scale to ${scale_y}`)
            }

            var comp;

            if (chart == 1) {
                comp = this.$refs.mlChart;
            } 

            comp.options.scales.yAxes[direction].ticks = {
                suggestedMin: 0,
                suggestedMax: scale_y
                // min: 0,
                // max: scale_y
            }

            if (chart == 1) {
                comp.renderChart(this.mlChartData, this.mlOptions);
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
    padding: 10px 20px 10px 0px;
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
    text-align: left;
}
.table-summary-items {
    display: flex;
    flex-flow: column nowrap;
    margin-left: 20px;
    text-align: left;
    width: 380px
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
    margin-top: 0px;
    margin-bottom: 0px;

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
    /* margin-top: 32px; */
    margin-top: 0px;
    margin-bottom: 0px;
}

.modal-mask {
    position: fixed;
    z-index: 1059;
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
    max-height: 700px;
    overflow-y: auto;
}

.page-summary-table {
    border-spacing: 0;
    width: 100%;
    height: 20px;
    overflow: auto;
}

.page-summary-table th, td {
    height: 25px;
    border-right: 1px solid lightgray;
}

.sticky-th {
    position: sticky;
    top: 0px;
    z-index: 1;
}

.sticky-th-two {
    position: sticky;
    top: 25px;
    z-index: 1;
}

.page-form-area {
    padding: 10px 0;
    border-bottom: 1px solid #CCCCCC;
}

</style>