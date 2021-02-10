<template>
<div id="gridtable">
    <!-- This page is GridTable - {{ isSearch }} -->
    <ui-container-box :columns="20" vertical class="mb50">
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
        <ui-container-box :columns="20" vertical>
            <ui-table header-divider no-action :columns="columns" :items="items" class="mt20"></ui-table>
        </ui-container-box>

        <lego-pagination :pagination="pagingInfo" @move="pageChange" class="mt20" />
    </ui-container-box>
</div>
</template>

<script>
import axios from "axios";
import {
    mapGetters
} from "vuex";
import {
    getSearchFilter,
    serverUrl
} from "@/common"
import VueElementLoading from 'vue-element-loading'

export default {
    name: "GridTable",
    components: {
        // export Loading Spinner components
        VueElementLoading,
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
                    timetaken: results[i].ftime_taken,
                    isSelected: false,
                    logline: results[i].log_line,
                    viewname: 'detail'
                });
            }

            //console.log("results : "+ this.results)
        },

        getLogDetails() {

            let offset = this.pagingInfo.rowsPerPage * (this.pagingInfo.currentPage - 1);

            // 1 : 0~9, 2 : 10~19,
            //console.log("offset :" + offset);

            let filters = getSearchFilter(this.dateFromValue, this.dateToValue, this.timeFromValue, this.timeToValue, this.conditionValue, this.searchValue, this.ttFromValue, this.ttToValue, this.projectID)
            //console.log("filters : " + filters)

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

                    //console.log(res.data.count); // 전체건수
                    //console.log(res);
                    this.pagingInfo.totalItems = res.data.count;
                    this.setItemList(res.data.results);
                    // Stop Loading Spinner
                    this.isActive = false
                })
                .catch(err => {
                    // Stop Loading Spinner
                    this.isActive = false
                    console.error(err);
                });
        },

        pageChange(page) {
            //console.log(page);
            this.pagingInfo.currentPage = page;
            this.getLogDetails();
        }
    },

    created() {
        this.getLogDetails();

    },

    watch: {
        isSearch() {
            this.getLogDetails();
        }
    }
};
</script>

<style scoped>
</style>
