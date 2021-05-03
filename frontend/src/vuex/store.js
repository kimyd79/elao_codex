import Vue from 'vue'
import Vuex from 'vuex'

import getters from './getters'
import actions from './actions'
import * as types from './mutation_types'

import createPersistedState from "vuex-persistedstate";
import { createStore } from 'vuex-extensions'

Vue.use(Vuex)

// state
const state = {
    
    // common info
    projectName: '',
    projectDescription: '',
    projectID: '',

    fileNames: '',
    logFormat: '',
    logFileID: '',

    // Files will have fileinfo objects
    // logfile_id, file_name, file_size, file_format, is_new
    projectFiles: '',

    // Global Date, Time (immutable) -Global  Scale X 
    global_fromDate: '',
    global_toDate: '',
    global_fromTime: '',
    global_toTime: '',

    // Global Scale Y
    global_Y_tps: '',
    global_Y_request: '',
    global_Y_duration: '',
    global_Y_request_sbar: '',

    // Global Scale Y2
    global_Y_tps2: '',
    global_Y_request2: '',
    global_Y_duration2: '',
    global_Y_request_sbar2: '',   
    
    // search info   
    fromDate: '',
    toDate: '',
    fromTime: '',
    toTime: '',
    fromTimeTaken: '',
    toTimeTaken: '',
    condition: '',
    searchKeyword: '',
    excludeSearch: false,

    // search info2   
    fromDate2: '',
    toDate2: '',
    fromTime2: '',
    toTime2: '',
    fromTimeTaken2: '',
    toTimeTaken2: '',
    condition2: '',
    searchKeyword2: '',
    excludeSearch2: false,

    // statistic detailpopup
    detailcondition: '',
    detailsearchKeyword: '',
    threshold: 3,

    // check
    toggleSearch: '0',  //  0 or 1 변경사항 확인용
    
    // For Comparison
    toggleSearch1: '0',  //  0 or 1 변경사항 확인용    
    toggleSearch2: '0',  //  0 or 1 변경사항 확인용
    
    //login info
    userToken: '',
    userName: 'Not logged in', 
    
    //popup info
    popupHeader: '',
    popupBody: '', 
    popupButton: '', 
    popupReturn: '', 
    popupKind: '', 
    popupFormatId: '',
    popupFormatKind: '', 

    //metric info
    metricId: ''
}

