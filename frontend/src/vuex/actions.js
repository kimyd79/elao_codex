import * as types from './mutation_types'

export default {
    
    setProjectName({commit}, value) { commit(types.SET_PROJECTNAME, value) },
    setProjectDescription({commit}, value) { commit(types.SET_PROJECTDESCRIPTION, value) },
    setFileNames({commit}, value) { commit(types.SET_FILENAMES, value) },
    setLogFormat({commit}, value) { commit(types.SET_LOGFORMAT, value) },
    setProjectID({commit}, value) { commit(types.SET_PROJECTID, value) },
    setLogFileID({commit}, value) { commit(types.SET_LOGFILEID, value) },

    setFromDate({commit}, value) { commit(types.SET_FROMDATE, value) },
    setToDate({commit}, value) { commit(types.SET_TODATE, value) },
    setFromTime({commit}, value) { commit(types.SET_FROMTIME, value) },
    setToTime({commit}, value) { commit(types.SET_TOTIME, value) },
    setFromTimeTaken({commit}, value) { commit(types.SET_FROMTIMETAKEN, value) },
    setToTimeTaken({commit}, value) { commit(types.SET_TOTIMETAKEN, value) },
    setCondition({commit}, value) { commit(types.SET_CONDITION, value) },
    setSearchKeyword({commit}, value) { commit(types.SET_SEARCHKEYWORD, value) },
    
    setToggleSearch({commit}) { commit(types.TOGGLE_SEARCH) },
}