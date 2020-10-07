<template>
<ui-container-box :columns="24" vertical align-center class="page-container-for-init">
    <div class="vld-parent">
        <ui-container-box :columns=12 vertical class="popup-container">
            <CommonPopup :is="currentView" v-on:popupClose="popupClose()" v-on:popupOK="popupOK()"></CommonPopup>

            <div class="popup-header">
                <div class="popup-header__title">
                    Initialization
                </div>
                <div class="popup-header__desc">
                    Set initial information for log analysis
                </div>
            </div>

            <ui-tab box :tabs="tabs" v-on:tabChange="tabChange" />

            <vue-element-loading :active="isActive" spinner="spinner" text="500MB 기준 약 100초 소요됩니다." :is-full-screen="false" color="#553ca5" />

            <div class="popup-form">

                <!-- STEP1 start -->
                <span id="step1" v-if="tabs[1].isSelected">

                    <ui-form-item :columns=11 label="Project" required-left left-label :label-width=144 :label-padding=16>
                        <lego-radio v-model="radioValue" value="1">New</lego-radio>
                        <lego-radio v-model="radioValue" value="2" v-on:click="getProjects">Exist</lego-radio>
                        &nbsp; &nbsp; &nbsp; &nbsp;
                        <lego-checkbox v-model="checkValue" v-if="radioValue == 2" small>Add Log Files</lego-checkbox>
                    </ui-form-item>

                    <ui-form-item :columns=11 label="Project Name" required-left left-label :label-width=144 :label-padding=16>
                        <lego-text-field v-model="projectName" />
                    </ui-form-item>

                    <ui-form-item :columns=11 label="Project Description" required-left left-label :label-width=144 :label-padding=16>
                        <lego-text-field textarea rows="3" v-model="projectDescription" />
                    </ui-form-item>

                    <!-- GridTable for existing project -->
                    <ui-container-box :columns="11" vertical v-if="radioValue == 2">
                        <ui-table header-divider no-action :columns="columns" :items="itemList" class="mt20"></ui-table>
                    </ui-container-box>
                    <!-- STEP1 end -->
                </span>

                <!-- STEP2 start -->
                <span id="step2" v-if="tabs[2].isSelected">
                    <ui-form-item :columns=11 label="File" required-left left-label :label-width=144 :label-padding=16>
                        <input type="file" id="file" ref="file" v-on:change="selectFile" />
                    </ui-form-item>

                    <ui-form-item :columns=11 label="File Size" required-left left-label :label-width=144 :label-padding=16>
                        {{ fileSize }} bytes
                    </ui-form-item>

                    <ui-form-item :columns=11 label="File Format" required-left left-label :label-width=144 :label-padding=16>
                        <lego-dropdown :items="items" v-model="fileFormat" width="650px" />
                    </ui-form-item>

                    <ui-form-item :columns="11" label="Data Range" required-left left-label :label-width=144 :label-padding=16>

                        <lego-radio v-model="dataRangeValue" value="1">ALL</lego-radio>
                        <lego-radio v-model="dataRangeValue" value="2">Select Range</lego-radio>

                    </ui-form-item>

                    <ui-form-item :columns="8" label="From ~ To" left-label :label-width=144 :label-padding=16 v-if="dataRangeValue == 2">

                        <date-picker type="date" value-type="format" format="YYYYMMDD" v-model="dateFromValue" default-value="dateFromValue" placeholder="YYYYMMDD" style="width:140px"></date-picker>&nbsp;&nbsp;
                        <date-picker type="time" value-type="format" format="HHmmss" v-model="timeFromValue" default-value="timeFromValue" placeholder="HHmmss" style="width:140px"></date-picker>
                        &nbsp;&nbsp;&nbsp;&nbsp;~&nbsp;&nbsp;&nbsp;&nbsp;
                        <date-picker type="date" value-type="format" format="YYYYMMDD" v-model="dateToValue" default-value="dateToValue" placeholder="YYYYMMDD" style="width:140px"></date-picker>&nbsp;&nbsp;
                        <date-picker type="time" value-type="format" format="HHmmss" v-model="timeToValue" default-value="timeToValue" placeholder="HHmmss" style="width:140px"></date-picker>

                    </ui-form-item>

                    <!-- STEP2 end -->
                </span>

                <!-- Current Info / STEP3 start -->
                <span id="step3" v-if="tabs[0].isSelected | tabs[3].isSelected">
                    <ui-form-item :columns=11 label="Project Name" required-left left-label :label-width=144 :label-padding=16>
                        {{ projectName }}
                    </ui-form-item>
                    <ui-form-item :columns=11 label="Project Description" required-left left-label :label-width=144 :label-padding=16>
                        {{ projectDescription }}
                    </ui-form-item>
                    <ui-form-item :columns=11 label="File" required-left left-label :label-width=144 :label-padding=16>
                        {{ fileName }}
                    </ui-form-item>
                    <ui-form-item :columns=11 label="File Format" required-left left-label :label-width=144 :label-padding=16>
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
                <lego-button v-if="isPrevShow" v-on:click="prevButton">Prev</lego-button>
                <lego-button v-on:click="nextButton" v-model="buttonName" main>{{ buttonName }}</lego-button>
                <lego-button v-on:click="deleteProjects" main>DelProjects</lego-button>
                <lego-button v-on:click="newProject">newProject</lego-button>
            </div>

        </ui-container-box>
    </div>
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
import {
    mapGetters
} from "vuex";

