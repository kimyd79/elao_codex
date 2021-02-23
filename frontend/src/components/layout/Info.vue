<template>
<div id="info">
    <ui-card :columns="10" :height="170" :padding="4">
        <ui-card-item header>Information</ui-card-item>
        <ui-card-item sub class="card_box" >
            <span style="color:gray">
                Project Name (Total Log Lines) : {{ this.projectName }} ({{ totalLogLines.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }} lines)
                <br>
                Logfile Name : {{ this.fileNames }}
                <br>
                LogFormat : {{ this.logFormat }}
                <br>
                Period(Date/Time) : {{ this.dateFromValue }}/{{ this.timeFromValue }} ~ {{ this.dateToValue }}/{{ this.timeToValue }}
            </span>
        </ui-card-item>
        <ui-card-item body></ui-card-item>
    </ui-card>

</div>
</template>

<script>
import {
    mapGetters
} from "vuex";
import axios from "axios";

import {
    serverUrl
} from "@/common";

export default {
    name: "Info",
    data: function () {
        return {
            totalLogLines: "0"
        };
    },
    created() {

        let project_id = this.projectID
        //console.log(project_id)

        //var url = serverUrl + "/logdetail/statistics/"
        var url = serverUrl + "/logdetail_dynamic/statistics/"

        let postData = {

            project_id: project_id,
            type: 0,
            N: 0,
        };

        let axiosConfig = {
            headers: {
                //'Authorization': 'Token '+ this.token // For Django
            }
        };

        axios.post(url, postData, axiosConfig)
            .then(res => {
                //console.log(res)
                this.totalLogLines = res.data.results[0]["result_count"]

            })
            .catch(err => {
                console.error(err);
            })

    },

    computed: mapGetters({

        projectName: "getProjectName",
        fileNames: "getFileNames",
        logFormat: "getLogFormat",
        logFileID: "getLogFileID",
        projectID: "getProjectID",

        dateFromValue: "getGlobalFromDate",
        dateToValue: "getGlobalToDate",
        timeFromValue: "getGlobalFromTime",
        timeToValue: "getGlobalToTime",

    }),

};
</script>

<style scoped>
.card_box {
    max-height: 300px;
    overflow-y: auto;
}
</style>
