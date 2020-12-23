<template>
<div id="logformatsearch">
    <ui-form-box>
        <ui-form-row>
            <ui-form-item :columns=6 label="format kind" align-left>
                <lego-dropdown :items="conditions" v-model='format_kind' />
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

export default {
    name: "LogformatSearch",

    data: function () {
        return {
            format_kind: '',

        }
    },

    computed: {
        conditions() {
            let rtn = [];
            rtn.push({
                value: "ALL",
                text: "ALL"
            });
            rtn.push({
                value: "apache",
                text: "apache"
            });
            rtn.push({
                value: "tomcat",
                text: "tomcat"
            });
            rtn.push({
                value: "webtob",
                text: "webtob"
            });
            rtn.push({
                value: "jeus",
                text: "jeus(>= ver7)"
            });
            rtn.push({
                value: "IIS-W3C",
                text: "IIS-W3C"
            });
            rtn.push({
                value: "IIS-NCSA",
                text: "IIS-NCSA"
            });
            rtn.push({
                value: "nginx",
                text: "nginx"
            });

            return rtn;
        }
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
