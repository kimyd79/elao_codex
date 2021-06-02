<template>
<div id="notice" >
    
    <ui-card :columns="10" :height="160" :padding="2" >
        <ui-card-item header>Findings2</ui-card-item>
        <component :is="currentView" v-on:popupClose="currentView=null" :finding="finding"></component>
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
        <ui-card-item sub class="card_box">                        
            <span style="color:#553ca5" v-for="(finding, idx) in findingListResult" :key="idx"> 
                <b>[{{idx+1}}] {{finding.description}}</b>
                <span style="color:gray" v-for="(result, idx) in finding.results" :key="idx" v-on:click="getMetricDetailSearch(finding, result)"> 
                    {{result.result}} : {{result.result_count}} ( {{result.result_per}} %)
                </span>
                <br> 
            </span>           
        </ui-card-item>
        <ui-card-item body></ui-card-item>

    </ui-card>

</div>
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
    //getSearchFilter
} from "@/common";

export default {
    name: "Notice",

    components: {
        // export Loading Spinner components
        VueElementLoading,
        DetailPopup2,
    },

    data() {
        return {
            // Loading Spinner data
            isActive: false,
            LongTransactionCount: 0,
            currentView: null,
            findingList: [],
            findingListResult: [],
            finding: [{
                description: '',
                results: [],
                metric_type: '',
                metric_kind: '',
                metric_filter: '',
                metric_unit: '',
                metric_value1: '',
                metric_value2: '',
                metric_static: '',
            }],
        }
    },

    created() {
        this.getMetrics()
    },

    computed: mapGetters({
        projectName: "getProjectName",
        fileNames: "getFileNames",
        logFormat: "getLogFormat",
        logfileID: "getLogFileID",
        projectID: "getProjectID",

        dateFromValue: "getFromDate2",
        dateToValue: "getToDate2",
        timeFromValue: "getFromTime2",
        timeToValue: "getToTime2",
        conditionValue: "getCondition2",
        searchValue: "getSearchKeyword2",
        excludeSearch: "getExcludeSearch2",

        ttFromValue: "getFromTimeTaken2",
        ttToValue: "getToTimeTaken2",

        threshold: "getThreshold",

        isSearch: "getToggleSearch2",
    }),

    methods: {

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
            }

            return filter
        },


        async getMetrics() {                    
            
            let items = [];
            let description = '';

            // Start Loading Spinner
            this.isActive = true; 

            let postData = {
                project_id: this.projectID,

                filter: this.getFilter(),
            };

            
            await axios
                .post(serverUrl + "/logdetail_dynamic/findings/", postData)
                .then(res => {

                    for (let i = 0; i < res.data.findingsResult.length; i++) {
                        // 0인거 제외 : Test시에는 열어둔다.
                        if (res.data.findingsResult[i].results.length == 0 || res.data.findingsResult[i].results[0].result_count == 0 || res.data.findingsResult[i].results[0].result_count == ''){
                            continue;
                        }

                        // Kind : threshold, scope, pattern
                        // [Info] Response time ＞ 3 (sec) : 769 (count)
                        // [Info] Response time 3 ~ 5 (sec) : 769 (count)
                        // [Warn] Response specific string for URI ＞ 30 (%) : 769 (count)

                        description = "["+res.data.findingsResult[i].metric_type+"] "+ res.data.findingsResult[i].metric_definition + " ";
                                                
                        if (res.data.findingsResult[i].metric_kind == 'scope'){
                            description += res.data.findingsResult[i].metric_value1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " ~ " + res.data.findingsResult[i].metric_value2.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        }else {

                            if (res.data.findingsResult[i].metric_kind == 'pattern'){ 
                                description += " [pat='"+ res.data.findingsResult[i].metric_value2 +"']";
                            }

                            // threshold
                            description += " > " + res.data.findingsResult[i].metric_value1.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                        }
                        
                        description += " ("+res.data.findingsResult[i].metric_unit+") → ";

                        items.push({
                            description: description,                    
                            results: res.data.findingsResult[i].results,
                            metric_kind: res.data.findingsResult[i].metric_kind,
                            metric_type: res.data.findingsResult[i].metric_type,
                            metric_filter: res.data.findingsResult[i].metric_filter,
                            metric_filter2: res.data.findingsResult[i].metric_filter2,
                            metric_unit: res.data.findingsResult[i].metric_unit,
                            metric_value1: res.data.findingsResult[i].metric_value1,
                            metric_value2: res.data.findingsResult[i].metric_value2,
                            metric_static: res.data.findingsResult[i].metric_static,
                        }); 
                    };                                            
                })
                .catch(err => {
                    console.error(err);
                });

            this.findingListResult = items;

            //setTimeout("Temp", 1000);
            this.isActive = false;
    
        },

        getMetricDetailSearch(finding, result) {            
            this.finding = finding
            if (result.result == 'count') {
                this.$store.dispatch("setDetailSearchKeyword", "");
            } else{
                this.$store.dispatch("setDetailSearchKeyword", result.result);
            }            
            this.$store.dispatch("setDetailCondition", finding.metric_filter);
            this.$store.dispatch("setPopupKind", 'FindingsDetail2');
            this.$store.dispatch("setPopupHeader", 'Findings Detail2');            
            this.$store.dispatch("setPopupBody", finding.description);
            this.$store.dispatch("setPopupButton", 'Close');   
            this.currentView = 'DetailPopup2';
        },
    },
    watch: {
        
        isSearch() {
            this.getMetrics();
        }
    }
};
</script>

<style scoped>
.card_box {
    max-height: 300px;
    overflow-y: auto;
}
</style>
