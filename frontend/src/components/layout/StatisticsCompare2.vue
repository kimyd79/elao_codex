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

                        <td><VueCustomTooltip :label="item.result">
                             {{ item.result_count != 0 ? item.result.substr(0,70)+(item.result.length > 70 ? " ..." : "" ) : "-"}}
                            </VueCustomTooltip>
                        </td>
                        <td style="cursor:pointer" v-on:click="getDetail(item)"><u>{{ item.result_count }}</u> <br> {{ item.ratio }}</td>
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
import DetailPopup2 from './DetailPopup2';
import {
    serverUrl,
    setCommonStatisticInfo,
} from "@/common";

export default {
    name: 'Statistics',
    props: ['statisticsRow', 'statisticsKind'],

    components: {

        VueElementLoading,
        DetailPopup2,
    },

    data: function () {
        return {
            title: "",
            content: "",
            items: [{
                result: '- No Data -',
                result_count: '....',
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
        isSearch2: "getToggleSearch2",

        dateFromValue: "getFromDate2",
        dateToValue: "getToDate2",
        timeFromValue: "getFromTime2",
        timeToValue: "getToTime2",

        conditionValue: "getCondition2",
        searchValue: "getSearchKeyword2",
        excludeSearch: "getExcludeSearch2",

        ttFromValue: "getFromTimeTaken2",
        ttToValue: "getToTimeTaken2",

        project_id: "getProjectID",

    }),

    methods: {

        // TODO: 팝업창(상세) 필요
        /*
        getDetail(item) {
            alert('getDetail : ' + item)
            console.log(item)
        },
        */

        getDetail(item) {
            this.$store.dispatch("setPopupKind", 'Statistics');
            this.$store.dispatch("setPopupHeader", 'Statistics Detail');
            this.$store.dispatch("setDetailCondition", this.statisticsKind);
            this.$store.dispatch("setDetailSearchKeyword", item.result);
            this.$store.dispatch("setPopupBody", 'searchKeyword : ' + item.result);
            this.$store.dispatch("setPopupButton", 'Close');
            this.currentView = 'DetailPopup2';
        },

        setItems(results, totalCnt, resultType) {

            this.items = []

            for (let i = 0; i < results.length; i++) {

                var ratio = ""

                // fbyte 부분도 % 포함 (기존 : && resultType != '8' && resultType != '10')
                // fbyte average는 %에서 의미 찾기가 어려움
                if (resultType != '4' && resultType != '10' && resultType != '11') {

                    // 소수 3째자리에서 반올림
                    let pos = Math.pow(10, 3);
                    let val = Math.round((results[i].result_count / totalCnt) * pos * 100) / pos;
                    let percentile = val.toFixed(2);
                    //console.log("percentile = " + percentile);

                    ratio = "(" + percentile + "%)";
                }

                this.items.push({
                    result: results[i].result,
                    result_count: results[i].result_count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
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
                excludeSearch: this.excludeSearch,

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
        isSearch2() {

            this.getStatistics();
        }
    }

}
</script>

<style scoped>

</style>
