import Vue from 'vue'
import Vuex from 'vuex'

import getters from './getters'
import actions from './actions'
import * as types from './mutation_types'

Vue.use(Vuex)

// state
const state = {
    
    // common info
    projectName: '',
    projectDescription: '',
    fileNames: '',
    logFormat: '',

    projectID: '',
    logFileID: '',

    // search info   
    fromDate: '',
    toDate: '',
    fromTime: '',
    toTime: '',
    fromTimeTaken: '',
    toTimeTaken: '',
    condition: '',
    searchKeyword: '',

    // check
    toggleSearch: '0',  //  0 or 1 변경사항 확인용
    
    //login info
    userToken: '',
    userName: 'Not logged in', 
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

    // search info
    [types.SET_FROMDATE] (state, value) { state.fromDate = value },
    [types.SET_TODATE] (state, value) { state.toDate = value },
    [types.SET_FROMTIME] (state, value) { state.fromTime = value },
    [types.SET_TOTIME] (state, value) { state.toTime = value },
    [types.SET_FROMTIMETAKEN] (state, value) { state.fromTimeTaken = value },
    [types.SET_TOTIMETAKEN] (state, value) { state.toTimeTaken = value },
    [types.SET_CONDITION] (state, value) { state.condition = value },
    [types.SET_SEARCHKEYWORD] (state, value) { state.searchKeyword = value },

    [types.TOGGLE_SEARCH] (state) { state.toggleSearch == 1 ? state.toggleSearch = 0 : state.toggleSearch = 1 },
    
    //login info
    [types.SET_USERTOKEN] (state, value) { state.userToken = value },
    [types.SET_USERNAME] (state, value) { state.userName = value },

}

// 저장소 초기화
export default new Vuex.Store({
    state: state,
    mutations: mutations,
    getters: getters,
    actions: actions
})
