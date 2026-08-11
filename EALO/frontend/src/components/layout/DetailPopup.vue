<template>
<div class="modal-mask" transition="modal">
    <div class="modal-wrapper">
        <ui-container-box :columns=21 vertical class="modal-container">
            <div class="popup-header">
                <div class="popup-header__title">
                    {{ this.$store.state.popupHeader }} 
                </div>
                <div class="popup-header__close">
                    <lego-icon small v-on:click="clickClose">close</lego-icon>
                </div>
            </div>

            <div class="popup-body" v-html="this.$store.state.popupBody">
            </div>

            <div id="gridtable">
                <ui-container-box :columns="20" vertical>
                    <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                    <ui-container-box :columns="20" vertical>
                        <ui-table header-divider no-action :columns="columns" :items="items" class="mt8"></ui-table>
                    </ui-container-box>
                    <lego-pagination :pagination="pagingInfo" @move="pageChange" class="mt8" />
                </ui-container-box>
            </div>

            <div class="vld-parent" v-if="loaded">
                <span class="page-title__2label">Charts</span>
                <vue-element-loading :active="isActiveLineChart" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />

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
        </ui-container-box>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import store from '@/vuex/store';
import EventBus from '../../EventBus';
import * as types from "@/vuex/mutation_types";
import VueElementLoading from 'vue-element-loading'
import ChartLine from "@/components/layout/ChartLine";

import {
    mapGetters
} from 'vuex';
import {
    //getSearchFilter,
    getDetailSearchFilter,
    serverUrl,
    getLineChartTemplate,
    getLineChartOptions,
    getLineChartData,
    getMultiLineChartTemplate,
    getMultiLineChartOptions,
    setDetailCondition,
    setFindingDetailCondition
} from "@/common"

