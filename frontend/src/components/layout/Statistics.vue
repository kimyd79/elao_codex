<template>
<keep-alive>
    <div class="vld-parent">
        <component :is="currentView" v-on:popupClose="currentView=null"></component>
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
        <div id="statistics">
            <table class="page-summary-table">
                <thead>
                    <tr>
                        <th rowspan="2" style="width: 60px; color: rgb(85,60,165)"><b>{{ this.title }}</b></th>
                        <th rowspan="2" style="width: 580px; color: rgb(85,60,165)"><b>{{ this.content }}</b></th>
                        <th rowspan="2" style="width: 100px; color: rgb(85,60,165)"><b>Result {{ this.timetakenUnit }}</b></th>
                    </tr>
                </thead>
                <tbody>

                    <tr v-for="(item, index) in items">
                        <td>{{ index+1 }}</td>

                        <!-- TODO: content 종류에 따라 style= "text-align:left;" 적용할 것 -->
                        <td v-on:click="getDetail(item)">{{ item.result.substr(0,70)+(item.result.length > 70 ? " ..." : "" )}}</td>
                        <td v-on:click="getDetail(item)">{{ item.result_count }} <br> {{ item.ratio }}</td>
                    </tr>

                </tbody>
            </table>
        </div>
    </div>
</keep-alive>
</template>

<script>
import axios from "axios";
import {
    mapGetters
} from "vuex";
import VueElementLoading from 'vue-element-loading'
import DetailPopup from './DetailPopup';
import {
    serverUrl,
    setCommonStatisticInfo
} from "@/common";

export default {
    name: 'Statistics',
    props: ['statisticsRow', 'statisticsKind'],

    components: {

        VueElementLoading,
        DetailPopup,
    },

    data: function () {
        return {
            title: "",
            content: "",
            items: [{
                result: '- No Data -',
                result_count: '...',
                ratio: ''
            }, ],

            timetakenUnit: "",

            // Loading Spinner data
            isActive: false,

            currentView: null,

        }
    },

    created() {
        //console.log(this.statisticsRow, this.statisticsKind)

        this.getStatistics();
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
        project_id: "getProjectID",

    }),

    methods: {

        getDetail(item) {
            this.$store.state.popupKind = 'Statistics';
            this.$store.state.popupHeader = 'Statistics Detail';
            this.$store.state.detailcondition = this.statisticsKind;
            this.$store.state.detailsearchKeyword = item.result;

            this.$store.state.popupBody = 'searchKeyword : ' + this.$store.state.detailsearchKeyword;
            this.$store.state.popupButton = 'Close';
            //console.log(this.items)
            this.currentView = 'DetailPopup';
        },

        setItems(results, totalCnt, resultType) {

            this.items = []

            for (let i = 0; i < results.length; i++) {

                var ratio = ""
                if (resultType != '4' && resultType != '8' && resultType != '10' && resultType != '11') {

                    //let percentile = (results[i].result_count / totalCnt).toFixed(4) * 100;
                    //console.log("percentile = " + percentile);

                    // 소수 3째자리에서 반올림
                    let pos = Math.pow(10, 3);
                    let val = Math.round((results[i].result_count / totalCnt) * pos * 100) / pos;
                    let percentile = val.toFixed(2);
                    //console.log("percentile = " + percentile);

                    ratio = "(" + percentile + "%)";
                }

                this.items.push({
                    result: results[i].result,
                    result_count: results[i].result_count,
                    ratio: ratio
                })

                if (results[i].timetakenUnit == 'D') {
                    this.timetakenUnit = "( ㎲ )"
                } else if (results[i].timetakenUnit == 'T') {
                    this.timetakenUnit = "( s )"
                }
            }
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

        getStatistics() {

            let commonInfo = setCommonStatisticInfo(this.statisticsKind, this.project_id, this.getFilter(), this.statisticsRow);

            this.title = "Top " + this.statisticsRow
            this.content = commonInfo.content
            // Start Loading Spinner
            this.isActive = true

            axios.post(commonInfo.url, commonInfo.postData, commonInfo.axiosConfig)
                .then(res => {
                    //console.log(res)
                    this.setItems(res.data.results, res.data.totalCnt, res.data.resultType);
                    //Stop Loading Spinner
                    this.isActive = false
                })
                .catch(err => {
                    console.error(err);
                    //Stop Loading Spinner
                    this.isActive = false
                })
        },
    },

    watch: {
        isSearch() {

            this.getStatistics();
        }
    }

}
</script>

<style scoped>

</style>
