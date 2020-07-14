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
                    <lego-radio v-model="radioValue" value="1" >New</lego-radio>
                    <lego-radio v-model="radioValue" value="2" v-on:click="getProjects">Exist</lego-radio>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Project Name" required-left left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="projectName"/>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Project Description" required-left left-label :label-width=144 :label-padding=16 >
                    <lego-text-field textarea rows="3" v-model="projectDescription"/>
                </ui-form-item>

                <!-- TODO : GridTable for existing project -->
                <ui-container-box :columns="11" vertical v-if="radioValue == 2">
                  <ui-table header-divider no-action :columns="columns" :items="itemList" class="mt20"></ui-table>
                </ui-container-box>
                <!-- STEP1 end -->
                </span>

                <!-- STEP2 start -->
                <span id="step2" v-if="tabs[2].isSelected">
                <ui-form-item :columns=11 
                    label="File" required-left left-label :label-width=144 :label-padding=16 >
                    <input type="file" id="file" ref="file" v-on:change="selectFile"/>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="File Size" required-left left-label :label-width=144 :label-padding=16 >
                    {{ fileSize }} bytes
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="File Format" required-left left-label :label-width=144 :label-padding=16>
                  <lego-dropdown :items="items" v-model="fileFormat"/>
                </ui-form-item>

                <ui-form-item :columns="11" label="Data Range" required-left left-label :label-width=144 :label-padding=16 >

                    <lego-radio v-model="dataRangeValue" value="1" >ALL</lego-radio>
                    <lego-radio v-model="dataRangeValue" value="2">Select Range</lego-radio>  

                </ui-form-item>

                <ui-form-item :columns="11" label="" required-left left-label :label-width=144 :label-padding=16 v-if="dataRangeValue == 2">
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
                    {{ projectName }}
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="Project Description" required-left left-label :label-width=144 :label-padding=16 >
                    {{ projectDescription }}
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="File" required-left left-label :label-width=144 :label-padding=16 >
                    {{ fileName }}
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="File Format" required-left left-label :label-width=144 :label-padding=16 >
                    {{ fileFormat }}
                </ui-form-item>
                
                <!--
                <ui-form-item :columns=11 
                    label="Data range" required-left left-label :label-width=144 :label-padding=16 >
                    {{ this.dateFromValue }} {{timeFromValue}} ~ {{ dateToValue }} {{timeToValue}}
                </ui-form-item>
                -->

                <!-- STEP3 end -->
                </span>
            </div>            

            <div class="popup-buttons">
                <lego-button>Cancel</lego-button>
                <lego-button v-on:click="nextButton" v-model="buttonName" main>{{ buttonName }}</lego-button>
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

