<template>
<keep-alive>
    <div class="vld-parent">
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
        <div id="statistics">
            <table class="page-summary-table">
                <thead>
                    <tr>
                        <th rowspan="2" style="width: 60px;">{{ this.title }}</th>
                        <th rowspan="2" style="width: 580px;">{{ this.content }}</th>
                        <th rowspan="2" style="width: 100px;">Result {{ this.timetakenUnit }}</th>
                    </tr>
                </thead>
                <tbody>

                    <tr v-for="(item, index) in items">
                        <td>{{ index+1 }}</td>

                        <!-- TODO: content 종류에 따라 style= "text-align:left;" 적용할 것 -->
                        <td v-on:click="getDetail(item)">{{ item.result.substr(0,70)+(item.result.length > 70 ? " ..." : "" )}}</td>
                        <td>{{ item.result_count }}</td>
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

import {
    serverUrl,
    setCommonStatisticInfo,
} from "@/common";

export default {
    name: 'Statistics',
    props: ['statisticsRow', 'statisticsKind'],

    components: {

        VueElementLoading,
    },

    data: function () {
        return {
            title: "",
            content: "",
            items: [{
                result: '...',
                result_count: '....',
            }, ],

            timetakenUnit: "",

            // Loading Spinner data
            isActive: false,

        }
    },

    created() {
        console.log(this.statisticsRow, this.statisticsKind)
    },

    computed: mapGetters({
        isSearch1: "getToggleSearch1",

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

        // TODO: 팝업창(상세) 필요
        getDetail(item) {
            alert('getDetail : ' + item)
            console.log(item)
        },

        setItems(results) {

            this.items = []

            for (let i = 0; i < results.length; i++) {
                this.items.push({
                    result: results[i].result,
                    result_count: results[i].result_count
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
                    console.log(res)
                    this.setItems(res.data.results);
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
        isSearch1() {

            this.getStatistics();
        }
    }

}
</script>

<style scoped>

</style>
