<template>
  <div id="projectsearch">
    <ui-form-box>
      <ui-form-row>
        <!-- <ui-form-item :columns=6 label="project name" left-label :label-width=144 :label-padding=16 > -->
        <ui-form-item :columns=6 label="project name" align-left>
          <lego-text-field v-model="project_name" placeholder="enter project name" />
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
  name: "ProjectSearch",

  data: function() {
      return {
        project_name : ''
      }
    },
    methods: {
      getData: function() {
        if( this.project_name == 'ALL') {
          this.project_name = ''
        }
        EventBus.$emit("searchProject", this.project_name);
        //console.log(this.project_name);
      }
    }
};
</script>

<style scoped>
</style>