//Popup
import CommonPopup from '@/components/layout/CommonPopup';

// Spinner
import VueElementLoading from 'vue-element-loading'

// Timepicker
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';

import {
    serverUrl
} from "@/common";

export default {
    name: 'Init',

    // 컴포넌트 등록
    components: {
        Info,
        Notice,
        Search,
        Statistics,
        CommonPopup,

        // export Loading Spinner components
        VueElementLoading,

        DatePicker,
    },
    data() {
        return {
            buttonName: "Next",
            isPrevShow: false,
            isNewProject: false,

            projectName: "",
            projectDescription: "",
            //creator: "Leehs", // TODO : 인증처리 후 사용자 ID입력
            creator: this.$store.state.userName,
            projectID: "",

            fileName: "",
            fileSize: 0,
            fileFormat: "",
            logfileID: "",
            isNewFileAdded: false,

            dateFromValue: "",
            dateToValue: "",
            timeFromValue: "",
            timeToValue: "",

            radioValue: "1",
            checkValue: false,
            dataRangeValue: "1",

            // for file format
            items: [],

            // For file upload
            file: '',

            tabs: [{
                    label: "Current Info",
                    isSelected: true
                },
                {
                    label: "Step1",
                    isSelected: false
                },
                {
                    label: "Step2",
                    isSelected: false
                },
                {
                    label: "Step3",
                    isSelected: false
                }
            ],

            columns: [{
                    label: 'Project Name',
                    key: "projectName",
                    sortable: true,
                    sortValue: "asc",
                    filtable: false,
                    alignRight: false,
                    width: 30
                },
                {
                    label: 'Project Description',
                    key: "projectDescription",
                    sortable: true,
                    sortValue: "desc",
                    filtable: true,
                    filterValue: [],
                    alignRight: false,
                    width: 50
                },
                {
                    label: 'Creator',
                    key: "creator",
                    sortable: false,
                    filtable: true,
                    filterValue: [],
                    alignRight: false,
                    width: 15,
                    filterList: ["Success", "Error", "Processing"]
                },
                {
                    label: 'Created Date',
                    key: "createdDate",
                    sortable: false,
                    filtable: false,
                    alignRight: false,
                    width: 30
                },
            ],

            // Grid Rows
            itemList: [],

            // Loading Spinner
            isActive: false,

            // Popup view
            currentView: null,
            needToAdditionalFile: false,
        }
    },

    created() {
        // TODO : 인증에 대해 처리한다.  

        // Initial Value Setting
        this.projectName = this.$store.state.projectName
        this.projectDescription = this.$store.state.projectDescription
        this.fileName = this.$store.state.fileNames
        this.fileFormat = this.$store.state.logFormat

        // File format 가져오기
        var url = serverUrl + "/logformat"

        let axiosConfig = {
            headers: {
                //'Authorization': 'Token '+ this.token // For Django
            }
        };

        axios.get(url, axiosConfig)
            .then(res => {

                for (let i = 0; i < res.data.results.length; i++) {
                    let tmp = res.data.results[i].format_kind + '/' + res.data.results[i].format_name
                    this.items.push({
                        value: tmp + '/' + res.data.results[i].format_strings,
                        text: tmp + ' => ' + res.data.results[i].format_strings
                    });
                }

            })
            .catch(err => {
                console.error(err);
            })

    },

    computed: {

        ...mapGetters({
            isRowChecked: "getToggleSearch"
        }),
    },

    methods: {

        popupOK() {
            this.currentView = null
            //console.log("click popupOK")

            this.needToAdditionalFile = true;
        },

        popupClose() {
            this.currentView = null
            //console.log("click popupClose")

            this.needToAdditionalFile = false
        },

        selectRow() {

        },

        // TODO: common.js로 추출할 것
        setNoticePopup(content) {
            this.$store.dispatch("setPopupKind", 'Noti');
            this.$store.dispatch("setPopupHeader", 'Notification');
            this.$store.dispatch("setPopupBody", content);
            this.$store.dispatch("setPopupButton", 'Close');
        },

        // New Project
        newProject() {

            this.$confirm("Do you want to start new project?", "Are you sure?", "question").then(() => {
                //do something...
                //("OK clicked")

                this.isNewProject = true
                // 로그인 풀림 방지
                userToken = this.$store.state.userToken
                userName = this.$store.state.userName
                localStorage.removeItem("vuex")
                this.$store.reset()
                this.$store.dispatch("setUserToken", userToken)
                this.$store.dispatch("seUserName", userName)
                this.projectName = ""
                this.projectDescription = ""
                this.fileName = ""
                this.fileFormat = ""

                for (let i = 0; i < this.tabs.length; i++) {
                    if (this.tabs[i].isSelected == true) {
                        this.tabs[i].isSelected = false
                        this.tabs[0].isSelected = true
                        break;
                    }
                }
                //this.isNewProject = false

            }).catch(() => {
                //console.log("Cancel clicked");
            });

        },

        // For Test : Project 전체 지우기(인자 받으면 1개만 지우기)
        deleteProjects(projectID) {

            let projectIDList = []

            // Get Projects

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                }
            };

            axios.get(serverUrl + "/logmaster/", axiosConfig)
                .then(res => {
                    //console.log(res)

                    for (let i = 0; i < res.data.results.length; i++) {

                        projectIDList.push(res.data.results[i].project_id);

                        axios.delete(serverUrl + '/logmaster/' + res.data.results[i].project_id + '/', axiosConfig) // '가 아니라 `이다.
                            .then(res => {
                                //console.log(res.data)
                            })
                            .catch(err => {
                                console.error(err);
                            })
                    }

                })
                .catch(err => {
                    console.error(err);
                })
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

        getProjects() {

            //var url = serverUrl + "/logmaster/?search=" + this.creator
            var url = serverUrl + "/logmaster/?creator=" + this.creator

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                }
            };

            this.isActive = true

            return axios.get(url, axiosConfig)
                .then(res => {
                    //console.log(res)
                    this.setItemList(res.data.results);

                    this.isActive = false
                    this.$alert("Get project data completed..!!", "Notification", "success");

                })
                .catch(err => {
                    this.isActive = false
                    console.error(err);
                    this.$alert("Get project data failed..!!", "Notification", "error");
                })
        },

        prevButton() {
            if (this.tabs[1].isSelected) {
                this.isPrevShow = false
            } else if (this.tabs[3].isSelected) {
                this.buttonName = "Next"
                this.isPrevShow = true
            }

            this.tabChange(1)

        },

        async nextButton() {

            var isNext = true;

            // Next 버튼 처리
            if (this.tabs[0].isSelected) {
                this.isPrevShow = true
            }

            if (this.tabs[1].isSelected) { // Step1 : logmaster    

                if (this.radioValue == 1) { // New인 경우 새로운 정보로 저장한다.

                    try {

                        await this.createLogmaster(serverUrl);

                        await this.createLogdetailSchema(serverUrl)

                        isNext = true;
                    } catch (err) {
                        console.error(err);
                        isNext = false;
                    }
                } else if (this.radioValue == 2) { // Exist인 경우 기존 정보를 가져온다.

                    // 로그 파일을 추가할 것인가?
                    if (this.checkValue) {

                        // Step2로 이동
                        this.isNewFileAdded = true;
                    } else {
                        // Step3으로 이동 :한번 더 이동시킨다.
                        this.tabChange(2);
                        this.buttonName = "OK"
                        this.isNewFileAdded = false;

                        //선택한 project의 file 정보를 가져온다.
                        try {
                            await this.getLogfile(this.projectID);
                            isNext = true;
                        } catch (err) {
                            console.error(err);
                            isNext = false;
                        }
                    }
                }

            } else if (this.tabs[2].isSelected) { // Step2 : this.projectID

                try {
                    await this.createLogfile(serverUrl)
                    this.buttonName = "OK"
                    this.isNewFileAdded = true;
                    isNext = true;

                } catch (err) {
                    console.error(err);
                    isNext = false;
                }

            } else if (this.tabs[3].isSelected) { // Step3 : this.logfileID

                // TODO : Multi-File 및 기존 project에 File Add시 처리

                try {
                    // CASE1 : File을 새로 추가한 경우            
                    if (this.isNewFileAdded) {

                        await this.createLogdetail(serverUrl);

                    }

                    // CASE2 : 기존 File을 이용하는 경우                    
                    await this.getLogDetail(this.projectID)

                    isNext = true;
                } catch (err) {
                    console.error(err);
                    isNext = false;
                }
            }

            // Tab 변경 - Backward
            if (isNext) {
                // 처리 성공한 경우
                this.tabChange(2)

                // TODO: 마지막 처리 후에는 다른 위치로 옮겨줘야 한다. 
                //       또는 detail 만드는 작업을 하지 말아야 한다.(이거 추가)

            }

        },

        tabChange(dir) {

            if (dir == 1) { // Forward
                for (let i = 0; i < this.tabs.length; i++) {
                    if (this.tabs[i].isSelected == true) {
                        if (i - 1 >= 0) {
                            this.tabs[i].isSelected = false
                            this.tabs[i - 1].isSelected = true
                            break;
                        }
                    }

                }
            } else { // Backward
                for (let i = 0; i < this.tabs.length; i++) {
                    if (this.tabs[i].isSelected == true) {
                        if (i + 1 < this.tabs.length) {
                            this.tabs[i].isSelected = false
                            this.tabs[i + 1].isSelected = true
                            break;
                        }
                    }

                }
            }

        },

        createLogmaster(url) {
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

            this.isActive = true

            return axios.post(url + "/logmaster/", postData, axiosConfig)
                .then(res => {
                    //console.log(res)
                    this.projectID = res.data.project_id

                    // Set in vuex
                    this.$store.dispatch("setProjectID", this.projectID);

                    this.isActive = false

                    this.$alert("Create Logmaster Data completed.", "Notification", "success");
                })
                .catch(err => {
                    console.error(err);
                    this.isActive = false

                    this.$alert("Create Logmaster Data failed.", "Notification", "error");

                    throw err
                })
        },

        createLogdetailSchema(url) {
            let postData = {
                project_id: this.projectID,
            };

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                }
            };

            this.isActive = true

            return axios.post(url + "/logmaster/create_dynamic_logdetail/", postData, axiosConfig)
                .then(res => {

                    //console.log(res)

                    this.isActive = false

                    this.$alert("Create Dynamic Logdetail completed..", "Notification", "success");

                })
                .catch(err => {
                    console.error(err);
                    this.isActive = false

                    this.$alert("Create Dynamic Logdetail failed.", "Notification", "error");

                    throw err
                })
        },

        selectFile() {

            this.file = this.$refs.file.files[0];
            //console.log('size=' + this.file.size);
            //console.log('name=' + this.file.name);

            this.fileName = this.file.name
            this.fileSize = this.file.size

            this.$store.dispatch("setFileNames", this.fileName);

        },

        createLogfile(url) {

            // TODO: Multi-file upload 필요

            let formData = new FormData();
            formData.append('file_object', this.file);
            formData.append('file_name', this.fileName);
            formData.append('file_size', this.fileSize);

            let splitedFormat = this.fileFormat.split("/")

            formData.append('format_kind', splitedFormat[0]);
            formData.append('format_name', splitedFormat[1]);
            formData.append('file_format', splitedFormat[2]);

            formData.append('project', this.projectID);

            this.$store.dispatch("setLogFormat", this.fileFormat);

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                    'Content-Type': 'multipart/form-data'
                }
            };

            this.isActive = true

            return axios.post(url + '/logfile/', formData, axiosConfig)
                .then(res => {
                    //console.log(res)

                    this.logfileID = res.data.logfile_id

                    // Set in vuex
                    this.$store.dispatch("setLogFileID", this.logfileID);

                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Create Logfile(File Upload) completed..!!", "Notification", "success");
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Create Logfile(File Upload) failed..!!", "Notification", "error");

                    throw err
                })

        },

        createLogdetail(url) {

            let postData = {
                logfile_id: this.logfileID,
                project_id: this.projectID
            };

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                }
            };

            // Start Loading Spinner
            this.isActive = true
            return axios.post(url + "/logdetail_dynamic/", postData, axiosConfig)
                .then(res => {
                    //console.log(res)

                    this.$store.dispatch("setFromDate", res.data.start_date);
                    this.$store.dispatch("setToDate", res.data.end_date);
                    this.$store.dispatch("setFromTime", res.data.start_time);
                    this.$store.dispatch("setToTime", res.data.end_time);

                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Create Logdetail Data completed..!!", "Notification", "success");

                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Create Logdetail Data failed..!!", "Notification", "error");

                    throw err
                })
        },

        getLogfile(projectID) {

            var url = serverUrl + "/logfile?project=" + projectID

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                }
            };

            this.isActive = true

            return axios.get(url, axiosConfig)
                .then(res => {
                    //console.log(res.data)
                    //console.log(res.data.results[0])
                    //console.log(res.data.results[0].file_format)
                    //console.log(res.data.results[0].file_name)

                    // TODO : 파일이 없는 경우도 있다. (프로젝트만 만들어놓은 경우)
                    //        오류처리 해야 한다.
                    this.fileName = res.data.results[0].file_name
                    this.fileFormat = res.data.results[0].file_format
                    this.logfileID = res.data.results[0].logfile_id

                    this.$store.dispatch("setFileNames", this.fileName);
                    this.$store.dispatch("setLogFormat", this.fileFormat);
                    this.$store.dispatch("setLogFileID", this.logfileID);

                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Get Logfile Data completed..!!", "Notification", "success");
                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Get Logfile Data completed..!!", "Notification", "error");

                    throw err
                })
        },

        getLogDetail(projectID) {

            //console.log("getLogDetail projectID : " + projectID)

            // TODO: Dynamic
            var url = serverUrl + "/logdetail_dynamic/start_end/"
            //var url = serverUrl + "/logdetail/start_end/"

            let postData = {
                project_id: projectID
            };

            this.isActive = true

            return axios.post(url, postData)
                .then(res => {
                    //console.log(res)

                    this.$store.dispatch("setFromDate", res.data.start_date);
                    this.$store.dispatch("setFromTime", res.data.start_time);
                    this.$store.dispatch("setToDate", res.data.end_date);
                    this.$store.dispatch("setToTime", res.data.end_time);

                    var file_list = ""
                    res.data.file_names.forEach(file => file_list = file_list + file + ", ")

                    //("file_list - " + file_list)

                    this.fileName = file_list
                    this.$store.dispatch("setFileNames", file_list);
                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Get Logdetail Data completed..!!", "Notification", "success");

                })
                .catch(err => {
                    console.error(err);
                    // Stop Loading Spinner
                    this.isActive = false

                    this.$alert("Get Logdetail Data failed..!!", "Notification", "error");

                    throw err
                })

        },
    },
    watch: {
        async isRowChecked() {
            //console.log("Is isRowChecked?")
            //console.log("this.isNewProject : " + this.isNewProject)

            if (this.isNewProject == false) {

                // 초기정보 설정 : 기존 project 가져오기          
                this.projectName = this.$store.state.projectName
                this.projectDescription = this.$store.state.projectDescription
                this.projectID = this.$store.state.projectID

                await this.getLogfile(this.projectID)
            } else {
                this.isNewProject = false
            }
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
