<template>
<ui-container-box :columns="22" vertical align-center class="page-container">

    <ui-container-box :columns="20" horizontal align-center class="page-title">
        <span class="page-title__label">Analysis</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <info></info>
        <notice></notice>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
        <search></search>
    </ui-container-box>

    <!-- Statisctic -->
    <ui-container-box :columns="20" vertical align-left class="page-title">
        <span class="page-title__label">Statistics - Top {{ valueN == 0 ? "" : valueN }}</span>
        <ui-form-row>
            <ui-form-item :columns="12" label="Select N" align-left required-left>
                <!-- TODO: 이벤트 처리, 숫자 바뀔 때 -->
                <lego-dropdown :items="listN" v-model="valueN" width="100px" />
            </ui-form-item>
        </ui-form-row>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">

        <ui-container-box :columns="10" vertical class="mt20">
            <statistics :statisticsRow="valueN" :statisticsKind="2"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="4"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="1"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="8"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="9"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="6"></statistics>
        </ui-container-box>

        <ui-container-box :columns="10" vertical class="mt20">
            <statistics :statisticsRow="valueN" :statisticsKind="5"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="11"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="3"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="10"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="9"></statistics>
            <statistics :statisticsRow="valueN" :statisticsKind="7"></statistics>
        </ui-container-box>

    </ui-container-box>

    <!-- Charts 영역 -->
    <ui-container-box :columns="20" vertical align-left class="page-title">
        <span class="page-title__label">Charts</span>

        <ui-form-row>
            <ui-form-item :columns="12" label="Timeline" align-left required-left>
                <lego-radio v-model="timeCondition" value="1">HH</lego-radio>
                <lego-radio v-model="timeCondition" value="2">HHMM</lego-radio>
                <lego-radio v-model="timeCondition" value="3">HHMMSS</lego-radio>
            </ui-form-item>
        </ui-form-row>

        <ui-form-row>
            <ui-form-item :columns="12" label="Charts" align-left required-left>

                <lego-button @click="lineChartData" main small>Line</lego-button>

                <lego-button @click="multilineChartData" main small>MultiLine</lego-button>
                <lego-button @click="barChartData" main small>Bar</lego-button>
                <lego-button @click="stackedbarChartData" main small>StackedBar</lego-button>
                <lego-button @click="pieChartData(5)" main small>Pie(5)</lego-button>
                <lego-button @click="pieChartData(1)" main small>Pie</lego-button>
                <lego-button @click="pieChartData(9)" main small>Pie(9)</lego-button>
                <lego-button @click="allChart()" small>ALL</lego-button>
            </ui-form-item>
        </ui-form-row>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">

        <ui-container-box :columns="10" vertical class="mt20">

            <div class="vld-parent">
                <vue-element-loading :active="isActiveLine" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />

                <lego-button @click="resetZoom(1)" small>resetZoom</lego-button>
                <chart-line ref='lChart' :chart-data="lChartData" :options="lOptions"></chart-line>
            </div>

            <div class="vld-parent">
                <vue-element-loading :active="isActivePie" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                <chart-pie :chart-data="pChartData" :options="pOptions"></chart-pie>
            </div>

            <!--div class="vld-parent">

                <vue-element-loading :active="isActiveBar" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />

                Dummy for Alignment
                <lego-button hidden small>resetZoom</lego-button>
                <chart-bar ref='bChart' :chart-data="bChartData" :options="bOptions"></chart-bar>
            </div-->

            <div class="vld-parent">
                <vue-element-loading :active="isActivePie5" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                <chart-pie :chart-data="pChartDataVisitorTop5" :options="pOptions"></chart-pie>
            </div>

        </ui-container-box>

        <ui-container-box :columns="10" vertical class="mt20">
            <div class="vld-parent">
                <lego-button @click="resetZoom(2)" small>resetZoom</lego-button>
                <vue-element-loading :active="isActiveMultiLine" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                <chart-line ref='mlChart' :chart-data="mlChartData" :options="mlOptions"></chart-line>
            </div>

            <div class="vld-parent">
                <vue-element-loading :active="isActiveStackedBar" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />

                <lego-button @click="resetZoom(3)" small>resetZoom</lego-button>
                <chart-stacked-bar ref="sbChart" :chart-data="sbChartData" :options="sbOptions"></chart-stacked-bar>
            </div>

            <div class="vld-parent">
                <vue-element-loading :active="isActivePieExtension" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
                <chart-pie :chart-data="pChartDataExtension" :options="pOptions"></chart-pie>
            </div>

        </ui-container-box>

    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-tab-area">
        <img src="@/assets/ico_footer.png" alt="Samsung SDS" />
    </ui-container-box>

