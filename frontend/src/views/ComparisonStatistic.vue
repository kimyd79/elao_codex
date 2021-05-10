<template>
<ui-container-box :columns="22" vertical align-center class="page-container">
    <ui-container-box :columns="20" horizontal align-center class="page-title">
        <span class="page-title__label">Comparison - Statistic</span>
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

    <ui-container-box :columns="20" horizontal align-left class="page-title">

        <ui-container-box :columns="10" vertical >
            <span class="page-title__2label">Statistics - Top {{ valueN1 == 0 ? "" : valueN1 }}</span>
            <ui-form-row>
                <ui-form-item :columns="10" label="Select N" align-left required-left>
                    <lego-dropdown :items="listN1" v-model="valueN1" width="100px" />
                </ui-form-item>
            </ui-form-row>
        </ui-container-box>

        <ui-container-box :columns="10" vertical >
            <span class="page-title__2label">Statistics - Top {{ valueN2 == 0 ? "" : valueN2 }}</span>
            <ui-form-row>
                <ui-form-item :columns="10" label="Select N" align-left required-left>
                    <lego-dropdown :items="listN2" v-model="valueN2" width="100px" />
                </ui-form-item>
            </ui-form-row>
        </ui-container-box>

    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
        <component :is="currentView" v-on:popupClose="currentView=null" :row="valueN1" :kind="kind"></component>

        <ui-container-box :columns="10" vertical>
            <ui-form-row align-left >
                <lego-button  v-on:click="PopupStatisticsKind2" v-if="creator.toLowerCase() == 'leehs' || creator.toLowerCase() == 'admin'" small main>PopupStatistics</lego-button>
            </ui-form-row>
            <!-- TODO: this.logFormat[0] -> 동일하게 1개만 우선, 단, 여러개 일때 처리 필요 -->

            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="2"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="5"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="4" v-if="this.logFormat[0].indexOf('%D')!=-1 || this.logFormat[0].indexOf('%T')!=-1"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="11" v-if="this.logFormat[0].indexOf('%D')!=-1 || this.logFormat[0].indexOf('%T')!=-1"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="1"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="3"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="8"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="10"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="12"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="9"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="6" v-if="this.logFormat[0].indexOf('Referer')!=-1"></statistics-compare1>
            <statistics-compare1 :statisticsRow="valueN1" :statisticsKind="7" v-if="this.logFormat[0].indexOf('User-Agent')!=-1"></statistics-compare1>
        </ui-container-box>

        <ui-container-box :columns="10" vertical>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="2"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="5"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="4" v-if="this.logFormat[0].indexOf('%D')!=-1 || this.logFormat[0].indexOf('%T')!=-1"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="11" v-if="this.logFormat[0].indexOf('%D')!=-1 || this.logFormat[0].indexOf('%T')!=-1"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="1"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="3"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="8"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="10"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="12"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="9"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="6" v-if="this.logFormat[0].indexOf('Referer')!=-1"></statistics-compare2>
            <statistics-compare2 :statisticsRow="valueN2" :statisticsKind="7" v-if="this.logFormat[0].indexOf('User-Agent')!=-1"></statistics-compare2>
        </ui-container-box>

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
import Info from "@/components/layout/Info";
import Init from "@/components/layout/Init";
import Notice from "@/components/layout/Notice";
import Notice2 from "@/components/layout/Notice2";
import Search from "@/components/layout/Search";
import SearchCompare1 from "@/components/layout/SearchCompare1";
import SearchCompare2 from "@/components/layout/SearchCompare2";
import StatisticsCompare1 from "@/components/layout/StatisticsCompare1";
import StatisticsCompare2 from "@/components/layout/StatisticsCompare2";
import PopupStatistics from '@/components/layout/PopupStatistics';

import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from "vuex";

import VueElementLoading from 'vue-element-loading'

export default {
    name: "Compare_statistic",

    // 컴포넌트 등록
    components: {
        Info,
        Notice,
        Notice2,
        SearchCompare1,
        SearchCompare2,
        StatisticsCompare1,
        StatisticsCompare2,
        VueElementLoading,
        PopupStatistics
    },
    data() {
        return {
            // For Statistics N
            valueN1: 5,
            valueN2: 5,

            logfile_id: '',
            project_id: '',

            currentView: null,
            creator: this.$store.state.userName,

            kind: '',

        }

    },

    created() {

        this.logfile_id = this.$store.state.logFileID
        this.project_id = this.$store.state.projectID

    },
    computed: {
        listN1() {
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

        listN2() {
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
            isSearch1: "getToggleSearch1",
            isSearch2: "getToggleSearch2",

            dateFromValue: "getFromDate",
            dateToValue: "getToDate",
            timeFromValue: "getFromTime",
            timeToValue: "getToTime",

            conditionValue: "getCondition",
            searchValue: "getSearchKeyword",

            ttFromValue: "getFromTimeTaken",
            ttToValue: "getToTimeTaken",

            logFormat: "getLogFormat",
        }),
    },
    methods: {

        PopupStatisticsKind2(){
            this.kind = 2
            this.currentView = 'PopupStatistics';
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

    },

    watch: {

        valueN1() {
            this.$store.dispatch("setToggleSearch1");
        },

        valueN2() {
            this.$store.dispatch("setToggleSearch2");
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
