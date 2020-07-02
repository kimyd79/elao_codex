<template>
  <div id="logformatsearch">
    <ui-form-box>
      <ui-form-row>
        <ui-form-item :columns=6 label="제품명" align-left>
            <lego-dropdown :items="[{value: 'ALL', text: 'ALL'}, {value: 'apache', text: 'apache'}, {value: 'nginx', text: 'nginx'}, {value: 'IIS', text: 'IIS'}]" v-model='format_kind'/>
        </ui-form-item>
        <!--
        <ui-form-item :columns=6 label="포맷명">
            <lego-dropdown :items="[{value: 'common', text: 'common'}, {value: 'commbined', text: 'combined'}, {value: 'custom', text: 'custom'}]" value="common"/>
        </ui-form-item>
        -->
        <ui-form-item :columns=14 align-right margin-right>
            <lego-button main v-on:click="getData">조회</lego-button>
        </ui-form-item>
      </ui-form-row>
    </ui-form-box>
  </div>
</template>

<script>
import EventBus from '../../EventBus';

export default {
  name: "LogformatSearch",

  data: function() {
      return {
        format_kind : ''
      }
    },
    methods: {
      getData: function() {
        if( this.format_kind == 'ALL') {
          this.format_kind = ''
        }
        EventBus.$emit("searchFormat", this.format_kind);
        EventBus.$emit("searchFormatDetail", 'Clear');
        console.log(this.format_kind);
      }
    }
};
</script>

<style scoped>
</style>
