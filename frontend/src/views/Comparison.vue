<template>
<ui-container-box :columns="22" vertical align-center class="page-container">
    <ui-container-box :columns="20" horizontal align-center class="page-title">
        <span class="page-title__label">Comparison - Chart</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- <info></info> -->
        <notice></notice>
        <notice2></notice2>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <search-compare1></search-compare1>
        <search-compare2></search-compare2>
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-form-area_no_border_top">
        <component :is="currentView" v-on:popupClose="currentView=null" :kind="kind"></component>

        <span class="page-title__2label">Charts</span>

        <ui-form-row>
            <ui-form-item :columns="12" label="Timeline" align-left required-left>
                <lego-radio v-model="timeCondition" value="1">HH</lego-radio>
                <lego-radio v-model="timeCondition" value="2">HHMM</lego-radio>
                <lego-radio v-model="timeCondition" value="3">HHMMSS</lego-radio>
            </ui-form-item>
        </ui-form-row>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">

        <ui-form-item :columns="10" label="Select" align-left required-left>
            <ui-form-box>
                <ui-form-row>
                    <lego-button @click="lineChartData(1)" main small>TPS</lego-button>
                    <lego-button @click="multilineChartData(1)" main small>Req/Duration</lego-button>
                    <!-- <lego-button @click="barChartData(1)" main small>Bar</lego-button> -->
                    <lego-button @click="stackedbarChartData(1)" main small>Http Status(T)</lego-button>
                    <lego-button @click="pieChartData(1,1)" main small>Http Status(P)</lego-button>
                    <lego-button @click="pieChartData(1,5)" main small>Visitor IP(5)</lego-button>
                </ui-form-row>
                <br>
                <ui-form-row>
                    <lego-button @click="pieChartData(1,9)" main small>Static Files</lego-button>
                    <lego-button @click="search1Chart" small>ALL</lego-button>
                </ui-form-row>
            </ui-form-box>
        </ui-form-item>

        <ui-form-item :columns="10" label="Select" align-left required-left>
            <ui-form-box>
                <ui-form-row>
                    <lego-button @click="lineChartData(2)" main small>TPS</lego-button>
                    <lego-button @click="multilineChartData(2)" main small>Req/Duration</lego-button>
                    <!--<lego-button @click="barChartData(2)" main small>Bar</lego-button> -->
                    <lego-button @click="stackedbarChartData(2)" main small>Http Status(T)</lego-button>
                    <lego-button @click="pieChartData(2,1)" main small>Http Status(P)</lego-button>
                    <lego-button @click="pieChartData(2,5)" main small>Visitor IP(5)</lego-button>
                </ui-form-row>
                <br>
                <ui-form-row>
                    <lego-button @click="pieChartData(2,9)" main small>Static Files</lego-button>
                    <lego-button @click="search2Chart" small>ALL</lego-button>
                </ui-form-row>
            </ui-form-box>
        </ui-form-item>

    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- search1 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActiveLine1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <lego-button @click="resetZoom(1)" small>resetZoom</lego-button>
            <lego-button @click="setScaleY(1)" small>setScaleY</lego-button>
            <lego-button @click="PopupChartKind(1)" small main>ComparePopup</lego-button>
            <chart-line ref="lChart1" :chart-data="lChartData1" :options="lOptions1" :width="800" :height="400"></chart-line>
        </div>
        <!-- search2 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActiveLine2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <lego-button @click="resetZoom(4)" small>resetZoom</lego-button>
            <lego-button @click="setScaleY(4)" small>setScaleY</lego-button>
            <chart-line ref="lChart2" :chart-data="lChartData2" :options="lOptions2" :width="800" :height="400"></chart-line>
        </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- search1 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActiveMultiLine1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <lego-button @click="resetZoom(2)" small>resetZoom</lego-button>
            <lego-button @click="setScaleY(2, 0)" small>setScaleY_L</lego-button>
            <lego-button @click="setScaleY(2, 1)" small main>setScaleY_R</lego-button>
            <lego-button @click="PopupChartKind(4)" small main>ComparePopup</lego-button>
            <chart-line ref="mlChart1" :chart-data="mlChartData1" :options="mlOptions1" :width="800" :height="400"></chart-line>
        </div>
        <!-- search2 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActiveMultiLine2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <lego-button @click="resetZoom(5)" small>resetZoom</lego-button>
            <lego-button @click="setScaleY(5, 0)" small>setScaleY_L</lego-button>
            <lego-button @click="setScaleY(5, 1)" small main>setScaleY_R</lego-button>
            <chart-line ref="mlChart2" :chart-data="mlChartData2" :options="mlOptions2" :width="800" :height="400"></chart-line>
        </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- search1 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActiveStackedBar1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <lego-button @click="resetZoom(3)" small>resetZoom</lego-button>
            <lego-button @click="setScaleY(3)" small>setScaleY</lego-button>
            <lego-button @click="PopupChartKind(5)" small main>ComparePopup</lego-button>
            <chart-stacked-bar ref="sbChart1" :chart-data="sbChartData1" :options="sbOptions1" :width="800" :height="400"></chart-stacked-bar>
        </div>
        <!-- search2 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActiveStackedBar2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <lego-button @click="resetZoom(6)" small>resetZoom</lego-button>
            <lego-button @click="setScaleY(6)" small>setScaleY</lego-button>
            <chart-stacked-bar ref="sbChart2" :chart-data="sbChartData2" :options="sbOptions2" :width="800" :height="400"></chart-stacked-bar>
        </div>
    </ui-container-box>

    <!--
    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        !-- search1 --
        <div class="vld-parent">
            <vue-element-loading :active="isActiveBar1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-bar :chart-data="bChartData1" :options="bOptions" :width="800" :height="400"></chart-bar>
        </div>
        !-- search2 --
        <div class="vld-parent">
            <vue-element-loading :active="isActiveBar2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-bar :chart-data="bChartData2" :options="bOptions" :width="800" :height="400"></chart-bar>
        </div>
    </ui-container-box>
    -->

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- search1 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActivePie1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-pie :chart-data="pChartData1" :options="pOptions" :width="800" :height="400"></chart-pie>
        </div>
        <!-- search2 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActivePie2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-pie :chart-data="pChartData2" :options="pOptions" :width="800" :height="400"></chart-pie>
        </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- search1 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActivePie1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-pie :chart-data="pChartDataVisitorTop5_1" :options="pOptions" :width="800" :height="400"></chart-pie>
        </div>
        <!-- search2 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActivePie2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-pie :chart-data="pChartDataVisitorTop5_2" :options="pOptions" :width="800" :height="400"></chart-pie>
        </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <!-- search1 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActivePieExtension1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-pie :chart-data="pChartDataExtension1" :options="pOptions" :width="800" :height="400"></chart-pie>
        </div>
        <!-- search2 -->
        <div class="vld-parent">
            <vue-element-loading :active="isActivePieExtension2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <chart-pie :chart-data="pChartDataExtension2" :options="pOptions" :width="800" :height="400"></chart-pie>
        </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal>
        <ui-container-box :columns="10" vertical class="mt20">
            <font size="4">CI-TEC</font>
        </ui-container-box>
        <ui-container-box :columns="3" vertical class="mt20">
            <img src="@/assets/ico_footer.png" alt="Samsung SDS" />
        </ui-container-box>
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
import Notice2 from "@/components/layout/Notice2";
import Search from "@/components/layout/Search";
import SearchCompare1 from "@/components/layout/SearchCompare1";
import SearchCompare2 from "@/components/layout/SearchCompare2";
import Statistics from "@/components/layout/Statistics";
import PopupChart from '@/components/layout/PopupChart';

