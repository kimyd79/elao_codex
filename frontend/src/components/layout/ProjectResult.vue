<template>
    <div id="projectresult">

      <div class="page-summary-title">Project Result</div>

      <!-- component :is="currentView"></component -->
      <component :is="currentView" v-on:popupClose="currentView=null" :project="project" v-on:popupOK="popupOK"></component>   

      <ui-form-item :columns=20 align-right margin-right>
          <lego-button main v-on:click="clickUpdate">Update</lego-button>
          <lego-button main v-on:click="clickDelete">Delete</lego-button>
      </ui-form-item>    
      <div class="tb_box">
      <table class="page-summary-table">
          <thead>
              <tr>
                  <th>project id</th>
                  <th>project name</th>
                  <th>project description</th>
                  <th>creator</th>
                  <th>created</th>
              </tr>
          </thead>
          <tbody id="list">
              <tr v-for="project_list in project_lists" :key="project_list" v-on:click="clickList(project_list)" :class="{'highlight': (project_list.project_id == selected_project_id) }">
                  <td>{{project_list.project_id}}</td>
                  <td>{{project_list.project_name}}</td>
                  <td>{{project_list.project_description}}</td>
                  <td>{{project_list.creator}}</td>
                  <td>{{project_list.created}}</td>
              </tr>
          </tbody>
      </table>
      </div>
    </div>

</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import UpdateProject from './UpdateProject';
import CommonPopup from './CommonPopup';
import store from '@/vuex/store';
import * as types from "@/vuex/mutation_types";
import { mapGetters } from 'vuex';

var urlStr = "http://127.0.0.1:8000/logmaster/";

export default {
    name: 'ProjectResult',
    components: { 
      UpdateProject,
      CommonPopup, 
    },
    data: function() {
      return {
        currentView : null,
        selected_project_id : null,
        project_lists : [],
        project : {project_id:'', project_name:'', project_description:'', creator:'', created:''},
      }
    },
    mounted() {
      EventBus.$on("searchProject", this.getData);
      EventBus.$on("cancel", () => {
        this.currentView = null;
      });
      EventBus.$on("updateOK", (project) => {
        this.currentView = null;
        this.currentView = 'UpdateProject';
      });
      EventBus.$on("updateProject", (project) => {
        this.updateData(project);
        this.currentView = null;
      });
      EventBus.$on("deleteProject", (project) => {
        this.deleteData(project);
        this.currentView = null;
      });
      
    },

    methods: {
      getData: function(project_name) {
        axios.get( urlStr + '?search='+project_name)
        .then((response) => {
                console.log(response);
                this.project_lists = response.data.results;
                this.selected_project_id = '';
                this.project.project_id = '';
                this.project.project_name = '';
                this.project.project_description = '';
                this.project.creator = '';        
                this.project.created = '';         
        })
        .catch((ex) => {
          console.log('getData failed', ex);
        })
      },
      deleteData: function(project) {
        axios.delete( urlStr + project.project_id)
        .then((response) => {
                console.log(response);
                this.getData(project.project_name);
        })
        .catch((ex) => {
          console.log('deleteData failed', ex);
        })
      },
      updateData: function(project) {
        axios.put( urlStr + project.project_id+'/', project)
        .then((response) => {
                console.log(response);
                this.getData(project.project_name);
        })
        .catch((ex) => {
          console.log('updateData failed', ex);
        })
      },
      clickList: function(project_list) {
        this.selected_project_id = project_list.project_id;
        this.project.project_id = project_list.project_id;
        this.project.project_name = project_list.project_name;
        this.project.project_description = project_list.project_description;
        this.project.creator = project_list.creator;
        this.project.created = project_list.created;
        console.log(this.project_name);
        console.log("click ID : " + project_list.project_id);

      },
      clickDelete: function() {
        this.$store.state.popupKind = 'Delete';
        this.$store.state.popupHeader = 'Confirm Delete';
        if (this.project.project_id != '') {
          this.$store.state.popupBody = 'Are you sure want to Delete? </p> ID : ' + this.selected_project_id;
          this.$store.state.popupprojectId = this.project.project_id;
          this.$store.state.popupprojectKind = this.project.project_name;
          this.$store.state.popupButton = 'CancelOK';
          this.currentView = 'CommonPopup';
        } else {
          this.$store.state.popupBody = 'No Project selected.';
          this.$store.state.popupButton = 'Close';
          this.currentView = 'CommonPopup';
        }       
      },
      clickUpdate: function() {
        this.$store.state.popupKind = 'Update';
        this.$store.state.popupHeader = 'Confirm Update';
        if (this.project.project_id != '') {
          this.currentView = 'UpdateProject';
        } else {
          this.$store.state.popupBody = 'No Project selected.';
          this.$store.state.popupButton = 'Close';
          this.currentView = 'CommonPopup';
        }
      },
      popupOK: function() {
        if (this.$store.state.popupKind == 'Delete') {
          console.log(this.project.project_id);
          this.deleteData(this.project);  
          this.currentView = null; 
        } else if(this.$store.state.popupKind == 'Update') {
          this.updateData(this.project);
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
  max-height:200px;
  overflow-y:auto;
}
.page-summary-table {
  border-spacing: 0;
  width:100%; 
  height:20px;
}
.page-summary-table thead th {
  height: 28px;
  border-top: 1px solid #eaeaea;
  font-weight: normal;
  background-color: #f7f7f7;
}
.page-summary-table thead th + th {
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
.page-summary-table tbody td + td {
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