export default {
    name: 'DetailPopup',
    components: {
        // export Loading Spinner components
        VueElementLoading,
        ChartLine,
    },
    props: {
        item: {
            type: Object,
            default: function () {
                return {
                    // result: '',
                    // result_count: '',
                }
            }
        },
        popupState: '',
        finding: {
            type: Object,
            default: function () {
                return {
                    // description: '',
                    // result: '',
                    // metric_kind: '',
                    // metric_filter: '',
                    // metric_unit: '',
                    // metric_value1: '',
                    // metric_value2: '',
                }
            }
        }
    },
    data: function () {
        return {

            // For Chart
            resetZoomV: "1",
            timeCondition: "1", // "Hour(시) 기준"

            mlChartData: null,
            mlOptions: getMultiLineChartOptions('- No Data -'),
            initailChartData: '',

            // Loading Spinner
            isActive: false,
            isActiveLineChart: false,
            loaded: false,

            pagingInfo: {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 0,
                totalItems: 0
            },
            columns: [{
                    label: 'Date',
                    key: "date",
                    sortable: true,
                    sortValue: "asc",
                    filtable: false,
                    alignRight: false,
                    width: 10
                },
                {
                    label: 'Time',
                    key: "time",
                    sortable: true,
                    sortValue: "desc",
                    filtable: true,
                    filterValue: [],
                    alignRight: false,
                    width: 10
                },
                {
                    label: 'IP',
                    key: "ip",
                    sortable: false,
                    filtable: true,
                    filterValue: [],
                    alignRight: false,
                    width: 10,
                    filterList: ["Success", "Error", "Processing"]
                },
                {
                    label: 'Request',
                    key: "request",
                    sortable: false,
                    filtable: false,
                    alignRight: false,
                    width: 40
                },
                {
                    label: 'Referrer',
                    key: "referrer",
                    sortable: true,
                    sortValue: "asc",
                    filtable: true,
                    alignRight: false,
                    width: 20
                },
                {
                    label: 'UserAgent',
                    key: "useragent",
                    sortable: false,
                    filtable: false,
                    alignRight: false,
                    width: 10
                },
                {
                    label: 'Status',
                    key: "status",
                    sortable: false,
                    filtable: false,
                    alignRight: false,
                    width: 10
                },
                {
                    label: 'Byte',
                    key: "byte",
                    sortable: false,
                    filtable: false,
                    alignRight: true,
                    width: 10
                },
                {
                    label: 'TimeTaken',
                    key: "timetaken",
                    sortable: false,
                    filtable: false,
                    alignRight: true,
                    width: 10
                },
            ],

            // Grid Rows
            items: [],

            //detailPopup filter
            statusYN: ''
        };
    },

    computed: mapGetters({
        //isSearch: "getToggleSearch",

        dateFromValue: "getFromDate",
        dateToValue: "getToDate",
        timeFromValue: "getFromTime",
        timeToValue: "getToTime",

        conditionValue: "getCondition",
        searchValue: "getSearchKeyword",
        excludeSearch: "getExcludeSearch",

        ttFromValue: "getFromTimeTaken",
        ttToValue: "getToTimeTaken",

        projectID: "getProjectID",

        detailconditionValue: "getDetailCondition",
        detailsearchValue: "getDetailSearchKeyword",
        threshold: "getThreshold",

        projectServers: "getProjectServers",

    }),

    methods: {
        resetZoom() {
            this.$refs.mlChart._data._chart.resetZoom();
        },

        getDateTimeString(str) {
            //return str >= 10 ? str : "0" + str;
            return str;            
        },

        nvl(str, defaultStr) {

            if (typeof str == "undefined" || str == null || str == "")
                str = defaultStr;

            return str;
        },

        setItemList(results) {
            var dateString, timeString;

            this.items = [];

            for (let i = 0; i < results.length; i++) {
                dateString =
                    results[i].fyear +
                    "/" +
                    this.getDateTimeString(results[i].fmonth) +
                    "/" +
                    this.getDateTimeString(results[i].fday);
                timeString =
                    this.getDateTimeString(results[i].fhour) +
                    ":" +
                    this.getDateTimeString(results[i].fminute) +
                    ":" +
                    this.getDateTimeString(results[i].fsecond);

                let frequest = results[i].frequest.substring(0, 60)
                let freferrer = this.nvl(results[i].freferer, "N/A").substring(0, 30)
                let fuser_agent = this.nvl(results[i].fuser_agent, "N/A").substring(0, 10)

                this.items.push({
                    date: dateString,
                    time: timeString,
                    ip: results[i].fip,

                    request: frequest,
                    referrer: freferrer,
                    useragent: fuser_agent,
                    status: results[i].fstatus,
                    byte: results[i].fbyte.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    // 숫자 3자리(천단위) 마다 "," 표시
                    timetaken: results[i].ftime_taken.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
                    logline: results[i].log_line,
                    viewname: 'detail'

                });
            }
        },

        getStatisticsLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

            // 1 : 0~9, 2 : 10~19,
            //console.log("offset :" + offset);

            // this.getDetailCondition();
            setDetailCondition();

            let filters = getDetailSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID, this.excludeSearch, this.projectServers, this.detailconditionValue, this.detailsearchValue, '', '', '', '')

            var urlstring =
                //serverUrl + "/logdetail/?limit=" + this.pagingInfo.rowsPerPage + "&offset=" + offset + filters;
                serverUrl + "/logdetail_dynamic/?limit=" + this.pagingInfo.rowsPerPage + "&offset=" + offset + filters;

            // TODO : Set axiosConfig to set headers
            //let axiosConfig = {
            //  headers: {
            //    'Authorization': 'Token '+ this.token // For Django
            //  }
            //};

            // TODO : Set GET parametes, ex) /logdetail/?limit=10&offset=20

            // Start Loading Spinner
            this.isActive = true

            axios
                .get(urlstring)
                .then(res => {
                    this.pagingInfo.totalItems = res.data.count;

                    //console.log(res.data.results)

                    this.setItemList(res.data.results);
                    // Stop Loading Spinner
                    this.isActive = false
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false
                });
        },

        getStatisticsLogDetailsDiff() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

            // PopupDifferences status 관련항목 조회조건 설정 (statusYN)
            // statisticsKind = 35. Defference : status Requests Top N at TPS peak
            // statisticsKind = 36. Defference : status Visitors Top N at TPS peak
            if( this.$store.state.detailcondition == 35 || this.$store.state.detailcondition == 36) this.statusYN = "Y"

            // this.getDetailCondition();
            setDetailCondition();

            let dateValueTmp = this.$store.state.popupDate.substring(0,8);
            let timeValueTmp =  this.$store.state.popupDate.substring(8,12);
            let filters = getDetailSearchFilter(dateValueTmp, dateValueTmp, timeValueTmp+'00', timeValueTmp+'59', this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID, this.excludeSearch, this.projectServers, this.detailconditionValue, this.detailsearchValue, '', '', '', this.statusYN)

            var urlstring =
                serverUrl + "/logdetail_dynamic/?limit=" + this.pagingInfo.rowsPerPage + "&offset=" + offset + filters;

            // Start Loading Spinner
            this.isActive = true

            axios
                .get(urlstring)
                .then(res => {
                    this.pagingInfo.totalItems = res.data.count;
                    //console.log(res.data.results)

                    this.setItemList(res.data.results);
                    // Stop Loading Spinner
                    this.isActive = false
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false
                });
        },

        getFindingLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);
            let ttFromValueThreshold = ''
            let ttToValueThreshold = ''
            let byteFromValueThreshold = ''
            let byteToValueThreshold = ''
            let staticValue = ''
            let filters = ''

            // this.getFindingDetailCondition();
            setFindingDetailCondition();

            if (this.finding.metric_static == 'Y'){
                staticValue = 'T'
            }
            // timetaken 값은 microseconds -> ms 단위로 처리한다.(/1000)
            // logdetail_dynamic ftime_taken, fbyte between 조회
            if (this.finding.metric_kind == 'threshold'){
                if (this.finding.metric_unit == 'micros'){
                    ttFromValueThreshold = this.finding.metric_value1 / 1000
                    ttToValueThreshold = 24*60*60*1000 
                } else if (this.finding.metric_unit == 'millis'){
                    ttFromValueThreshold = this.finding.metric_value1
                    ttToValueThreshold = 24*60*60*1000
                } else if (this.finding.metric_unit == 'byte'){
                    byteFromValueThreshold = this.finding.metric_value1
                    byteToValueThreshold = 1024*1024*1024*1024
                } 
            } else if (this.finding.metric_kind == 'scope'){
                if (this.finding.metric_unit == 'micros'){
                    ttFromValueThreshold = this.finding.metric_value1 / 1000
                    ttToValueThreshold =  this.finding.metric_value2 / 1000
                } else if (this.finding.metric_unit == 'millis'){
                    ttFromValueThreshold = this.finding.metric_value1
                    ttToValueThreshold = this.finding.metric_value2
                } else if (this.finding.metric_unit == 'byte'){
                    byteFromValueThreshold = this.finding.metric_value1
                    byteToValueThreshold = this.finding.metric_value2
                } 
            }

            filters = getDetailSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, ttFromValueThreshold, ttToValueThreshold, this.projectID, this.excludeSearch, this.projectServers, this.detailconditionValue, this.detailsearchValue, byteFromValueThreshold, byteToValueThreshold, staticValue, '')

            var urlstring =
                serverUrl + "/logdetail_dynamic/?limit=" + this.pagingInfo.rowsPerPage + "&offset=" + offset + filters;

            // TODO : Set axiosConfig to set headers
            //let axiosConfig = {
            //  headers: {
            //    'Authorization': 'Token '+ this.token // For Django
            //  }
            //};

            // TODO : Set GET parametes, ex) /logdetail/?limit=10&offset=20

            // Start Loading Spinner
            this.isActive = true

            axios
                .get(urlstring)
                .then(res => {

                    this.pagingInfo.totalItems = res.data.count;
                    this.setItemList(res.data.results);
                    // Stop Loading Spinner
                    this.isActive = false
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false
                });
        },

        pageChange(page) {
            //console.log(page);
            this.pagingInfo.currentPage = page;
            if (this.$store.state.popupKind == 'Statistics') {
                this.getStatisticsLogDetails();
            } else if (this.$store.state.popupKind == 'FindingsDetail') {
                this.getFindingLogDetails();
            } else if (this.$store.state.popupKind == 'Differences') {
                this.getStatisticsLogDetailsDiff();
            }
        },

        clickClose: function () {
            this.$emit('popupClose');
            //EventBus.$emit("cancel");
        },

        getFilter() {

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
                project_id: this.projectID,

                detailconditionValue: this.detailconditionValue,
                detailsearchValue: this.detailsearchValue,

                projectServers: this.projectServers,
            }

            return filter
        },

        // 시계열 분석용 Line Chart
        async multilineChartData() {

            this.isActiveLineChart = true

            try {

                // this.getDetailCondition();
                setDetailCondition();
                this.$store.dispatch("setDetailSearchKeyword", decodeURIComponent(this.$store.state.detailsearchKeyword));

                let filter = this.getFilter();        

                let ttFromValueThreshold = ''
                let ttToValueThreshold = ''
                let byteFromValueThreshold = ''
                let byteToValueThreshold = ''
                let staticValue = ''

                // this.getFindingDetailCondition();
                setFindingDetailCondition(); 

                if (this.finding.metric_static == 'Y'){
                    staticValue = 'T'
                }

                // timetaken 값은 microseconds -> ms 단위로 처리한다.(/1000)
                // logdetail_dynamic ftime_taken, fbyte between 조회
                if (this.finding.metric_kind == 'threshold'){
                    if (this.finding.metric_unit == 'micros'){
                        ttFromValueThreshold = this.finding.metric_value1 / 1000
                        ttToValueThreshold = 24*60*60*1000 
                    } else if (this.finding.metric_unit == 'millis'){
                        ttFromValueThreshold = this.finding.metric_value1
                        ttToValueThreshold = 24*60*60*1000
                    } else if (this.finding.metric_unit == 'byte'){
                        byteFromValueThreshold = this.finding.metric_value1
                        byteToValueThreshold = 1024*1024*1024*1024
                    } 
                } else if (this.finding.metric_kind == 'scope'){
                    if (this.finding.metric_unit == 'micros'){
                        ttFromValueThreshold = this.finding.metric_value1 / 1000
                        ttToValueThreshold =  this.finding.metric_value2 / 1000
                    } else if (this.finding.metric_unit == 'millis'){
                        ttFromValueThreshold = this.finding.metric_value1
                        ttToValueThreshold = this.finding.metric_value2
                    } else if (this.finding.metric_unit == 'byte'){
                        byteFromValueThreshold = this.finding.metric_value1
                        byteToValueThreshold = this.finding.metric_value2
                    } 
                }

                filter['ttFromValue'] = ttFromValueThreshold;
                filter['ttToValue'] = ttToValueThreshold;
                filter['byteFromValue'] = byteFromValueThreshold;
                filter['byteToValue'] = byteToValueThreshold;
                filter['staticValue'] = staticValue;
                    
                let res = await getLineChartData(3, this.timeCondition, this.projectID, filter)

                this.mlChartData = getMultiLineChartTemplate(res.x, res.y, 'Request (count)', res.yt, "Time-Taken")
                this.mlOptions = getMultiLineChartOptions('Request (count) / Time-Taken', this.dateFromValue+this.timeFromValue, this.dateToValue+this.timeToValue); 
                this.$refs.mlChart.renderChart(this.mlChartData, this.mlOptions);
                

            } catch (err) {

                console.error(err); // TypeError: failed to fatch

            } finally {
                this.isActiveLineChart = false
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
            
        }
    },

    created() {
        if (this.$store.state.popupKind == 'Statistics') {
            this.getStatisticsLogDetails();
            this.multilineChartData();
            this.loaded = true
        } else if (this.$store.state.popupKind == 'FindingsDetail') {
            this.getFindingLogDetails();
            this.multilineChartData();
            this.loaded = true
        } else if (this.$store.state.popupKind == 'Differences') {
                this.getStatisticsLogDetailsDiff();
        }
    },

    watch: {
        isSearch() {
            if (this.$store.state.popupKind == 'Statistics') {
                this.getStatisticsLogDetails();
                this.multilineChartData();
            } else if (this.$store.state.popupKind == 'FindingsDetail') {
                this.getFindingLogDetails();
            } else if (this.$store.state.popupKind == 'Differences') {
                this.getStatisticsLogDetailsDiff();
            }
        },
        timeCondition() {
            this.multilineChartData();
        }
    }
};
</script>

<style scoped>
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
    width: 100%;
    height: 100%;
    margin: 0px auto;
    padding: 20px 20px 20px 20px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
    max-height: 930px;
    overflow-y: auto;
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

</style>
