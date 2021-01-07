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
    serverUrl,
    getFormatkindLlist
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
        this.items = getFormatkindLlist();
        this.items.push({
        value: "",
        text: "ALL"
        });
    },        

    methods: {
        getData: function () {
            EventBus.$emit("searchFormat", this.format_kind);
            EventBus.$emit("searchFormatDetail", 'Clear');
            //console.log(this.format_kind);
        }
    }
};
</script>

<style scoped>
</style>
