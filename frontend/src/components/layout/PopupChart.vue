<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">      
        <ui-container-box :columns=14 vertical class="modal-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Chart Differences : {{ this.content }}
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickClose">close</lego-icon>
                </div>
            
                <ui-container-box :columns="13" horizontal align-center class="page-form-area">

                    <div class="table-summary">
                        <div class="table-summary-items">
                            <div style="color:#553ca5"><b>* Search-1</b></div>
                            <div>{{ this.subTitle1 }}</div>
                            <!-- <div>{{ this.dateTime1 }}</div> -->
                        </div>
                        <div class="table-summary-items">
                            <div style="color:#553ca5"><b>* Search-2</b></div>
                            <div>{{ this.subTitle2 }}</div>
                            <!-- <div>{{ this.dateTime2 }}</div> -->
                        </div>
                    </div> 
                    
                </ui-container-box>
            </div>
        
            <!-- Chart Area-->
            <!-- <span class="page-title__2label">Charts</span> -->
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
    getMultiLineChartOptions2Diff,
    getMultiLineChartTemplateStatusDiff,
    getMultiLineChartTemplateStatus2Diff,
    getMultiLineChartTemplate2Diff,
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

    props: ['kind'],

    components: {
        VueElementLoading,
        UIFormRow,
        ChartLine,  
        DetailPopup,  
        moment       
    },
  
    data() {
        return {

            // kind = 0 : request  
            // kind = 1 : TPS  
            // kind = 2 : timeTaken  
            // kind = 3 : status
            // kind = 4 : request / timeTaken

            multilineChartKind: this.kind,
            
            // title: ' URI at TPS peak',
            subTitle1: this.dateFromValue,
            subTitle2: this.dateToValue,
            TopN: '',
            content: '',
            tmp_res1: [],
            tmp_res2: [], 
            timetakenUnit: "",
            currentView: null,

            // For Chart
            resetZoomV: "1",
            timeCondition: "1", // "Hour(시) 기준"

            mlChartData: null,
            mlOptions: getMultiLineChartOptionsDiff('- No Data -'),

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
        this.multilineChartData();

        let search1_datetime1 = this.dateFromValue.substr(0,4)+"/"+this.dateFromValue.substr(4,2)+"/"+this.dateFromValue.substr(6,2)+" "+this.timeFromValue.substr(0,2)+":"+this.timeFromValue.substr(2,2)+":"+this.timeFromValue.substr(4,2)
        let search1_datetime2 = this.dateToValue.substr(0,4)+"/"+this.dateToValue.substr(4,2)+"/"+this.dateToValue.substr(6,2)+" "+this.timeToValue.substr(0,2)+":"+this.timeToValue.substr(2,2)+":"+this.timeToValue.substr(4,2)
        let search2_datetime1 = this.dateFromValue2.substr(0,4)+"/"+this.dateFromValue2.substr(4,2)+"/"+this.dateFromValue2.substr(6,2)+" "+this.timeFromValue2.substr(0,2)+":"+this.timeFromValue2.substr(2,2)+":"+this.timeFromValue2.substr(4,2)
        let search2_datetime2 = this.dateToValue2.substr(0,4)+"/"+this.dateToValue2.substr(4,2)+"/"+this.dateToValue2.substr(6,2)+" "+this.timeToValue2.substr(0,2)+":"+this.timeToValue2.substr(2,2)+":"+this.timeToValue2.substr(4,2)
        this.subTitle1 = "Date/Time : " + search1_datetime1 + " ~ " + search1_datetime2
        this.subTitle2 = "Date/Time : " + search2_datetime1 + " ~ " + search2_datetime2
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
    },
    watch: {
        statisticsRow() {
            this.getStatistics();
        },
        timeCondition() {
            this.multilineChartData();
        },
        differenceKind() {
            this.multilineChartData();
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

        showAlert() {
        
            this.$swal('Hello Vue world!!!');
        },

            clickClose: function () {
            
                this.$emit('popupClose');
            
        },

        getDetail(result, date) {  
            this.$store.dispatch("setPopupKind", 'Differences');
            this.$store.dispatch("setPopupHeader", 'Differnce Detail');
            this.$store.dispatch("setDetailCondition", this.statisticsKind);
            this.$store.dispatch("setDetailSearchKeyword", result);         
            this.$store.dispatch("setPopupBody", 'searchKeyword : ' + this.$store.state.detailsearchKeyword);
            this.$store.dispatch("setPopupButton", 'Close');
            this.$store.dispatch("setPopupDate", date); 
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
                // kind = 3 : status(4xx, 5xx) 
                // kind = 4 : Request + timeTaken 
                // kind = 5 : status(2xx, 3xx, 4xx, 5xx) 
                
                let res1 = await getLineChartDataDiff(this.multilineChartKind, this.timeCondition, this.project_id, filter1)
                let res2 = await getLineChartDataDiff(this.multilineChartKind, this.timeCondition, this.project_id, filter2)

                // console.log("res1", res1)
                // console.log("res2", res2)                   

                if (this.multilineChartKind == 0){
                    this.content = 'Request'
                    this.mlChartData = getMultiLineChartTemplateDiff('Search-1(request)', res1.xy, 'Search-2(request)', res2.xy)                    
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(request) / Search-2(request)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "request")
                } else if (this.multilineChartKind == 1){
                    this.content = 'TPS'
                    this.mlChartData = getMultiLineChartTemplateDiff('Search-1(TPS)', res1.xy, 'Search-2(TPS)', res2.xy)                    
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(TPS) / Search-2(TPS)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "TPS")
                } else if (this.multilineChartKind == 2){
                    this.content = 'Duration'
                    this.mlChartData = getMultiLineChartTemplateDiff('Search-1(Duration(s))', res1.xy, 'Search-2(Duration(s))', res2.xy)                    
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(Duration(s)) / Search-2(Duration(s))', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "Duration(s)")
                } else if (this.multilineChartKind == 3) {
                    this.content = 'Status(4xx, 5xx)'
                    this.mlChartData = getMultiLineChartTemplateStatusDiff('Search-1(4xx)', res1.xy_400, 'Search-1(5xx)', res1.xy_500, 'Search-2(4xx)', res2.xy_400, 'Search-2(5xx)', res2.xy_500)
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(Status) / Search-2(Status)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, 'request(Count)')
                } else if (this.multilineChartKind == 4) {
                    this.content = 'Request/timeTaken'
                    this.mlChartData = getMultiLineChartTemplate2Diff('Search-1(request)', res1.xy, 'Search-1(timeTaken)', res1.xy2, 'Search-2(request)', res2.xy, 'Search-2(timeTaken)', res2.xy2)                    
                    this.mlOptions = getMultiLineChartOptions2Diff('Search-1(request/timeTaken)) / Search-2(request/timeTaken)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, "Request(s)", "timeTaken(s)")
                } else if (this.multilineChartKind == 5) {
                    this.content = 'Status(2xx, 3xx, 4xx, 5xx)'
                    this.mlChartData = getMultiLineChartTemplateStatus2Diff('Search-1(2xx)', res1.xy_200, 'Search-1(3xx)', res1.xy_300, 'Search-1(4xx)', res1.xy_400, 'Search-1(5xx)', res1.xy_500, 'Search-2(2xx)', res2.xy_200, 'Search-2(3xx)', res2.xy_300, 'Search-2(4xx)', res2.xy_400, 'Search-2(5xx)', res2.xy_500)
                    this.mlOptions = getMultiLineChartOptionsDiff('Search-1(Status) / Search-2(Status)', x_datetime.x_min1, x_datetime.x_max1, x_datetime.x_min2, x_datetime.x_max2, 'request(Count)')
                }

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
    max-height: 280px;
    overflow-y: auto;
}

.page-form-area {
    padding: 10px 0;
    border-bottom: 1px solid #CCCCCC;
}

</style>