import * as types from "@/vuex/mutation_types";
import { mapGetters } from "vuex";

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
        buttonName: "Next",

        projectName: "",
        projectDescription: "",
        creator: "Leehs",      // TODO : 인증처리 후 사용자 ID입력
        projectID: "",

        fileName: "",
        fileSize: 0,
        fileFormat: "",
        logfileID: "",

        dateFromValue: "",
        dateToValue: "",
        timeFromValue: "",
        timeToValue: "",

        radioValue: "1",
        dataRangeValue: "1",

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
            {label: 'Project Description', key: "projectDescription", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 50 },
            {label: 'Creator', key: "creator", sortable: false, filtable: true, filterValue:[], alignRight: false, width: 15, filterList: ["Success","Error","Processing"] },
            {label: 'Created Date', key: "createdDate", sortable: false, filtable: false, alignRight: false, width: 30 },            
          ],

          // Grid Rows
          itemList: [
            //{projectName:'MW LogAnalysys 1', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
            //{projectName:'MW LogAnalysys 2', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
            //{projectName:'MW LogAnalysys 3', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},            
            
          ]
      }
  },

  created() {
    // TODO : 인증에 대해 처리한다.  
    
    // Initial Value Setting
    this.projectName = this.$store.state.projectName
    this.fileName = this.$store.state.fileNames
    this.fileFormat = this.$store.state.logFormat
    
  },
  computed: { 
      
      ...mapGetters({
        isRowChecked: "getToggleSearch"
      }),
    

          items() {
            // TODO : Get File Formats from DB
            let rtn = [];
            rtn.push({value:'%h %l %u %t \"%r\" %>s %b',text:'Common Log Format(CLF) => %h %l %u %t \"%r\" %>s %b'});
            rtn.push({value:'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"',text:'NCSA extended/combined => %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"'});
            rtn.push({value:'TODO',text:'TODO : Custom '});
            return rtn;
        },
    },
  methods: {

      selectRow() {

      },
      
      setItemList(results) {

        this.itemList = [];

        for (let i = 0; i < results.length; i++) {
            this.itemList.push({
                projectName: results[i].project_name,
                projectDescription: results[i].project_description,
                creator: results[i].creator,
                createdDate: results[i].created,
                isSelected: false,
                projectID: results[i].project_id
            })
        }
      },

      getProjects(project_id){
          // {projectName:'MW LogAnalysys 1', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
          //{projectName:'MW LogAnalysys 2', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
          //{projectName:'MW LogAnalysys 3', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},            
            
          // /logmaster/?search=Leehs       
        // "+(project_id != '' ? project_id+"/" : project_id)+"
          var url = "http://127.0.0.1:8000/logmaster/?search="+this.creator

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          axios.get(url,axiosConfig)
          .then(res => {
              console.log(res)
              this.setItemList(res.data.results);
              
          })
          .catch(err => {
              console.error(err); 
          })
      },
      nextButton(){

        // Next 버튼 처리
        if(this.tabs[0].isSelected){
            this.buttonName = "OK"
        }

        // Logic 처리 : TODO - Global 변수로 뺄 것
        var url = "http://127.0.0.1:8000"       

        // for Test : --> TODO : vuex에 추가할 것
        //this.projectID = '49898027-f29d-4d7e-9a68-ab590e46e783'
        //this.logfileID = 'c2eaa555-4980-4945-8bd9-6afcdda4de4e'
        
        if(this.tabs[1].isSelected){ // Step1 : logmaster    
            
            if(this.radioValue == 1 & this.projectID == ""){   // New인 경우 새로운 정보로 저장한다.

                 this.createLogmaster(url);
            }else{        
                              // Exist인 경우 - TODO : 현재 ID 기준으로 기존 project들을 가져와서 보여준다.
            }
            
        } else if(this.tabs[2].isSelected  & this.projectID != ""){ // Step2 : 

            // TODO : Tab 왔다갔다 할때 체크로직 필요
            this.createLogfile(url)

        } else if(this.tabs[3].isSelected  & this.logfileID != ""){ // Step3 or Info

            // TODO : Tab 왔다갔다 할때 체크로직 필요
            this.createLogdetail(url)
        }

        // Tab 변경 - Backward
        this.tabChange(2)
      },

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

      createLogmaster(url){
          let postData = {
                
                project_name: this.projectName,        
                project_description: this.projectDescription,
                creator: this.creator
            };

            this.$store.dispatch("setProjectName", this.projectName);

            let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

            axios.post(url+"/logmaster/", postData, axiosConfig )
            .then(res => {
                console.log(res)                
                this.projectID = res.data.project_id
                
                // Set in vuex
                this.$store.dispatch("setProjectID", this.projectID);
                
            })
            .catch(err => {
                console.error(err); 
            })
      },

      selectFile(){

        this.file = this.$refs.file.files[0];
        console.log('size=' + this.file.size);
        console.log('name=' + this.file.name);

        this.fileName = this.file.name
        this.fileSize = this.file.size

        this.$store.dispatch("setFileNames", this.fileName);

      },

      createLogfile(url){

            // TODO : Multi-file upload 필요

            let formData = new FormData();
            formData.append('file_object', this.file);
            formData.append('file_name', this.fileName);
            formData.append('file_size', this.fileSize);
            formData.append('file_format', this.fileFormat);
            formData.append('project', this.projectID);  
            
            this.$store.dispatch("setLogFormat", this.fileFormat);            

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                    'Content-Type': 'multipart/form-data'
                }
            };

            axios.post(url+'/logfile/', formData, axiosConfig)
            .then(res => {
                console.log(res)
                
                this.logfileID = res.data.logfile_id

                // Set in vuex
                this.$store.dispatch("setLogFileID", this.logfileID);
            })
            .catch(err => {
                console.error(err); 
            })
            
      },

      createLogdetail(url){

            let postData = {
                logfile: this.logfileID
            };

            let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          // TODO : Progress Bar가 필요하다.
          axios.post(url+"/logdetail/", postData, axiosConfig )
            .then(res => {
                console.log(res)

                // TODO : 로그의 시작날짜와 시간을 받아와서 vuex에 입력한다.
                //        끝 시간은 +1 시간으로 설정(기본)
                let day = res.data.result[19]
                let month = res.data.result[20]
                let year = res.data.result[21]

                let hour = res.data.result[22]
                let minute = res.data.result[23]
                let second = res.data.result[24]

                this.$store.dispatch("setFromDate", year+month+day);
                this.$store.dispatch("setToDate", year+month+day);
                this.$store.dispatch("setFromTime", hour+minute+second);
                this.$store.dispatch("setToTime", hour+minute+second);

                
            })
            .catch(err => {
                console.error(err); 
            })
      }
  },
  watch: {
      isRowChecked(){
        console.log("Is isRowChecked?")
          
        this.projectName = this.$store.state.projectName
        this.projectDescription = this.$store.state.projectDescription

        // TODO : project id로 file 정보 가져오기 (여기부터....)
        this.fileName = this.$store.state.fileNames
        this.fileFormat = this.$store.state.logFormat
          
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