<template>

  <ui-container-box :columns="24" vertical align-center class="page-container-for-init">
    <ui-container-box :columns=12 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Initialization
                </div>
                <div class="popup-header__desc">
                    Set initial information for log analysis
                </div>                
            </div>

            <ui-tab box :tabs="tabs" v-on:tabChange="tabChange"/>

            <div class="popup-form">

                <!-- STEP1 start -->
                <span id="step1" v-if="tabs[1].isSelected">
                
                <ui-form-item :columns=11 label="Project" required-left left-label :label-width=144 :label-padding=16>
                    <lego-radio v-model="radioValue" value="1">New</lego-radio>
                    <lego-radio v-model="radioValue" value="2">Exist</lego-radio>                    
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Project Name" required-left left-label :label-width=144 :label-padding=16 >
                    <lego-text-field />
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Project Description" required-left left-label :label-width=144 :label-padding=16 >
                    <lego-text-field textarea rows="3" />
                </ui-form-item>

                <!-- TODO : GridTable for existing project -->
                <ui-container-box :columns="11" vertical>
                  <ui-table header-divider no-action :columns="columns" :items="itemList" class="mt20"></ui-table>
                </ui-container-box>
                <!-- STEP1 end -->
                </span>

                <!-- STEP2 start -->
                <span id="step2" v-if="tabs[2].isSelected">
                <ui-form-item :columns=11 
                    label="File" required-left left-label :label-width=144 :label-padding=16 >
                    <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="File Format" required-left left-label :label-width=144 :label-padding=16>
                  <lego-dropdown :items="items" v-model="value"/>
                </ui-form-item>

                <ui-form-item :columns="11" label="Data Range" required-left left-label :label-width=144 :label-padding=16 >
                  <lego-text-field v-model="dateFromValue" placeholder="YYYYMMDD" />
                  <lego-text-field v-model="timeFromValue" placeholder="hhmmss" />
                  &nbsp;&nbsp;&nbsp;&nbsp;~            
                  <lego-text-field v-model="dateToValue" placeholder="YYYYMMDD" />
                  <lego-text-field v-model="timeToValue" placeholder="hhmmss" />
                </ui-form-item>
                
                <!-- STEP2 end -->
                </span>    

                <!-- Current Info / STEP3 start -->
                <span id="step3" v-if="tabs[0].isSelected | tabs[3].isSelected">
                <ui-form-item :columns=11 
                    label="Project Name" required-left left-label :label-width=144 :label-padding=16 >
                    <!--{{ projectName }}-->
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="Project Description" required-left left-label :label-width=144 :label-padding=16 >
                    <!--{{ projectDescription }}-->
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="File" required-left left-label :label-width=144 :label-padding=16 >
                    <!--{{ fileName }}-->
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="File Format" required-left left-label :label-width=144 :label-padding=16 >
                    <!--{{ FileFormat }}-->
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="Data range" required-left left-label :label-width=144 :label-padding=16 >
                    <!--{{ this.dateFromValue }} {{timeFromValue}} ~ {{ dateToValue }} {{timeToValue}}-->
                </ui-form-item>

                <!-- STEP3 end -->
                </span>
            </div>            

            <div class="popup-buttons">
                <lego-button>Cancel</lego-button>
                <lego-button v-on:click="submitFile()" main>Next</lego-button>
            </div>

        </ui-container-box>
        </ui-container-box>
</template>

<script>

import axios from "axios";
import Info from '@/components/layout/Info'
import Init from '@/components/layout/Init'
import Notice from '@/components/layout/Notice'
import Search from '@/components/layout/Search'
import Statistics from '@/components/layout/Statistics'

export default {
  name: 'Init',

     // 컴포넌트 등록
  components:{
    'Info': Info,
    'Notice': Notice, 
    'Search': Search, 
    'Statistics': Statistics,

  },
  data: function() {
      return {
        
        dateFromValue: "",
        dateToValue: "",
        timeFromValue: "",
        timeToValue: "",

        radioValue: "",
        value: "",

          // for tabs
              

          // For file upload
          file: '',

          tabs: [
              { label: "Current Info",  isSelected: true },
              { label: "Step1",  isSelected: false },
              { label: "Step2",  isSelected: false },
              { label: "Step3",  isSelected: false }
          ],

          columns: [
            {label: 'Project Name', key: "projectName", sortable: true, sortValue: "asc", filtable: false, alignRight: false, width: 30 },
            {label: 'Project Description', key: "projectDescription", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 70 },
            {label: 'Creator', key: "creator", sortable: false, filtable: true, filterValue:[], alignRight: false, width: 15, filterList: ["Success","Error","Processing"] },
            {label: 'Created Date', key: "createdDate", sortable: false, filtable: false, alignRight: false, width: 20 },            
          ],

          // Grid Rows
          itemList: [
            {projectName:'MW LogAnalysys 1', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
            {projectName:'MW LogAnalysys 2', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
            {projectName:'MW LogAnalysys 3', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},            
            
          ]
      }
  },
  computed : {
        items() {
            // TODO : Get File Formats from DB
            let rtn = [];
            rtn.push({value:'A',text:'FileFormat A'});
            rtn.push({value:'B',text:'FileFormat B'});
            return rtn;
        }
    },
  methods: {

      tabChange(dir){
        
        if( dir == 1 ){ // Forward
            for (let i = 0; i < this.tabs.length; i++) {
                if (this.tabs[i].isSelected == true){
                    if ( i-1 >= 0){
                        this.tabs[i].isSelected = false
                        this.tabs[i-1].isSelected = true
                        break;
                    }
                }
                    
            }
        } else {    // Backward
            for (let i = 0; i < this.tabs.length; i++) {
                if (this.tabs[i].isSelected == true){
                    if ( i+1 < this.tabs.length){
                        this.tabs[i].isSelected = false
                        this.tabs[i+1].isSelected = true
                        break;
                    }
                }
                    
            }
        }


      },

      handleFileUpload(){
        this.file = this.$refs.file.files[0];
        console.log('size=' + this.file.size);
        console.log('name=' + this.file.name);
      },
      submitFile(){

            // TODO : Multi-file upload 필요

            let formData = new FormData();
            formData.append('file_object', this.file);
            formData.append('file_name', this.file.name);
            formData.append('file_size', this.file.size);

             // this.project
            let project = '3d2bb0b6-143b-4e61-a064-0d65bd3e4623'    // ID 가져와야 한다.
            formData.append('project', project);  

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                    'Content-Type': 'multipart/form-data'
                }
            };

            axios.post('http://172.16.1.110:8000/logfile/', formData, axiosConfig)
            .then(function(){
              console.log('SUCCESS!!');
            })
            .catch(function(){
              console.log('FAILURE!!');
            });
            
      },
  },

  watch: {
      tabs() {
          console.log(this.tabs[0])
          console.log(this.tabs[1])
          console.log(this.tabs[2])
          console.log(this.tabs[3])
      }
  }

}
</script>

<style scoped>
.popup-container {
    padding: 32px;
    border: 1px solid #D0D0D0;
    background-color: white;
}
.popup-header {
    position: relative;
    display: flex;
    flex-flow: column nowrap;
    margin-bottom: 32px;
}
.popup-header__title {
    font-size: 24px;
    font-weight: bold;
}
.popup-header__desc {
    color: #767676;
    margin-top: 16px;
}
.popup-header__close {
    position: absolute;
    top: 0;
    right: 0;
}
.popup-header__close:hover {
    cursor: pointer;
}
.popup-step {
    margin-top: 48px;
}
.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}
.popup-form .ui-form-item {
    margin-top: 32px;
}
</style>