</ui-container-box>
</template>

<script>
import ChartLine from "@/components/layout/ChartLine";
import ChartBar from "@/components/layout/ChartBar";
import ChartPie from "@/components/layout/ChartPie";
import ChartStackedBar from "@/components/layout/ChartStackedBar";

import GridTable from "@/components/layout/GridTable";
import Info from "@/components/layout/Info";
import Init from "@/components/layout/Init";
import Notice from "@/components/layout/Notice";
import Search from "@/components/layout/Search";
import Statistics from "@/components/layout/Statistics";

import {
    mapGetters
} from "vuex";

import {
    getPieChartTemplate,
    getBarChartTemplate,
    getStackedBarChartTemplate,
    getLineChartTemplate,
    getPieChartOptions,
    getBarChartOptions,
    getStackedBarChartOptions,
    getLineChartOptions,
    getMultiLineChartTemplate,
    getMultiLineChartOptions,
    setCommonStatisticInfo,
    getChartDataFromStatistics,
    getLineChartData,
    getSearchFilter
} from "@/common"

import VueElementLoading from 'vue-element-loading'

export default {
    name: "Analysis",

    data() {
        return {
            // For Chart
            resetZoomV: "1",
            timeCondition: "1", // "Hour(시) 기준"

            // For Statistics
            statisticsRow: "1", // Top or Top5 (Row 수)
            statisticsKind: "1", // 전체 처리량 (통계 종류)  

            // for chart reactivess Test
            lChartData: null,
            lOptions: getLineChartOptions('Waiting..'),

            mlChartData: null,
            mlOptions: getMultiLineChartOptions('Waiting..'),

            bChartData: null,
            bOptions: getBarChartOptions('Waiting..'),

            sbChartData: null,
            sbOptions: getStackedBarChartOptions('Waiting..'),

            pChartData: null,
            pChartDataVisitorTop5: null,
            pChartDataExtension: null,
            pOptions: getPieChartOptions('Waiting..'),

            logfile_id: '',

            // For Loading Spinner
            isActiveLine: false,
            isActiveMultiLine: false,
            isActiveBar: false,
            isActiveStackedBar: false,
            isActivePie: false,
            isActivePie5: false,
            isActivePieExtension: false,

            // For Statistics N
            valueN: 5,
        }
    },

    // 컴포넌트 등록
    components: {
        Info,
        Notice,
        Search,
        Statistics,
        ChartLine,
        ChartBar,
        ChartPie,
        ChartStackedBar,
        VueElementLoading,
    },

    created() {
        this.logfile_id = this.$store.state.logFileID
        this.project_id = this.$store.state.projectID
    },

    mounted() {

    },

    computed: {

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

        ...mapGetters({

            dateFromValue: "getFromDate",
            dateToValue: "getToDate",
            timeFromValue: "getFromTime",
            timeToValue: "getToTime",

            conditionValue: "getCondition",
            searchValue: "getSearchKeyword",

            ttFromValue: "getFromTimeTaken",
            ttToValue: "getToTimeTaken",

            project_id: "getProjectID",

        })
    },

    methods: {

        allChart() {

            this.lineChartData();
            this.multilineChartData();
            //this.barChartData();
            this.stackedbarChartData();
            this.pieChartData(5);
            this.pieChartData(1);
            this.pieChartData(9)

        },

        resetZoom(chart) {

            var comp;

            if (chart == 1) {
                comp = this.$refs.lChart;
            } else if (chart == 2) {
                comp = this.$refs.mlChart;
            } else if (chart == 3) {
                comp = this.$refs.sbChart;
            }

            comp._data._chart.resetZoom()

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

                project_id: this.project_id,
            }

            return filter
        },

        async pieChartData(type) {

            // Start Loading Spinner
            if (type == 1) {
                this.isActivePie = true
            } else if (type == 5) {
                this.isActivePie5 = true
            } else if (type == 9) {
                this.isActivePieExtension = true
            }

            let filter = this.getFilter()

            try {
                let res = await getChartDataFromStatistics(type, this.project_id, filter, this.valueN)

                if (type == 1) {
                    this.pChartData = getPieChartTemplate(res.x, res.y)
                    this.pOptions = getPieChartOptions("HTTP Status Codes");

                    //Stop Loading Spinner
                    this.isActivePie = false
                } else if (type == 5) {
                    this.pChartDataVisitorTop5 = getPieChartTemplate(res.x, res.y)
                    this.pOptions = getPieChartOptions("Visitor IP Top5");

                    //Stop Loading Spinner
                    this.isActivePie5 = false
                } else if (type == 9) {
                    this.pChartDataExtension = getPieChartTemplate(res.x, res.y)
                    this.pOptions = getPieChartOptions("Static File Types");

                    //Stop Loading Spinner
                    this.isActivePieExtension = false
                }
            } catch (err) {
                console.log(err); // TypeError: failed to fatch

                //Stop Loading Spinner
                if (type == 1) {
                    this.isActivePie = false;
                } else if (type == 5) {
                    this.isActivePie5 = false;
                } else if (type == 9) {
                    this.isActivePieExtension = false;
                }
            }

        },

        async barChartData() {
            // Start Loading Spinner
            this.isActiveBar = true

            let filter = this.getFilter()

            try {
                let res = await getChartDataFromStatistics(1, this.project_id, filter, this.valueN)
                this.bChartData = getBarChartTemplate(res.x, res.y, res.label)
                this.bOptions = getBarChartOptions(res.label)
            } catch (err) {
                console.log(err); // TypeError: failed to fatch
            } finally {
                //Stop Loading Spinner
                this.isActiveBar = false
            }

        },

        async stackedbarChartData() {
            // Start Loading Spinner
            this.isActiveStackedBar = true

            let filter = this.getFilter()

            try {
                let res = await getLineChartData(2, this.timeCondition, this.project_id, filter)
                this.sbChartData = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
                this.sbOptions = getStackedBarChartOptions('Http Status Code');
            } catch (err) {
                console.log(err); // TypeError: failed to fatch
            } finally {
                //Stop Loading Spinner
                this.isActiveStackedBar = false
            }

        },

        // 시계열 분석용 Line Chart
        async lineChartData() {
            // Start Loading Spinner
            this.isActiveLine = true

            let filter = this.getFilter()

            try {
                let res = await getLineChartData(1, this.timeCondition, this.project_id, filter)
                this.lChartData = getLineChartTemplate(res.x, res.y, "TPS")

                this.lOptions = getLineChartOptions('Transaction Per Second');
            } catch (err) {
                console.log(err); // TypeError: failed to fatch
            } finally {
                //Stop Loading Spinner
                this.isActiveLine = false
            }

        },

        // 시계열 분석용 Line Chart
        async multilineChartData() {
            // Start Loading Spinner
            this.isActiveMultiLine = true

            let filter = this.getFilter()

            try {
                let res = await getLineChartData(3, this.timeCondition, this.project_id, filter);
                this.mlChartData = getMultiLineChartTemplate(res.x, res.y, 'Request (count)', res.yt, 'Time-Taken');
                this.mlOptions = getMultiLineChartOptions('Request (count) / Time-Taken');
            } catch (err) {
                console.log(err); // TypeError: failed to fatch
            } finally {
                //Stop Loading Spinner
                this.isActiveMultiLine = false
            }
        },

    },

    watch: {
        valueN() {
            this.$store.dispatch("setToggleSearch");
        }
    }
};
</script>

<style scoped>
.page-container {
    margin: 48px 80px 32px;
    padding: 80px 80px;
    background-color: white;
}
</style>
