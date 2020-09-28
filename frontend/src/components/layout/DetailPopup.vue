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
    name: 'DetailPopup',
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
        popupState: ''
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
        isSearch: "getToggleSearch",

        dateFromValue: "getFromDate",
        dateToValue: "getToDate",
        timeFromValue: "getFromTime",
        timeToValue: "getToTime",

        conditionValue: "getCondition",
        searchValue: "getSearchKeyword",

        ttFromValue: "getFromTimeTaken",
        ttToValue: "getToTimeTaken",

        projectID: "getProjectID",

        detailconditionValue: "getDetailCondition",
        detailsearchValue: "getDetailSearchKeyword",
        threshold: "getThreshold",

    }),

    methods: {
        getDateTimeString(str) {
            return str >= 10 ? str : "0" + str;
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
                    "" +
                    this.getDateTimeString(results[i].fmonth) +
                    "" +
                    this.getDateTimeString(results[i].fday);
                timeString =
                    this.getDateTimeString(results[i].fhour) +
                    "" +
                    this.getDateTimeString(results[i].fminute) +
                    "" +
                    this.getDateTimeString(results[i].fsecond);

                let frequest = results[i].frequest.substring(0, 60)
                let referrer = this.nvl(results[i].referrer, "N/A").substring(0, 10)
                let fuser_agent = this.nvl(results[i].fuser_agent, "N/A").substring(0, 10)

                this.items.push({
                    date: dateString,
                    time: timeString,
                    ip: results[i].fip,

                    request: frequest,
                    referrer: referrer,
                    useragent: fuser_agent,
                    status: results[i].fstatus,
                    timetaken: results[i].ftime_taken,
                    isSelected: false,
                    logline: results[i].log_line,
                    viewname: 'detail'

                });
            }
        },

        getDetailCondition() {

            switch (this.$store.state.detailcondition) {
                case 1:
                    this.$store.state.popupHeader = "HTTP Status Codes (count)"
                    this.$store.state.detailcondition = "S"
                    break;
                case 2:
                    this.$store.state.popupHeader = "Requests URI (count)"
                    this.$store.state.detailcondition = "R"
                    break;
                case 3:
                    this.$store.state.popupHeader = "404 Requests URI (count)"
                    this.$store.state.detailcondition = "R"
                    break;
                case 4:
                    this.$store.state.popupHeader = "Requests Time-taken (s/㎲)"
                    this.$store.state.detailcondition = "R"
                    break;
                case 5:
                    this.$store.state.popupHeader = "Visitors (count)"
                    this.$store.state.detailcondition = "I"
                    break;
                case 6:
                    this.$store.state.popupHeader = "Referers (count)"
                    this.$store.state.detailcondition = "E"
                    break;
                case 7:
                    this.$store.state.popupHeader = "User Agent (count)"
                    this.$store.state.detailcondition = "U"
                    break;
                case 8:
                    this.$store.state.popupHeader = "Requests URI (Total Bytes)"
                    this.$store.state.detailcondition = "R"
                    break;
                case 9:
                    this.$store.state.popupHeader = "Static files (count)"
                    this.$store.state.detailcondition = "F"
                    break;
                case 10:
                    this.$store.state.popupHeader = "Requests URI (Average Bytes)"
                    this.$store.state.detailcondition = "R"
                    break;
                case 11:
                    this.$store.state.popupHeader = "Requests Average Time-taken (s/㎲)"
                    this.$store.state.detailcondition = "R"
                    break;
                default:
            }
        },

        getStatisticsLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

            // 1 : 0~9, 2 : 10~19,
            //console.log("offset :" + offset);

            this.getDetailCondition();

            //let filters = getSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID)
            let filters = getDetailSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID, this.detailconditionValue, this.detailsearchValue)
            console.log("DetailPopUp detailconditionValue : " + this.detailconditionValue)
            console.log("DetailPopUp detailsearchValue : " + this.detailsearchValue)
            console.log("DetailPopUp filters : " + filters)

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

                    console.log(res.data.count); // 전체건수
                    console.log(res);
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

        getLongTransactionLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

            // 1 : 0~9, 2 : 10~19,
            //console.log("offset :" + offset);

            //let filters = getSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID)  

            var ttFromValueThreshold = this.threshold * 1000000
            var ttToValueThreshold = 99999 * 1000000
            //let filters = getDetailSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID, this.detailconditionValue, this.detailsearchValue)
            let filters = getDetailSearchFilter('', '', '', '', '', '', ttFromValueThreshold, ttToValueThreshold, this.projectID, '', '')
            //let filters = getDetailSearchFilter(ttFromValueThreshold, ttToValueThreshold, this.projectID)
            console.log("LongTransactionDetailPopUp ttFromValueThreshold : " + ttFromValueThreshold)
            console.log("LongTransactionDetailPopUp ttToValueThreshold : " + ttToValueThreshold)
            console.log("LongTransactionDetailPopUp filters : " + filters)

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

                    console.log(res.data.count); // 전체건수
                    console.log(res);
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
            console.log(page);
            this.pagingInfo.currentPage = page;
            if (this.$store.state.popupKind == 'Statistics') {
                this.getStatisticsLogDetails();
            } else if (this.$store.state.popupKind == 'LongTransaction') {
                this.getLongTransactionLogDetails();
            }
        },

        clickClose: function () {
            console.log("click Popup Close/Cancel Button");
            this.$emit('popupClose');
            //EventBus.$emit("cancel");
        },
    },

    created() {
        if (this.$store.state.popupKind == 'Statistics') {
            this.getStatisticsLogDetails();
        } else if (this.$store.state.popupKind == 'LongTransaction') {
            this.getLongTransactionLogDetails();
        }
    },

    watch: {
        isSearch() {
            if (this.$store.state.popupKind == 'Statistics') {
                this.getStatisticsLogDetails();
            } else if (this.$store.state.popupKind == 'LongTransaction') {
                this.getLongTransactionLogDetails();
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
