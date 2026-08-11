import * as types from './mutation_types'

export default {
    
    setProjectName({commit}, value) { commit(types.SET_PROJECTNAME, value) },
    setProjectDescription({commit}, value) { commit(types.SET_PROJECTDESCRIPTION, value) },
    setFileNames({commit}, value) { commit(types.SET_FILENAMES, value) },
    setLogFormat({commit}, value) { commit(types.SET_LOGFORMAT, value) },
    setProjectID({commit}, value) { commit(types.SET_PROJECTID, value) },
    setLogFileID({commit}, value) { commit(types.SET_LOGFILEID, value) },

    setProjectFiles({commit}, value) { commit(types.SET_PROJECTFILES, value) },
    setProjectServers({commit}, value) { commit(types.SET_PROJECTSERVERS, value) },
    setProjectServers2({commit}, value) { commit(types.SET_PROJECTSERVERS2, value) },

    setGlobalFromDate({commit}, value) { commit(types.SET_GLOBAL_FROMDATE, value) },
    setGlobalToDate({commit}, value) { commit(types.SET_GLOBAL_TODATE, value) },
    setGlobalFromTime({commit}, value) { commit(types.SET_GLOBAL_FROMTIME, value) },
    setGlobalToTime({commit}, value) { commit(types.SET_GLOBAL_TOTIME, value) },

    setGlobalYTps({commit}, value) { commit(types.SET_GLOBAL_Y_TPS, value) },
    setGlobalYRequest({commit}, value) { commit(types.SET_GLOBAL_Y_REQUEST, value) },
    setGlobalYDuration({commit}, value) { commit(types.SET_GLOBAL_Y_DURATION, value) },
    setGlobalYRequestSBar({commit}, value) { commit(types.SET_GLOBAL_Y_REQUEST_SBAR, value) },

    setGlobalYTps2({commit}, value) { commit(types.SET_GLOBAL_Y_TPS2, value) },
    setGlobalYRequest2({commit}, value) { commit(types.SET_GLOBAL_Y_REQUEST2, value) },
    setGlobalYDuration2({commit}, value) { commit(types.SET_GLOBAL_Y_DURATION2, value) },
    setGlobalYRequestSBar2({commit}, value) { commit(types.SET_GLOBAL_Y_REQUEST_SBAR2, value) },

    setFromDate({commit}, value) { commit(types.SET_FROMDATE, value) },
    setToDate({commit}, value) { commit(types.SET_TODATE, value) },
    setFromTime({commit}, value) { commit(types.SET_FROMTIME, value) },
    setToTime({commit}, value) { commit(types.SET_TOTIME, value) },
    setFromTimeTaken({commit}, value) { commit(types.SET_FROMTIMETAKEN, value) },
    setToTimeTaken({commit}, value) { commit(types.SET_TOTIMETAKEN, value) },
    setCondition({commit}, value) { commit(types.SET_CONDITION, value) },
    setSearchKeyword({commit}, value) { commit(types.SET_SEARCHKEYWORD, value) },
    setExcludeSearch({commit}, value) { commit(types.SET_EXCLUDESEARCH, value) },

    setFromDate2({commit}, value) { commit(types.SET_FROMDATE2, value) },
    setToDate2({commit}, value) { commit(types.SET_TODATE2, value) },
    setFromTime2({commit}, value) { commit(types.SET_FROMTIME2, value) },
    setToTime2({commit}, value) { commit(types.SET_TOTIME2, value) },
    setFromTimeTaken2({commit}, value) { commit(types.SET_FROMTIMETAKEN2, value) },
    setToTimeTaken2({commit}, value) { commit(types.SET_TOTIMETAKEN2, value) },
    setCondition2({commit}, value) { commit(types.SET_CONDITION2, value) },
    setSearchKeyword2({commit}, value) { commit(types.SET_SEARCHKEYWORD2, value) },
    setExcludeSearch2({commit}, value) { commit(types.SET_EXCLUDESEARCH2, value) },

    //statistic detailpopup
    setDetailCondition({commit}, value) { commit(types.SET_DETAILCONDITION, value) },
    setDetailSearchKeyword({commit}, value) { commit(types.SET_DETAILSEARCHKEYWORD, value) },
    setDetailCondition2({commit}, value) { commit(types.SET_DETAILCONDITION2, value) },
    setDetailSearchKeyword2({commit}, value) { commit(types.SET_DETAILSEARCHKEYWORD2, value) },
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
    setPopupDate({commit}, value) { commit(types.SET_POPUPDATE, value) },

    setMetricId({commit}, value) { commit(types.SET_METRICID, value) },

    setCurrentMenu({commit}, value) { commit(types.SET_CURRENTMENU, value) }
}
