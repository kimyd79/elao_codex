<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">      
      <ui-container-box :columns=14 vertical class="modal-container">

        <div class="popup-header">
            <div class="popup-header__title"> 
                Finding Differences               
            </div>
            <div class="popup-header__close">
                <lego-icon small v-on:click="clickClose">close</lego-icon>
            </div>

            <ui-container-box :columns="13" horizontal align-center class="page-form-area">
    
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
       
        <ui-container-box :columns="13" horizontal align-center class="page-form-area">
            <div class="vld-parent">
                <component :is="currentView" v-on:popupClose="currentView=null" :finding="finding"></component>
                <vue-element-loading :active="isActiveStatistic" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                <div class="add_scroll">
                    <table class="page-summary-table">
                        <thead>
                            <tr>
                                <th rowspan="2" style="width: 60px; color: rgb(85,60,165)"><b>Num</b></th>
                                <th rowspan="2" style="width: 700px; color: rgb(85,60,165)"><b>Finding description</b></th>
                                <th rowspan="2" style="width: 300px; color: rgb(85,60,165)"><b>Item</b></th>
                                <th colspan="2" style="width: 100px; color: rgb(85,60,165)"><b>Findings-1 </b></th>
                                <th colspan="2" style="width: 100px; color: rgb(85,60,165)"><b>Findings-2</b></th>
                            </tr>
                            <tr>
                                <th style="width: 100px; color: rgb(85,60,165)"><b>count </b></th>
                                <th style="width: 100px; color: rgb(85,60,165)"><b>percent</b></th>
                                <th style="width: 100px; color: rgb(85,60,165)"><b>count </b></th>
                                <th style="width: 100px; color: rgb(85,60,165)"><b>percent </b></th>
                            </tr>
                        </thead>
                        <tbody>

                            <tr v-for="(item, idx) in items" :key="idx">
                                <td>{{ idx+1 }}</td>                                
                                <td style="cursor:pointer" v-on:click="multilineChartData(item)">{{ item.description }}</td>
                                <td style="cursor:pointer" v-on:click="multilineChartData(item)">{{ item.result }}</td>
                                <!-- <td style="cursor:pointer" v-on:click="getMetricDetailSearch(item)"><u>{{ item.result_count }}</u></td>
                                <td style="cursor:pointer" v-on:click="getMetricDetailSearch(item)"><u>{{ item.ratio }}</u></td>
                                <td style="cursor:pointer" v-on:click="getMetricDetailSearch2(item)"><u>{{ item.result_count2 }}</u></td>
                                <td style="cursor:pointer" v-on:click="getMetricDetailSearch2(item)"><u>{{ item.ratio2 }}</u></td>
                                <td style="cursor:pointer" v-on:click="getMetricDetailSearch2(item)"><u>{{ item.ratio2 }}</u></td> -->

                                <td v-if="item.ratio > item.ratio2" style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 1)"><u><b>{{ item.result_count }}</b></u></td>
                                <td v-else style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 1)"><u>{{ item.result_count }}</u></td>

                                <td v-if="item.ratio > item.ratio2" style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 1)"><u><b>{{ item.ratio }}</b></u></td>
                                <td v-else style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 1)"><u>{{ item.ratio }}</u></td>

                                <td v-if="item.ratio < item.ratio2" style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 2)"><u><b>{{ item.result_count2 }}</b></u></td>
                                <td v-else style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 2)"><u>{{ item.result_count2 }}</u></td>

                                <td v-if="item.ratio < item.ratio2" style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 2)"><u><b>{{ item.ratio2 }}</b></u></td>
                                <td v-else style="cursor:pointer" v-on:click="getMetricDetailSearch(item, 2)"><u>{{ item.ratio2 }}</u></td>

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
            <lego-button @click="setScaleY(1)" small>setScaleY</lego-button>
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
    getLineChartDataDiff,
    getMultiLineChartOptions2Diff,
    getMultiLineChartTemplate2Diff,
    serverUrl,
    setFindingDetailCondition
} from "@/common"
import {
    mapGetters
} from "vuex";
import VueElementLoading from 'vue-element-loading'
import UIFormRow from './form/UIFormRow.vue';
import ChartLine from "@/components/layout/ChartLine";
import DetailPopup from './DetailPopup';
import DetailPopup2 from './DetailPopup2';
import moment from 'moment'
export default {

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
            
            title: ' URI at TPS peak',
            subTitle1: '...',
            subTitle2: '...',
            dateTime1: '...',
            dateTime2: '...',
            TopN: '',
            content: '',
            tmp_res1: [],
            tmp_res2: [], 
            tmp_res3: [],
            tmp_res4: [], 
            timetakenUnit: "",
            currentView: null,

            // For Chart
            resetZoomV: "1",
            timeCondition: "1", // "Hour(시) 기준"

            mlChartData: null,
            mlOptions: getMultiLineChartOptionsDiff('- No Data -'),

            items: [],

            finding: [{
                description: '',
                result: '',
                result_count: '',
                ratio: '',      
                result_count2: '',
                ratio2: '',           
                metric_id: '',
                metric_kind: '',
                metric_type: '',
                metric_filter: '',
                metric_filter2: '',
                metric_unit: '',
                metric_value1: '',
                metric_value2: '',
                metric_static: '',
            }],


            // For Loading Spinner
            isActiveMultiLine: false,
            isActiveStatistic: false,

            initailChartData: null
        }
    },

    created() {
        // TODO: Check! mapGetter로 가능?
        // this.logfile_id = this.$store.state.logFileID
        // this.project_id = this.$store.state.projectID
        // this.differenceKind = "0"
        // this.multilineChartData();
        this.getMetrics();
        this.isActiveMultiLine = true

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

            detailconditionValue: "getDetailCondition",
            detailsearchValue: "getDetailSearchKeyword",

            //logfile_id: "getLogFileID",
            project_id: "getProjectID",
            logFormat: "getLogFormat",

        }),
    },
    watch: {
        timeCondition() {
            this.multilineChartData(this.finding);
        },
        initailChartData(){
            this.multilineChartData(this.initailChartData)
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

        getMetricDetailSearch(finding, idx) {            
            this.finding = finding
            if (finding.result == 'count') {
                this.$store.dispatch("setDetailSearchKeyword", "");
            } else{
                this.$store.dispatch("setDetailSearchKeyword", finding.result);
            }            
            this.$store.dispatch("setDetailCondition", finding.metric_filter);                        
            this.$store.dispatch("setPopupBody", finding.description);
            this.$store.dispatch("setPopupButton", 'Close');               
            if (idx == 1){
                this.$store.dispatch("setPopupKind", 'FindingsDetail');
                this.$store.dispatch("setPopupHeader", 'Findings Detail-1');
                this.currentView = 'DetailPopup';
            } else {
                this.$store.dispatch("setPopupKind", 'FindingsDetail2');
                this.$store.dispatch("setPopupHeader", 'Findings Detail-2');
                this.currentView = 'DetailPopup2';
            }
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

        setFindingsItems(result1, result1_count, result2, result2_count) {
            // console.log("findings result1 : ", result1)
            // console.log("findings result2 : ", result2)

            this.subTitle1 = "Total number of Requests : " + result1_count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
            this.subTitle2 = "Total number of Requests : " + result2_count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

            //Search-1
            for (let i = 0; i < result1.length; i++) {      
                        
                // 0인거 제외 : Test시에는 열어둔다.
                if (result1[i].results.length == 0 || result1[i].results[0].result_count == 0 || result1[i].results[0].result_count == ''){
                    continue;
                }

                // Kind : threshold, scope, pattern
                // [Info] Response time ＞ 3 (sec) : 769 (count)
                // [Info] Response time 3 ~ 5 (sec) : 769 (count)
                // [Warn] Response specific string for URI ＞ 30 (%) : 769 (count)

                var description = "["+result1[i].metric_type+"] "+ result1[i].metric_definition + " ";
                                        
                if (result1[i].metric_kind == 'scope'){
                    description += result1[i].metric_value1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " ~ " + result1[i].metric_value2.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                }else {

                    if (result1[i].metric_kind == 'pattern'){ 
                        description += " [pat='"+ result1[i].metric_value2 +"']";
                    }

                    // threshold
                    description += " > " + result1[i].metric_value1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                }
                
                description += " ("+result1[i].metric_unit+")";

                for (let j = 0; j < result1[i].results.length; j++) {   

                    this.items.push({
                        description: description,
                        result: result1[i].results[j].result,
                        result_count: result1[i].results[j].result_count,
                        ratio: result1[i].results[j].result_per,
                        metric_id: result1[i].metric_id,
                        metric_kind: result1[i].metric_kind,
                        metric_type: result1[i].metric_type,
                        metric_filter: result1[i].metric_filter,
                        metric_filter2: result1[i].metric_filter2,
                        metric_unit: result1[i].metric_unit,
                        metric_value1: result1[i].metric_value1,
                        metric_value2: result1[i].metric_value2,
                        metric_static: result1[i].metric_static,
                    });
                }
            };

            //Search-2
            for (let i = 0; i < result2.length; i++) {      
                        
                // 0인거 제외 : Test시에는 열어둔다.
                if (result2[i].results.length == 0 || result2[i].results[0].result_count == 0 || result2[i].results[0].result_count == ''){
                    continue;
                }

                // Kind : threshold, scope, pattern
                // [Info] Response time ＞ 3 (sec) : 769 (count)
                // [Info] Response time 3 ~ 5 (sec) : 769 (count)
                // [Warn] Response specific string for URI ＞ 30 (%) : 769 (count)

                description = "["+result2[i].metric_type+"] "+ result2[i].metric_definition + " ";
                                        
                if (result2[i].metric_kind == 'scope'){
                    description += result2[i].metric_value1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " ~ " + result2[i].metric_value2.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                }else {

                    if (result2[i].metric_kind == 'pattern'){ 
                        description += " [pat='"+ result2[i].metric_value2 +"']";
                    }

                    // threshold
                    description += " > " + result2[i].metric_value1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                }
                
                description += " ("+result2[i].metric_unit+") → ";

                // 같은 result가 존재하는지 확인. 존재 시 같은 row에 count_2, percent_2입력, 미존재 시 New row 생성. 

                for (let j = 0; j < result2[i].results.length; j++) {
                    let check = 0;
                    for (let k = 0; k < this.items.length; k++) {
                        check = 0;                     
                        if(this.items[k].metric_id == result2[i].metric_id && this.items[k].result == result2[i].results[j].result){                                                     
                            this.items[k].result_count2 = result2[i].results[j].result_count
                            this.items[k].ratio2 = result2[i].results[j].result_per   
                            check=1
                            break
                        }                        
                    }
                    if(check==0){
                        this.items.push({
                            // index: 'New',
                            description: description,
                            result: result2[i].results[j].result,
                            result_count2: result1[i].results[j].result_count,
                            ratio2: result2[i].results[j].result_per,               
                            metric_id: result2[i].metric_id,
                            metric_kind: result2[i].metric_kind,
                            metric_type: result2[i].metric_type,
                            metric_filter: result2[i].metric_filter,
                            metric_filter2: result2[i].metric_filter2,
                            metric_unit: result2[i].metric_unit,
                            metric_value1: result2[i].metric_value1,
                            metric_value2: result2[i].metric_value2,
                            metric_static: result2[i].metric_static,
                        })
                    }
                }
            }

            this.initailChartData = this.items[0]
                
            //Stop Loading Spinner
            this.isActiveStatistic = false
        },
   
        async getMetrics() {                    

            // Start Loading Spinner
            this.isActiveStatistic = true

            let postData = {
                project_id: this.project_id,
                filter: this.getFilter1(),
            };            

            await axios
                .post(serverUrl + "/logdetail_dynamic/findings/", postData)
                .then(res => {
                    this.tmp_res1 = res
                })
                .catch(err => {
                    console.error(err);
                    this.isActive = false;
                });           


            let postData2 = {
                project_id: this.project_id,
                filter: this.getFilter2(),
            }; 

            await axios
                .post(serverUrl + "/logdetail_dynamic/findings/", postData2)
                .then(res => {
                    this.tmp_res2 = res 
                })
                .catch(err => {
                    console.error(err);
                    this.isActive = false;
                });

            this.setFindingsItems(this.tmp_res1.data.findingsResult, this.tmp_res1.data.totalCnt, this.tmp_res2.data.findingsResult, this.tmp_res2.data.totalCnt)
    
        },

        // 시계열 분석용 Line Chart
        async multilineChartData(finding) {
            this.finding = finding
            this.isActiveMultiLine = true

            let chartDescription = finding.description

            if (finding.result == 'count') {
                this.$store.dispatch("setDetailSearchKeyword", "");
            } else{
                this.$store.dispatch("setDetailSearchKeyword", finding.result);
                chartDescription = chartDescription+"-"+finding.result
            }
            this.$store.dispatch("setDetailCondition", finding.metric_filter);            

            try {
                // Kind = 0 : request(요청) 건수(count)
                // Kind = 1 : TPS
                // Kind = 2 : time-taken(평균처리시간) 
                // Kind = 3 : Status code(2XX, 3XX)
                // Kind = 4 : request + time-taken
                // Kind = 5 : Status code(2XX, 3XX, 4XX, 5XX)
                
                this.multilineChartKind = 4                

                let ttFromValueThreshold = ''
                let ttToValueThreshold = ''
                let byteFromValueThreshold = ''
                let byteToValueThreshold = ''
                let staticValue = ''

                // this.getFindingDetailCondition() 
                setFindingDetailCondition()

                if (this.finding.metric_static == 'Y'){
                    staticValue = 'T'
                }

                // timetaken 값은 microseconds -> ms 단위로 처리한다.(/1000)
                // logdetail_dynamic ftime_taken, fbyte between 조회
                if (finding.metric_kind == 'threshold'){
                    if (finding.metric_unit == 'micros'){
                        ttFromValueThreshold = finding.metric_value1 / 1000
                        ttToValueThreshold = 24*60*60*1000 
                    } else if (finding.metric_unit == 'millis'){
                        ttFromValueThreshold = finding.metric_value1
                        ttToValueThreshold = 24*60*60*1000
                    } else if (finding.metric_unit == 'byte'){
                        byteFromValueThreshold = finding.metric_value1
                        byteToValueThreshold = 1024*1024*1024*1024
                    } 
                } else if (finding.metric_kind == 'scope'){
                    if (finding.metric_unit == 'micros'){
                        ttFromValueThreshold = finding.metric_value1 / 1000
                        ttToValueThreshold =  finding.metric_value2 / 1000
                    } else if (finding.metric_unit == 'millis'){
                        ttFromValueThreshold = finding.metric_value1
                        ttToValueThreshold = finding.metric_value2
                    } else if (finding.metric_unit == 'byte'){
                        byteFromValueThreshold = finding.metric_value1
                        byteToValueThreshold = finding.metric_value2
                    } 
                }

                let filter1 = this.getFilterChart1();

                filter1['ttFromValue'] = ttFromValueThreshold;
                filter1['ttToValue'] = ttToValueThreshold;
                filter1['byteFromValue'] = byteFromValueThreshold;
                filter1['byteToValue'] = byteToValueThreshold;
                filter1['staticValue'] = staticValue;

                let res1 = await getLineChartDataDiff(this.multilineChartKind, this.timeCondition, this.project_id, filter1)


                let filter2 = this.getFilterChart2();

                filter2['ttFromValue'] = ttFromValueThreshold;
                filter2['ttToValue'] = ttToValueThreshold;
                filter2['byteFromValue'] = byteFromValueThreshold;
                filter2['byteToValue'] = byteToValueThreshold;
                filter2['staticValue'] = staticValue;
                

                let res2 = await getLineChartDataDiff(this.multilineChartKind, this.timeCondition, this.project_id, filter2)

                let x_datetime = this.getXaxisDatetimeFilter(filter1, filter2)

                // console.log("res1", res1)
                // console.log("res2", res2)                   

                this.content = 'Request/timeTaken'
                this.mlChartData = getMultiLineChartTemplate2Diff('Search-1(request)', res1.xy, 'Search-1(timeTaken)', res1.xy2, 'Search-2(request)', res2.xy, 'Search-2(timeTaken)', res2.xy2)                    
                this.mlOptions = getMultiLineChartOptions2Diff(chartDescription , x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "Request(s)", "timeTaken(s)")
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
    width: 480px
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
    max-height: 930px;
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

.page-form-area {
    padding: 10px 0;
    border-bottom: 1px solid #CCCCCC;
}

</style>