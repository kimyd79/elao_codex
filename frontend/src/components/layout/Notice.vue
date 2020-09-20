<template>
<div id="notice">
    <component :is="currentView" v-on:popupClose="currentView=null"></component>
    <ui-card :columns="10" :height="200">
        <ui-card-item header>Notice</ui-card-item>
        <ui-card-item sub>

            <!-- bar-fade-scale, color="#FF6700" -->
            <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <span style="color:red" v-on:click="getLongTransactionDetail()">

                [CHECK] Long Transaction time [>= {{ this.threshold }} seconds] : {{ this.LongTransactionCount }}
                <!--[CHECK] Long Transaction time [>= 3 seconds] : {{ this.LongTransactionCount }}-->

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
import DetailPopup from './DetailPopup';
import {
    serverUrl
} from "@/common";

export default {
    name: "Notice",

    components: {
        // export Loading Spinner components
        VueElementLoading,
        DetailPopup, 
    },

    data() {
        return {
            isActive: false,
            LongTransactionCount: 0,
            currentView : null,
        }
    },

    created() {
        this.getNotice()
    },

    computed: mapGetters({
        projectName: "getProjectName",
        fileNames: "getFileNames",
        logFormat: "getLogFormat",
        logfileID: "getLogFileID",
        projectID: "getProjectID",

        dateFromValue: "getFromDate",
        dateToValue: "getToDate",
        timeFromValue: "getFromTime",
        timeToValue: "getToTime",
        threshold: "getThreshold"        
    }),

    methods: {
        getNotice() {

            let postData = {
                project_id: this.projectID,
                threshold: this.threshold
            };

            // Start Loading Spinner
            this.isLoading = true;
            axios
                //.post(serverUrl + "/logdetail/notice/", postData)
                .post(serverUrl + "/logdetail_dynamic/notice/", postData)
                .then(res => {
                    console.log(res);

                    this.LongTransactionCount = res.data.tiemtakenResult

                    // Stop Loading Spinner
                    this.isLoading = false;
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isLoading = false;
                });
        },
        getLongTransactionDetail: function () {
            //alert('LongTransactionCount : ' + this.LongTransactionCount)
            console.log(this.LongTransactionCount +', ' + this.threshold)
            this.$store.state.popupKind = 'LongTransaction';
            this.$store.state.popupHeader = 'Long Transaction Detail'; 
            this.$store.state.popupBody = 'threshold : >= ' + this.threshold +'seconds';
            this.$store.state.popupButton = 'Close';
            this.currentView = 'DetailPopup';
        },
    }
};
</script>

<style scoped>
</style>
