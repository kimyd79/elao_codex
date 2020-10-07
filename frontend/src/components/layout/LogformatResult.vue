<template>
<div id="logformatresult">

    <div class="page-summary-title">Logformat Search Result</div>

    <!-- component :is="currentView"></component -->
    <component :is="currentView" v-on:popupClose="currentView=null" :format="format"></component>

    <ui-form-item :columns=20 align-right margin-right>
        <lego-button main v-on:click="clickUpdate">Update</lego-button>
        <lego-button main v-on:click="clickAdd">Add</lego-button>
        <lego-button main v-on:click="clickDelete">Delete</lego-button>
    </ui-form-item>
    <div class="tb_box">
        <table class="page-summary-table">
            <thead>
                <tr>
                    <th>format id</th>
                    <th>format kind</th>
                    <th>format name</th>
                    <th>format strings</th>
                    <th>creator</th>
                    <th>created</th>
                </tr>
            </thead>
            <tbody id="list">                
                <tr v-for="(format_list, idx) in format_lists" :key="idx" v-on:click="clickList(format_list)" :class="{'highlight': (format_list.format_id == selected_format_id) }">
                    <td>{{format_list.format_id}}</td>
                    <td>{{format_list.format_kind}}</td>
                    <td>{{format_list.format_name}}</td>
                    <td>{{format_list.format_strings}}</td>
                    <td>{{format_list.creator}}</td>
                    <td>{{format_list.created}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import AddLogformatForm from './AddLogformatForm';
import UpdateLogformatForm from './UpdateLogformatForm';
import CommonPopup from './CommonPopup';
import store from '@/vuex/store';
import * as types from "@/vuex/mutation_types";
import {
    mapGetters
} from 'vuex';
import {
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/logformat/";

export default {
    name: 'LogformatResult',
    components: {
        AddLogformatForm,
        UpdateLogformatForm,
        CommonPopup,
    },
    data: function () {
        return {
            currentView: null,
            selected_format_id: null,
            format_lists: [],
            format: {
                format_id: '',
                format_kind: '',
                format_name: '',
                format_strings: '',
                creator: ''
            },
        }
    },
    mounted() {
        EventBus.$on("searchFormat", this.getData);
        EventBus.$on("cancel", () => {
            this.currentView = null;
        });
        EventBus.$on("addFormat", (format) => {
            this.addData(format);
            this.currentView = null;
        });
        EventBus.$on("updateOK", (format) => {
            this.currentView = null;
            this.currentView = 'updateLogformatForm';
        });
        EventBus.$on("updateFormat", (format) => {
            this.updateData(format);
            this.currentView = null;
        });
        EventBus.$on("deleteFormat", (format) => {
            this.deleteData(format);
            this.currentView = null;
        });

    },

    methods: {
        getData: function (format_kind) {
            //axios.get( 'http://127.0.0.1:8000/logformat/?format_kind='+format_kind)
            axios.get(urlStr + '?format_kind=' + format_kind)
                .then((response) => {
                    //console.log(response);
                    this.format_lists = response.data.results;
                    this.selected_format_id = '';
                    this.format.format_id = '';
                    this.format.format_kind = '';
                    this.format.format_name = '';
                    this.format.format_strings = '';
                    this.format.creator = '';
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        getDataOne: function (id) {
            //axios.get( 'http://127.0.0.1:8000/logformat/'+id)
            axios.get(urlStr + id)
                .then((response) => {
                    //console.log(response);
                    this.format_lists = response.data;
                })
                .catch((err) => {
                   console.error(err);
                })
        },
        deleteData: function (format) {
            //axios.delete( 'http://127.0.0.1:8000/logformat/'+format.format_id)
            axios.delete(urlStr + format.format_id)
                .then((response) => {
                    //console.log(response);
                    this.getData("");
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        addData: function (format) {
            //axios.post( 'http://127.0.0.1:8000/logformat/', format)
            axios.post(urlStr, format)
                .then((response) => {
                    //console.log(response);
                    this.getData("");
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        updateData: function (format) {
            //axios.put('http://127.0.0.1:8000/logformat/'+format.format_id+'/', format)
            axios.put(urlStr + format.format_id + '/', format)
                .then((response) => {
                    //console.log(response);
                    this.getData("");
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        clickList: function (format_list) {
            this.selected_format_id = format_list.format_id;
            this.format.format_id = format_list.format_id;
            this.format.format_kind = format_list.format_kind;
            this.format.format_name = format_list.format_name;
            this.format.format_strings = format_list.format_strings;
            this.format.creator = format_list.creator;
            EventBus.$emit("searchFormatDetail", format_list.format_kind);
            //console.log(this.format_kind);
            //console.log("click ID : " + format_list.format_id);

        },
        clickDelete: function () {
            if (this.format.format_id != '') {
                 this.$confirm("Are you sure want to Delete?", "Confirm Delete", "question").then(() => {
                    //console.log("OK clicked");
                    this.deleteData(this.format);
                }).catch(() => {
                    //console.log("Cancel clicked");
                });
            } else {
                this.$alert("No Logformat selected", "Confirm Update", "error");
            }
        },
        clickAdd: function () {
            this.currentView = 'AddLogformatForm';
        },
        clickUpdate: function () {
            if (this.format.format_id != '') {
                this.currentView = 'updateLogformatForm';
            } else {
                this.$alert("No Logformat selected", "Confirm Update", "error");
            }
        },
    }
};
</script>

<style scoped>
.highlight {
    color: #553CA5;
    background-color: #F3F1F9;
    font-weight: bold;
}

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
    max-height: 200px;
    overflow-y: auto;
}

.page-summary-table {
    border-spacing: 0;
    width: 100%;
    height: 20px;
}

.page-summary-table thead th {
    height: 28px;
    border-top: 1px solid #eaeaea;
    font-weight: normal;
    background-color: #f7f7f7;
}

.page-summary-table thead th+th {
    border-left: 1px solid #eaeaea;
}

.page-summary-table tbody td {
    width: 500px;
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