// mutation
const mutations = {

    // common info
    [types.SET_PROJECTNAME] (state, value) { state.projectName = value },
    [types.SET_PROJECTDESCRIPTION] (state, value) { state.projectDescription = value },
    [types.SET_FILENAMES] (state, value) { state.fileNames = value },
    [types.SET_LOGFORMAT] (state, value) { state.logFormat = value },
    [types.SET_PROJECTID] (state, value) { state.projectID = value },
    [types.SET_LOGFILEID] (state, value) { state.logFileID = value },

    [types.SET_PROJECTFILES] (state, value) { state.projectFiles = value },    

    // global time, date
    [types.SET_GLOBAL_FROMDATE] (state, value) { state.global_fromDate = value },
    [types.SET_GLOBAL_TODATE] (state, value) { state.global_toDate = value },
    [types.SET_GLOBAL_FROMTIME] (state, value) { state.global_fromTime = value },
    [types.SET_GLOBAL_TOTIME] (state, value) { state.global_toTime = value },

    // global Y
    [types.SET_GLOBAL_Y_TPS] (state, value) { state.global_Y_tps = value },
    [types.SET_GLOBAL_Y_REQUEST] (state, value) { state.global_Y_request = value },
    [types.SET_GLOBAL_Y_DURATION] (state, value) { state.global_Y_duration = value },
    [types.SET_GLOBAL_Y_REQUEST_SBAR] (state, value) { state.global_Y_request = value },

    // global Y2
    [types.SET_GLOBAL_Y_TPS2] (state, value) { state.global_Y_tps2 = value },
    [types.SET_GLOBAL_Y_REQUEST2] (state, value) { state.global_Y_request2 = value },
    [types.SET_GLOBAL_Y_DURATION2] (state, value) { state.global_Y_duration2 = value },
    [types.SET_GLOBAL_Y_REQUEST_SBAR2] (state, value) { state.global_Y_request2 = value },

    // search info
    [types.SET_FROMDATE] (state, value) { state.fromDate = value },
    [types.SET_TODATE] (state, value) { state.toDate = value },
    [types.SET_FROMTIME] (state, value) { state.fromTime = value },
    [types.SET_TOTIME] (state, value) { state.toTime = value },
    [types.SET_FROMTIMETAKEN] (state, value) { state.fromTimeTaken = value },
    [types.SET_TOTIMETAKEN] (state, value) { state.toTimeTaken = value },
    [types.SET_CONDITION] (state, value) { state.condition = value },
    [types.SET_SEARCHKEYWORD] (state, value) { state.searchKeyword = value },
    [types.SET_EXCLUDESEARCH] (state, value) { state.excludeSearch = value },
    
    // search info 2
    [types.SET_FROMDATE2] (state, value) { state.fromDate2 = value },
    [types.SET_TODATE2] (state, value) { state.toDate2 = value },
    [types.SET_FROMTIME2] (state, value) { state.fromTime2 = value },
    [types.SET_TOTIME2] (state, value) { state.toTime2 = value },
    [types.SET_FROMTIMETAKEN2] (state, value) { state.fromTimeTaken2 = value },
    [types.SET_TOTIMETAKEN2] (state, value) { state.toTimeTaken2 = value },
    [types.SET_CONDITION2] (state, value) { state.condition2 = value },
    [types.SET_SEARCHKEYWORD2] (state, value) { state.searchKeyword2 = value },
    [types.SET_EXCLUDESEARCH2] (state, value) { state.excludeSearch2 = value },

    [types.TOGGLE_SEARCH] (state) { state.toggleSearch == 1 ? state.toggleSearch = 0 : state.toggleSearch = 1 },
    
    [types.TOGGLE_SEARCH1] (state) { state.toggleSearch1 == 1 ? state.toggleSearch1 = 0 : state.toggleSearch1 = 1 },
    [types.TOGGLE_SEARCH2] (state) { state.toggleSearch2 == 1 ? state.toggleSearch2 = 0 : state.toggleSearch2 = 1 },
    
    // login info
    [types.SET_USERTOKEN] (state, value) { state.userToken = value },
    [types.SET_USERNAME] (state, value) { state.userName = value },
    
    // popup info
    [types.SET_POPUPHEADER] (state, value) { state.popupHeader = value },
    [types.SET_POPUPBODY] (state, value) { state.popupBody = value },
    [types.SET_POPUPBUTTON] (state, value) { state.popupButton = value },
    [types.SET_POPUPRETURN] (state, value) { state.popupReturn = value },
    [types.SET_POPUPKIND] (state, value) { state.popupKind = value },
    [types.SET_POPUPFORMATID] (state, value) { state.popupFormatId = value },
    [types.SET_POPUPFORMATKIND] (state, value) { state.popupFormatKind = value },
    [types.SET_POPUPDATE] (state, value) { state.popupDate = value },
    [types.SET_POPUPDIFFID] (state, value) { state.popupDiffId = value },

    // metric info
    [types.SET_METRICID] (state, value) { state.metricId = value },

    [types.SET_DETAILCONDITION] (state, value) { state.detailcondition = value },
    [types.SET_DETAILSEARCHKEYWORD] (state, value) { state.detailsearchKeyword = value },
    [types.SET_DETAILCONDITION2] (state, value) { state.detailcondition2 = value },
    [types.SET_DETAILSEARCHKEYWORD2] (state, value) { state.detailsearchKeyword2 = value },


}

// 저장소 초기화
export default createStore(Vuex.Store, {
    state: state,
    mutations: mutations,
    getters: getters,
    actions: actions,

    plugins: [createPersistedState()],
})



