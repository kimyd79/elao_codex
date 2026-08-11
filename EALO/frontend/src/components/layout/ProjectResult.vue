<template>
<div id="projectresult">

    <div class="page-summary-title">Project Result</div>

    <!-- component :is="currentView"></component -->
    <component :is="currentView" v-on:popupClose="currentView=null" :project="project"></component>

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
            <tr v-for="(project_list, idx) in project_lists" :key="idx" v-on:click="clickList(project_list)" :class="{'highlight': (project_list.project_id == selected_project_id) }">
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
import {
    mapGetters
} from 'vuex';

import {
    serverUrl
} from "@/common";

var urlStr = serverUrl + "/logmaster/";

export default {
    name: 'ProjectResult',
    components: {
        UpdateProject,
        CommonPopup,
    },
    data: function () {
        return {
            creator: this.$store.state.userName,
            currentView: null,
            selected_project_id: null,
            project_lists: [],
            project: {
                project_id: '',
                project_name: '',
                project_description: '',
                creator: '',
                created: ''
            },
        }
    },

    created() {
        EventBus.$on("searchProject", this.getData);
        EventBus.$on("cancelUpdateProject", () => {
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
    },
    beforeDestroy(){
        EventBus.$off("searchProject");
        EventBus.$off("cancelUpdateProject");
        EventBus.$off("updateOK");
        EventBus.$off("updateProject");
    },

    methods: {
        getData: function (project_name) {
            if (this.creator.toLowerCase() == 'leehs' || this.creator.toLowerCase() == 'admin') {
                var url = urlStr + '?search=' + project_name
            } else {
                var url = urlStr + '?search=' + project_name + '&creator=' + this.creator
            }

            axios.get(url)
                .then((response) => {
                    //console.log(response);
                    this.project_lists = response.data.results;
                    this.selected_project_id = '';
                    this.project.project_id = '';
                    this.project.project_name = '';
                    this.project.project_description = '';
                    this.project.creator = '';
                    this.project.created = '';
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        deleteData: async function (project) {

            return await axios.delete(urlStr + project.project_id)
                    .then((response) => {                        
                        this.getData("");
                        return true;
                    })
                    .catch((err) => {
                        console.error(err);
                        throw err;
                    })
        },
        updateData: function (project) {
            axios.put(urlStr + project.project_id + '/', project)
                .then((response) => {
                    //console.log(response);
                    this.getData("");
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        clickList: function (project_list) {
            this.selected_project_id = project_list.project_id;
            this.project.project_id = project_list.project_id;
            this.project.project_name = project_list.project_name;
            this.project.project_description = project_list.project_description;
            this.project.creator = project_list.creator;
            this.project.created = project_list.created;
            //console.log(this.project_name);
            //console.log("click ID : " + project_list.project_id);

        },        
        clickDelete: function () {
            if (this.project.project_id != '') {

                let project_id = this.project.project_id;

                this.$swal({
                    title: 'Notification',
                    html: 'Are you sure want to Delete?',                
                    icon: 'question',                        
                    showCancelButton: true,
                    cancelButtonColor: '#dddddd',
                    confirmButtonColor: '#553ca5',                
                    confirmButtonText: 'OK',         
                    reverseButtons: true,           
                }).then((result) => {
                    if (result.isConfirmed) {
                        
                        try {
                        let res = this.deleteData(this.project);
                        
                        console.log("== project_id : " + project_id);

                        if(res){                        
                            
                            // axios : POST
                            let postData = {
                                project_id: project_id,                            
                            };

                            axios.post(urlStr + "delete_dynamic_logdetail/", postData)
                                .then(res => {
                                    
                                    console.log("result : "+res);

                                })
                                .catch(err => {
                                    console.error(err);                            
                                    //throw err
                                })

                        }                        
                        } catch (err) {
                            console.error(err);
                        }
                    }
                });
               
            } else {

                this.$swal({
                    title: 'Notification',
                    html: 'No Project selected',
                    icon: 'error',
                    confirmButtonColor: '#553ca5',                
                    confirmButtonText: 'OK',
                });  
            }
        },
        clickUpdate: function () {
            if (this.project.project_id != '') {
                this.currentView = 'UpdateProject';
            } else {

                this.$swal({
                    title: 'Notification',
                    html: 'No Project selected',
                    icon: 'error',
                    confirmButtonColor: '#553ca5',                
                    confirmButtonText: 'OK',
                });
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
    max-height: 400px;
    overflow-y: auto;
}

.page-summary-table {
    border-spacing: 0;
    width: 100%;
    height: 20px;
}

.page-summary-table thead th {
    height: 28px;
    border-top: 1px solid #eaeaea;
    font-weight: normal;
    background-color: #f7f7f7;
    position: sticky;
    top: 0px;
}

.page-summary-table thead th+th {
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

.page-summary-table tbody td+td {
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
