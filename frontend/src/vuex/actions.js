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
    //statistic detailpopup
    setDetailCondition({commit}, value) { commit(types.SET_DETAILCONDITION, value) },
    setDetailSearchKeyword({commit}, value) { commit(types.SET_DETAILSEARCHKEYWORD, value) },
    setThreshold({commit}, value) { commit(types.SET_THRESHOLD, value) },
    
    setToggleSearch({commit}) { commit(types.TOGGLE_SEARCH) },
    setToggleSearch1({commit}) { commit(types.TOGGLE_SEARCH1) },
    setToggleSearch2({commit}) { commit(types.TOGGLE_SEARCH2) },
    
    setUserToken({commit}, value) { commit(types.SET_USERTOKEN, value) },
    setUserName({commit}, value) { commit(types.SET_USERNAME, value) },
    
    setPopupHeader({commit}, value) { commit(types.SET_POPUPHEADER, value) },
    setPopupBody({commit}, value) { commit(types.SET_POPUPBODY, value) },
    setPopupButton({commit}, value) { commit(types.SET_POPUPBUTTON, value) },
    setPopupRetrun({commit}, value) { commit(types.SET_POPUPRETURN, value) },
    setPopupKind({commit}, value) { commit(types.SET_POPUPKIND, value) },
    setPopupFormatId({commit}, value) { commit(types.SET_POPUPFORMATID, value) },
    setPopupFormatKind({commit}, value) { commit(types.SET_POPUPFORMATKIND, value) },
}
