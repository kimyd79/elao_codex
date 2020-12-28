<template>
<div id="logformatsearch">
    <ui-form-box>
        <ui-form-row>
            <ui-form-item :columns=6 label="format kind" align-left>
                <!-- <lego-dropdown :items="conditions" v-model='format_kind' /> -->
                <lego-dropdown :items="items" v-model='format_kind' />
            </ui-form-item>
            <ui-form-item :columns=14 align-right margin-right>
                <lego-button main v-on:click="getData">Search</lego-button>
            </ui-form-item>
        </ui-form-row>
    </ui-form-box>
</div>
</template>

<script>

import EventBus from '../../EventBus';
import axios from 'axios';
import {
    serverUrl
} from "@/common";

export default {
    name: "LogformatSearch",

    data: function () {
        return {
            format_kind: '',
            // for format_kind list
            items: [],
        }
    },

    created() {
        var url = serverUrl + "/logformatstring/formatkind_list/"

        let axiosConfig = {
            headers: {
                //'Authorization': 'Token '+ this.token // For Django
            }
        };

        axios.get(url, axiosConfig)
            .then(res => {
                //console.log(res);
                this.items.push({
                    value: "ALL",
                    text: "ALL"
                });
                for (let i = 0; i < res.data.list_format_kind.length; i++) {
                    let tmp = (res.data.list_format_kind[i] == "jeus") ? "jeus(>= ver7)" : res.data.list_format_kind[i];
                    this.items.push({
                        value: res.data.list_format_kind[i],
                        text: tmp
                    });
                }
            })
            .catch(err => {
                console.error(err);
            });
    },        

    methods: {
        getData: function () {
            if (this.format_kind == 'ALL') {
                this.format_kind = ''
            }
            EventBus.$emit("searchFormat", this.format_kind);
            EventBus.$emit("searchFormatDetail", 'Clear');
            //console.log(this.format_kind);
        }
    }
};
</script>

<style scoped>
</style>
