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
import {
    mapGetters
} from 'vuex';
import {
    getSearchFilter,
    getDetailSearchFilter,
    serverUrl
} from "@/common"

export default {
    name: 'DetailPopup2',
    components: {
        // export Loading Spinner components
        VueElementLoading,
    },
    props: {
        item: {
            type: Object,
            default: function () {

                return {
                    result: '',
                    result_count: '',
                }
            }
        },
        popupState: '',
        finding: {
            type: Object,
            default: function () {
                return {
                    description: '',
                    result: '',
                    metric_kind: '',
                    metric_filter: '',
                    metric_unit: '',
                    metric_value1: '',
                    metric_value2: '',
                }
            }
        }
    },
    data: function () {
        return {
            // Loading Spinner
            isActive: false,

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
                    width: 15
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
                    label: 'TimeTaken',
                    key: "timetaken",
                    sortable: false,
                    filtable: false,
                    alignRight: false,
                    width: 10
                },
            ],

            // Grid Rows
            items: []
        };
    },

    computed: mapGetters({
        //isSearch: "getToggleSearch",

        dateFromValue: "getFromDate2",
        dateToValue: "getToDate2",
        timeFromValue: "getFromTime2",
        timeToValue: "getToTime2",

        conditionValue: "getCondition2",
        searchValue: "getSearchKeyword2",

        ttFromValue: "getFromTimeTaken2",
        ttToValue: "getToTimeTaken2",

        projectID: "getProjectID",

        detailconditionValue: "getDetailCondition2",
        detailsearchValue: "getDetailSearchKeyword2",
        threshold: "getThreshold",

    }),

    methods: {
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
                let freferrer = this.nvl(results[i].freferer, "N/A").substring(0, 10)
                let fuser_agent = this.nvl(results[i].fuser_agent, "N/A").substring(0, 10)

                this.items.push({
                    date: dateString,
                    time: timeString,
                    ip: results[i].fip,

                    request: frequest,
                    referrer: freferrer,
                    useragent: fuser_agent,
                    status: results[i].fstatus,
                    // 숫자 3자리(천단위) 마다 "," 표시
                    timetaken: results[i].ftime_taken.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),                    
                    isSelected: false,
                    logline: results[i].log_line,
                    viewname: 'detail'

                });
            }
        },

        getDetailCondition() {

            switch (this.$store.state.detailcondition2) {
                case 1:
                    this.$store.state.popupHeader2 = "HTTP Status Codes (count)"
                    this.$store.state.detailcondition2 = "S"
                    break;
                case 2:
                    this.$store.state.popupHeader2 = "Requests URI (count)"
                    this.$store.state.detailcondition2 = "R"
                    break;
                case 3:
                    this.$store.state.popupHeader2 = "404 Requests URI (count)"
                    this.$store.state.detailcondition2 = "NFR"
                    break;
                case 4:
                    this.$store.state.popupHeader2 = "Requests Time-taken (s/㎲)"
                    this.$store.state.detailcondition2 = "R"
                    break;
                case 5:
                    this.$store.state.popupHeader2 = "Visitors (count)"
                    this.$store.state.detailcondition2 = "I"
                    break;
                case 6:
                    this.$store.state.popupHeader2 = "Referers (count)"
                    this.$store.state.detailcondition2 = "E"
                    break;
                case 7:
                    this.$store.state.popupHeader2 = "User Agent (count)"
                    this.$store.state.detailcondition2 = "U"
                    break;
                case 8:
                    this.$store.state.popupHeader2 = "Requests URI (Total Bytes)"
                    this.$store.state.detailcondition2 = "R"
                    break;
                case 9:
                    this.$store.state.popupHeader2 = "Static files (count)"
                    this.$store.state.detailcondition2 = "F"
                    break;
                case 10:
                    this.$store.state.popupHeader2 = "Requests URI (Average Bytes)"
                    this.$store.state.detailcondition2 = "R"
                    break;
                case 11:
                    this.$store.state.popupHeader2 = "Requests Average Time-taken (s/㎲)"
                    this.$store.state.detailcondition2 = "R"
                    break;
                case 12:
                    this.$store.state.popupHeader2 = "Static file Names (count)"
                    this.$store.state.detailcondition2 = "R"
                    break;
                case 13:
                    this.$store.state.popupHeader2 = "Upstream Info (count, K8S Ingress)";
                    this.$store.state.detailcondition2 = "V1"
                    break;
                case 14:
                    this.$store.state.popupHeader2 = "Domains (count, K8S Ingress)";    
                    this.$store.state.detailcondition2 = "V2"        
                    break;
                default:
            }
        },

        getStatisticsLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

            // 1 : 0~9, 2 : 10~19,
            //console.log("offset :" + offset);

            this.getDetailCondition();

            let filters = getDetailSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID, this.detailconditionValue, this.detailsearchValue, '', '', '')

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

                    console.log(res.data.results)

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

        getFindingDetailCondition() {

            if (this.$store.state.detailcondition2 == 'fstatus') {
                //this.$store.state.popupHeader = "HTTP Status Codes (count)"
                this.$store.state.detailcondition2 = "S"
            } else if (this.$store.state.detailcondition2 == 'frequest') {    
                // this.$store.state.popupHeader = "Requests URI (count)"
                this.$store.state.detailcondition2 = "R"
            } else if (this.$store.state.detailcondition2 == 'fip') {
                // this.$store.state.popupHeader = "Visitors (count)"
                this.$store.state.detailcondition2 = "I"
            } else if (this.$store.state.detailcondition2 == 'freferer') {
                // this.$store.state.popupHeader = "Referers (count)"
                this.$store.state.detailcondition2 = "E"
            } else if (this.$store.state.detailcondition2 == 'fuser_agent') {
                // this.$store.state.popupHeader = "User Agent (count)"
                this.$store.state.detailcondition2 = "U"
            } else if (this.$store.state.detailcondition2 == 'fextension') {
                // this.$store.state.popupHeader = "Static files (count)"
                this.$store.state.detailcondition2 = "F"
            } else if (this.$store.state.detailcondition2 == 'freserve1') {
                // this.$store.state.popupHeader = "Upstream Info (count, K8S Ingress)";
                this.$store.state.detailcondition2 = "V1"
            } else if (this.$store.state.detailcondition2 == 'freserve2') {
                // this.$store.state.popupHeader = "Domains (count, K8S Ingress)";    
                this.$store.state.detailcondition2 = "V2"        
            }
        },

        getFindingLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);
            let ttFromValueThreshold = ''
            let ttToValueThreshold = ''
            let byteFromValueThreshold = ''
            let byteToValueThreshold = ''
            let staticValue = ''
            let filters = ''

            this.getFindingDetailCondition();

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

            filters = getDetailSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, ttFromValueThreshold, ttToValueThreshold, this.projectID, this.detailconditionValue, this.detailsearchValue, byteFromValueThreshold, byteToValueThreshold, staticValue)

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

                    //console.log(res.data.count); // 전체건수
                    //console.log(res);
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
            } else if (this.$store.state.popupKind == 'FindingsDetail2') {
                this.getFindingLogDetails();
            }
        },

        clickClose: function () {
            //("click Popup Close/Cancel Button");
            this.$emit('popupClose');
            //EventBus.$emit("cancel");
        },
    },

    created() {
        if (this.$store.state.popupKind == 'Statistics') {
            this.getStatisticsLogDetails();
        } else if (this.$store.state.popupKind == 'FindingsDetail2') {
            this.getFindingLogDetails();
        }
    },

    watch: {
        isSearch() {
            if (this.$store.state.popupKind == 'Statistics') {
                this.getStatisticsLogDetails();
            } else if (this.$store.state.popupKind == 'FindingsDetail2') {
                this.getFindingLogDetails();
            }
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
    width: 500px;
    height: 100%;
    margin: 0px auto;
    padding: 20px 20px 20px 20px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
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
