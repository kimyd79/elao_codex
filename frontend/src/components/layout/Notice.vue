<template>
<div id="notice">
    <ui-card :columns="10" :height="200">
        <ui-card-item header>Notice</ui-card-item>
        <ui-card-item sub>

            <!-- bar-fade-scale, color="#FF6700" -->
            <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5" />
            <span style="color:red">

                [CHECK] Long Transaction time [>= 3 seconds] : {{ this.LongTransactionCount }}

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

import {
    serverUrl
} from "@/common";

export default {
    name: "Notice",

    components: {
        // export Loading Spinner components
        VueElementLoading,

    },

    data() {
        return {
            isActive: false,
            LongTransactionCount: 0,
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
        timeToValue: "getToTime"
    }),

    methods: {
        getNotice() {

            let postData = {
                project_id: this.projectID
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
        }
    }
};
</script>

<style scoped>
</style>