import {
    serverUrl
} from "@/common";

import {
    getPieChartTemplate,
    getBarChartTemplate,
    getStackedBarChartTemplate,
    getLineChartTemplate,
    getMultiLineChartTemplate,
    getMultiLineChartOptions,
    getPieChartOptions,
    getBarChartOptions,
    getStackedBarChartOptions,
    getLineChartOptions,
    getChartDataFromStatistics,
    getLineChartData
} from "@/common"

import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from "vuex";

import VueElementLoading from 'vue-element-loading'

export default {
    name: "Compare",

    // 컴포넌트 등록
    components: {
        Info,
        Notice,
        Notice2,
        Search,
        SearchCompare1,
        SearchCompare2,
        Statistics,
        ChartLine,
        ChartBar,
        ChartPie,
        ChartStackedBar,
        VueElementLoading,
        PopupChart
    },
    data() {
        return {
            timeCondition: "1",

            // for chart reactivess Test
            lChartData1: null,
            lChartData2: null,
            lOptions1: getLineChartOptions('- No Data -'),
            lOptions2: getLineChartOptions('- No Data -'),

            mlChartData1: null,
            mlChartData2: null,
            mlOptions1: getMultiLineChartOptions('- No Data -'),
            mlOptions2: getMultiLineChartOptions('- No Data -'),            

            sbChartData1: null,
            sbChartData2: null,
            sbOptions1: getStackedBarChartOptions('- No Data -'),
            sbOptions2: getStackedBarChartOptions('- No Data -'),

            bChartData1: null,
            bChartData2: null,
            bOptions: getBarChartOptions('- No Data -'),

            pChartData1: null,
            pChartDataVisitorTop5_1: null,
            pChartDataExtension1: null,
            pChartData2: null,
            pChartDataVisitorTop5_2: null,
            pChartDataExtension2: null,
            pOptions: getPieChartOptions('- No Data -'),

            logfile_id: '',
            project_id: '',

            // For Loading Spinner
            isActiveLine1: false,
            isActiveMultiLine1: false,
            isActiveBar1: false,
            isActiveStackedBar1: false,
            isActivePie1: false,
            isActivePie5_1: false,
            isActivePieExtension1: false,

            isActiveLine2: false,
            isActiveMultiLine2: false,
            isActiveBar2: false,
            isActiveStackedBar2: false,
            isActivePie2: false,
            isActivePie5_2: false,
            isActivePieExtension2: false,

            currentView: null,
            kind: '',
        }

    },

    created() {
        // console.log("serverUrl : ", serverUrl);

        // TODO: Check! mapGetter로 가능?
        this.logfile_id = this.$store.state.logFileID
        this.project_id = this.$store.state.projectID

        this.search1Chart();
        this.search2Chart();
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

            x_min_date: "getGlobalFromDate",            
            x_min_time: "getGlobalFromTime",
            x_max_date: "getGlobalToDate",
            x_max_time: "getGlobalToTime",

            // global scale Y
            global_Y_tps: "getGlobalYTps",
            global_Y_request: "getGlobalYRequest",            
            global_Y_duration: "getGlobalYDuration",
            global_Y_request_sbar: "getGlobalYRequestSBar",

            // global scale Y2
            global_Y_tps: "getGlobalYTps2",
            global_Y_request: "getGlobalYRequest2",            
            global_Y_duration: "getGlobalYDuration2",
            global_Y_request_sbar: "getGlobalYRequestSBar2",

            projectServers: "getProjectServers",
            projectServers2: "getProjectServers2",
        }),
    },
    methods: {

        PopupChartKind(kind){
            this.kind = kind
            this.currentView = 'PopupChart';
        },

        async setScaleY(chart, direction) { // direction 0 : left, 1 : right

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
                comp = this.$refs.lChart1;
            } else if (chart == 2) {
                comp = this.$refs.mlChart1;
            } else if (chart == 3) {
                comp = this.$refs.sbChart1;
            } else if (chart == 4) {
                comp = this.$refs.lChart2;
            } else if (chart == 5) {
                comp = this.$refs.mlChart2;
            } else if (chart == 6) {
                comp = this.$refs.sbChart2;
            }
            
            comp.options.scales.yAxes[direction].ticks = {
                suggestedMin: 0,
                suggestedMax: scale_y
            }

            if (chart == 1) {
                comp.renderChart(this.lChartData1, this.lOptions1);
            } else if (chart == 2) {
                comp.renderChart(this.mlChartData1, this.mlOptions1);
            } else if (chart == 3) {
                comp.renderChart(this.sbChartData1, this.sbOptions1);
            } else if (chart == 4) {
                comp.renderChart(this.lChartData2, this.lOptions2);
            } else if (chart == 5) {
                comp.renderChart(this.mlChartData2, this.mlOptions2);
            } else if (chart == 6) {
                comp.renderChart(this.sbChartData2, this.sbOptions2);
            }
            
        },

        resetZoom(chart) {
            var comp;

            if (chart == 1) {
                comp = this.$refs.lChart1;
            } else if (chart == 2) {
                comp = this.$refs.mlChart1;
            } else if (chart == 3) {
                comp = this.$refs.sbChart1;
            } else if (chart == 4) {
                comp = this.$refs.lChart2;
            } else if (chart == 5) {
                comp = this.$refs.mlChart2;
            } else if (chart == 6) {
                comp = this.$refs.sbChart2;
            }

            comp._data._chart.resetZoom()
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

                projectServers: this.projectServers,
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

                projectServers: this.projectServers2,
            }

            return filter
        },

        search1Chart() {

            //console.log("search1Chart")

            this.lineChartData(1)
            this.multilineChartData(1)
            this.stackedbarChartData(1)
            //this.barChartData(1)
            this.pieChartData(1, 1)
            this.pieChartData(1, 5)
            this.pieChartData(1, 9)

        },

        search2Chart() {

            //console.log("search2Chart")

            this.lineChartData(2)
            this.multilineChartData(2)
            this.stackedbarChartData(2)
            //this.barChartData(2)
            this.pieChartData(2, 1)
            this.pieChartData(2, 5)
            this.pieChartData(2, 9)

        },

        async pieChartData(searchArea, type) {

            if (searchArea == 1) {
                //this.isActivePie1 = true

                // Start Loading Spinner
                if (type == 1) {
                    this.isActivePie1 = true
                } else if (type == 5) {
                    this.isActivePie5_1 = true
                } else if (type == 9) {
                    this.isActivePieExtension1 = true
                }

            } else if (searchArea == 2) {
                //this.isActivePie2 = true

                // Start Loading Spinner
                if (type == 1) {
                    this.isActivePie2 = true
                } else if (type == 5) {
                    this.isActivePie5_2 = true
                } else if (type == 9) {
                    this.isActivePieExtension2 = true
                }

            }

            let filter = searchArea == 1 ? this.getFilter1() : this.getFilter2();

            try {
                let res = await getChartDataFromStatistics(type, this.project_id, filter, 5)

                if (searchArea == 1) {
                    //this.pChartData1 = getPieChartTemplate(res.x, res.y)
                    //this.isActivePie1 = false
                    if (type == 1) {
                        this.pChartData1 = getPieChartTemplate(res.x, res.y)
                        this.pOptions = getPieChartOptions("HTTP Status Codes");

                        //Stop Loading Spinner
                        //this.isActivePie = false
                    } else if (type == 5) {
                        this.pChartDataVisitorTop5_1 = getPieChartTemplate(res.x, res.y)
                        this.pOptions = getPieChartOptions("Visitor IP Top5");

                        //Stop Loading Spinner
                        //this.isActivePie5 = false
                    } else if (type == 9) {
                        this.pChartDataExtension1 = getPieChartTemplate(res.x, res.y)
                        this.pOptions = getPieChartOptions("Static File Types");

                        //Stop Loading Spinner
                        //this.isActivePieExtension = false
                    }

                } else {
                    //this.pChartData2 = getPieChartTemplate(res.x, res.y)
                    //this.isActivePie2 = false
                    if (type == 1) {
                        this.pChartData2 = getPieChartTemplate(res.x, res.y)
                        this.pOptions = getPieChartOptions("HTTP Status Codes");

                        //Stop Loading Spinner
                        //this.isActivePie = false
                    } else if (type == 5) {
                        this.pChartDataVisitorTop5_2 = getPieChartTemplate(res.x, res.y)
                        this.pOptions = getPieChartOptions("Visitor IP Top5");

                        //Stop Loading Spinner
                        //this.isActivePie5 = false
                    } else if (type == 9) {
                        this.pChartDataExtension2 = getPieChartTemplate(res.x, res.y)
                        this.pOptions = getPieChartOptions("Static File Types");

                        //Stop Loading Spinner
                        //this.isActivePieExtension = false
                    }
                }
                //this.pOptions = getPieChartOptions("HTTP Status Codes");

            } catch (err) {
                console.error(err); // TypeError: failed to fatch                
            } finally {
                //Stop Loading Spinner
                if (searchArea == 1) {
                    //this.isActivePie1 = false
                    //Stop Loading Spinner
                    if (type == 1) {
                        this.isActivePie1 = false;
                    } else if (type == 5) {
                        this.isActivePie5_1 = false;
                    } else if (type == 9) {
                        this.isActivePieExtension1 = false;
                    }
                } else if (searchArea == 2) {
                    //this.isActivePie2 = false
                    //Stop Loading Spinner
                    if (type == 1) {
                        this.isActivePie2 = false;
                    } else if (type == 5) {
                        this.isActivePie5_2 = false;
                    } else if (type == 9) {
                        this.isActivePieExtension2 = false;
                    }
                }
            }
        },

        async barChartData(searchArea) {
            // Start Loading Spinner
            if (searchArea == 1) {
                this.isActiveBar1 = true
            } else if (searchArea == 2) {
                this.isActiveBar2 = true
            }

            let filter = searchArea == 1 ? this.getFilter1() : this.getFilter2();

            try {
                let res = await getChartDataFromStatistics(1, this.project_id, filter, 5)
                if (searchArea == 1) {
                    this.bChartData1 = getBarChartTemplate(res.x, res.y, res.label)
                    this.isActiveBar1 = false
                } else {
                    this.bChartData2 = getBarChartTemplate(res.x, res.y, res.label)
                    this.isActiveBar2 = false
                }
            } catch (err) {

                console.error(err); // TypeError: failed to fatch

                if (searchArea == 1) {
                    this.isActiveBar1 = false
                } else if (searchArea == 2) {
                    this.isActiveBar2 = false
                }
            }

        },

        async stackedbarChartData(searchArea) {

            if (searchArea == 1) {
                this.isActiveStackedBar1 = true
            } else if (searchArea == 2) {
                this.isActiveStackedBar2 = true
            }

            let filter = searchArea == 1 ? this.getFilter1() : this.getFilter2();

            try {
                let res = await getLineChartData(2, this.timeCondition, this.project_id, filter)

                // Global Scale : 200, 300, 400, 500을 모두 더해주어야 한다.                
                //console.log(res)

                //var sumsbarY = new Array;
//
                //let scale_y_global = this.$store.state.global_Y_request_sbar;
                //let scale_y_global2 = this.$store.state.global_Y_request_sbar2;
                //let scale_y_local = 0;
                //
                //for (let i = 0 ; i < res.sbarX.length ; i++){
                //    sumsbarY.push(res.sbarY_200[i] + res.sbarY_300[i] + res.sbarY_400[i] + res.sbarY_500[i]);
                //}

                //let currentMax = Math.max.apply(null, sumsbarY);               
//
                //console.log("currentMax  : "+currentMax)
                //console.log("scale_y_global  : "+ scale_y_global)
                //console.log("scale_y_global2  : "+ scale_y_global2)
//
                //// Initialization
                //if (scale_y_global == "" || scale_y_global == "undefined" || scale_y_global == null )//{               
                //    this.$store.state.global_Y_request_sbar = currentMax;
                //}
//
                //if (scale_y_global2 == "" || scale_y_global2 == "undefined" || scale_y_global2 == null )//{               
                //    this.$store.state.global_Y_request_sbar2 = currentMax;
                //}
//
                //// Update global scale
                //scale_y_local = currentMax;
                //if (searchArea == 1) {                        
                //    this.$store.state.global_Y_request_sbar = currentMax;
                //    scale_y_global = currentMax;
                //    
                //} else if (searchArea == 2) {
                //    
                //    this.$store.state.global_Y_request_sbar2 = currentMax;
                //    scale_y_global2 = currentMax;                    
                //}
//
                //if (scale_y_global < scale_y_global2) {
                //    scale_y_local = scale_y_global2;                    
                //} else {
                //    scale_y_local = scale_y_global;                    
                //}
                //
                //console.log("scale_y_local  : "+scale_y_local)

                if (searchArea == 1) {
                    this.sbChartData1 = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500);
                    this.sbOptions1 = getStackedBarChartOptions('Http Status Code', this.dateFromValue+this.timeFromValue, this.dateToValue+this.timeToValue); 

                    this.$refs.sbChart1.renderChart(this.sbChartData1, this.sbOptions1);

                } else {
                    this.sbChartData2 = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500);
                    this.sbOptions2 = getStackedBarChartOptions('Http Status Code', this.dateFromValue2+this.timeFromValue2, this.dateToValue2+this.timeToValue2); 

                    this.$refs.sbChart2.renderChart(this.sbChartData2, this.sbOptions2);
                }                
                
            } catch (err) {

                console.error(err); // TypeError: failed to fatch

            } finally {
                if (searchArea == 1) {
                    this.isActiveStackedBar1 = false
                } else if (searchArea == 2) {
                    this.isActiveStackedBar2 = false
                }
            }
        },

        // 시계열 분석용 Line Chart
        async lineChartData(searchArea) {

            if (searchArea == 1) {
                this.isActiveLine1 = true
            } else if (searchArea == 2) {
                this.isActiveLine2 = true
            }

            try {
                let filter = searchArea == 1 ? this.getFilter1() : this.getFilter2();
                let res = await getLineChartData(1, this.timeCondition, this.project_id, filter)

                //let scale_y_global = this.$store.state.global_Y_tps;
                //let scale_y_global2 = this.$store.state.global_Y_tps2;
                //let scale_y_local = 0;
//
                //let currentMax = Math.max.apply(null, res.y);
//
                //console.log("currentMax  : "+currentMax)
                //console.log("scale_y_global  : "+ scale_y_global)
                //console.log("scale_y_global2  : "+ scale_y_global2)
//
                //// Initialization
                //if (scale_y_global == "" || scale_y_global == "undefined" || scale_y_global == null )//{               
                //    this.$store.state.global_Y_tps = currentMax;
                //}
//
                //if (scale_y_global2 == "" || scale_y_global2 == "undefined" || scale_y_global2 == null )//{               
                //    this.$store.state.global_Y_tps2 = currentMax;
                //}
//
                //// Update global scale
                //scale_y_local = currentMax;
                //if (searchArea == 1) {                        
                //    this.$store.state.global_Y_tps = currentMax;
                //    scale_y_global = currentMax;
                //    
                //} else if (searchArea == 2) {
                //    
                //    this.$store.state.global_Y_tps2 = currentMax;
                //    scale_y_global2 = currentMax;                    
                //}
//
                //if (scale_y_global < scale_y_global2) {
                //    scale_y_local = scale_y_global2;                    
                //} else {
                //    scale_y_local = scale_y_global;                    
                //}
                //
                //console.log("scale_y_local  : "+scale_y_local)


                if (searchArea == 1) {
                    
                    this.lChartData1 = getLineChartTemplate(res.x, res.y, "TPS")
                    this.lOptions1 = getLineChartOptions('Transaction Per Second', this.dateFromValue+this.timeFromValue, this.dateToValue+this.timeToValue); 

                    this.$refs.lChart1.renderChart(this.lChartData1, this.lOptions1);
                    
                } else {
                    
                    this.lChartData2 = getLineChartTemplate(res.x, res.y, "TPS")
                    this.lOptions2 = getLineChartOptions('Transaction Per Second', this.dateFromValue2+this.timeFromValue2, this.dateToValue2+this.timeToValue2); 

                    this.$refs.lChart2.renderChart(this.lChartData2, this.lOptions2);
                    
                }
                
            } catch (err) {

                console.error(err); // TypeError: failed to fatch               
            } finally {
                if (searchArea == 1) {
                    this.isActiveLine1 = false
                } else if (searchArea == 2) {
                    this.isActiveLine2 = false
                }
            }
        },

        // 시계열 분석용 Line Chart
        async multilineChartData(searchArea) {

            if (searchArea == 1) {
                this.isActiveMultiLine1 = true
            } else if (searchArea == 2) {
                this.isActiveMultiLine2 = true
            }

            try {
                let filter = searchArea == 1 ? this.getFilter1() : this.getFilter2();
                
                let res = await getLineChartData(3, this.timeCondition, this.project_id, filter)

                //console.log(res.y)
                //console.log(res.yt)

                // Global Scale 
                //let scale_y_request = this.$store.state.global_Y_request;                

                //if (scale_y_request == "" || scale_y_request == "undefined" || scale_y_request == null ){
                //    this.$store.state.global_Y_request = Math.max.apply(null, res.y);

                //} else {

                //    if (scale_y_request < Math.max.apply(null, res.y)){
                //        this.$store.state.global_Y_request = Math.max.apply(null, res.y);
                //    }                    
                //}

                //let scale_y_duration = this.$store.state.global_Y_duration;

                //if (scale_y_duration == "" || scale_y_duration == "undefined" || scale_y_duration == null ){
                //    this.$store.state.global_Y_duration = Math.max.apply(null, res.yt);

                //} else {

                //    if (scale_y_duration < Math.max.apply(null, res.yt)){
                //        this.$store.state.global_Y_duration = Math.max.apply(null, res.yt);
                //    }                    
                //}
                
                if (searchArea == 1) {
                    this.mlChartData1 = getMultiLineChartTemplate(res.x, res.y, 'Request (count)', res.yt, "Time-Taken")
                    this.mlOptions1 = getMultiLineChartOptions('Request (count) / Time-Taken', this.dateFromValue+this.timeFromValue, this.dateToValue+this.timeToValue); 

                    this.$refs.mlChart1.renderChart(this.mlChartData1, this.mlOptions1);
                } else {
                    this.mlChartData2 = getMultiLineChartTemplate(res.x, res.y, 'Request (count)', res.yt, "Time-Taken")
                    this.mlOptions2 = getMultiLineChartOptions('Request (count) / Time-Taken', this.dateFromValue2+this.timeFromValue2, this.dateToValue2+this.timeToValue2);

                    this.$refs.mlChart2.renderChart(this.mlChartData2, this.mlOptions2);
                }
                
                // TODO:, this.$store.state.global_Y_request, this.$store.state.global_Y_duration);

            } catch (err) {

                console.error(err); // TypeError: failed to fatch

            } finally {
                if (searchArea == 1) {
                    this.isActiveMultiLine1 = false
                } else if (searchArea == 2) {
                    this.isActiveMultiLine2 = false
                }
            }
        },
    },

    watch: {
        isSearch1() {
            this.search1Chart()
        },

        isSearch2() {
            this.search2Chart()
        },

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
