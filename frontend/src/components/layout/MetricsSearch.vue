<template>
    <div id="metricssearch">
        <ui-form-box>
            <ui-form-row>
                <!-- <ui-form-item :columns=8 
                    label="metrics kind" required left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="metric_kind" placeholder="enter metric kind" />
                </ui-form-item> -->
                <ui-form-item :columns=6 label="metrics kind">
                      <lego-dropdown :items="items" v-model="metric_kind" />
                </ui-form-item>
                <ui-form-item :columns=12 align-right margin-right>
                    <lego-button main v-on:click="getData">Search</lego-button>
                </ui-form-item>
            </ui-form-row>
        </ui-form-box>
    </div>
</template>

<script>
import EventBus from '../../EventBus';
import {
    getMetricskindLlist
} from "@/common";
export default {
    name: "MetricsSearch",

    data: function() {
        return {
          metric_kind: '',
          items: [],
        }
    },

    created() {
        this.items = getMetricskindLlist();
    },

    // computed: {
    //     conditions() {
    //         let rtn = [];
    //         // rtn.push({
    //         //     value: "N",
    //         //     text: "None"
    //         // });
    //         rtn.push({
    //             value: "threshhold",
    //             text: "threshhold"
    //         });
    //         rtn.push({
    //             value: "scope",
    //             text: "scope"
    //         });
    //         return rtn;
    //     }
    // },
    methods: {
        getData: function() {
            if( this.metric_kind == 'ALL') {
                this.metric_kind = ''
            }
            EventBus.$emit("searchMetrics", this.metric_kind);
            //console.log(this.project_name);
        }
    }
};
</script>

<style scoped>
</style>
