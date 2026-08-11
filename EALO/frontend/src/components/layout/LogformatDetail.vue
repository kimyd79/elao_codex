<template>
<div id="LogformatDetail">
    <div class="page-summary-title">Logformat Detail</div>
    <div class="tb_box">
        <table class="page-summary-table">
            <thead>
                <tr>
                    <th style="width: 70px;">format kind</th>
                    <th style="width: 70px;">format string</th>
                    <th>format definition</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(formatdetail_list, idx) in formatdetail_lists" :key="idx">
                    <td>{{formatdetail_list.format_kind}}</td>
                    <td>{{formatdetail_list.format_string}}</td>
                    <td>{{formatdetail_list.format_definition}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';

import {
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/logformatstring/";

export default {
    name: 'LogformatDetail',
    data: function () {
        return {
            formatdetail_lists: []
        }
    },
    created() {
        EventBus.$on("searchFormatDetail", this.getData);
    },
     beforeDestroy(){
        EventBus.$off("searchFormatDetail");
    },

    methods: {
        getData: function (format_kind) {
            axios.get(urlStr + '?format_kind=' + format_kind)
                .then((response) => {
                    //console.log(response);
                    this.formatdetail_lists = response.data.results;
                });
        }
    }
};
</script>

<style scoped>
.page-container {
    margin: 48px 0 32px;
    padding: 48px 80px;
    background-color: white;
}

.page-title {
    margin-top: 16px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #cccccc;
}

.page-title__label {
    font-size: 32px;
    font-weight: bold;
}

.page-form-area {
    padding: 16px 0;
    border-bottom: 1px solid #cccccc;
}

.page-summary-area {
    margin-top: 48px;
}

.page-summary-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 24px;
}

.tb_box {
    max-height: 500px;
    overflow-y: auto;
}

.page-summary-table {
    border-spacing: 0;
    width: 100%;
    height: 20px;
}

.page-summary-table thead th {
    width: 500px;
    height: 28px;
    border-top: 1px solid #eaeaea;
    font-weight: normal;
    background-color: #f7f7f7;
    position: sticky;
    top: 0px;
}

.page-summary-table thead th+th {
    border-left: 1px solid #eaeaea;
}

.page-summary-table tbody td {
    height: 44px;
    text-align: center;
    border-bottom: 1px solid #eaeaea;
}

.page-summary-table tbody tr:first-child td {
    border-top: 1px solid #a5a5a5;
}

.page-summary-table tbody td+td {
    border-left: 1px solid #eaeaea;
}

.page-tab-area {
    margin-top: 60px;
    border-bottom: 1px solid #cccccc;
}

.page-table-area {
    margin: 32px 0 24px;
}
</style>
