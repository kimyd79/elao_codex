export default {

    getProjectName: state => state.projectName ,
    getProjectDescription: state => state.projectDescription ,
    getFileNames: state => state.fileNames ,
    getLogFormat: state => state.logFormat ,
    getProjectID: state => state.projectID,
    getLogFileID: state => state.logFileID,

    getGlobalFromDate: state => state.global_fromDate ,
    getGlobalToDate: state => state.global_toDate ,
    getGlobalFromTime: state => state.global_fromTime ,
    getGlobalToTime: state => state.global_toTime ,

    getGlobalYTps: state => state.global_Y_tps ,
    getGlobalYRequest: state => state.global_Y_request ,
    getGlobalYDuration: state => state.global_Y_duration ,
    getGlobalYRequestSBar: state => state.global_Y_request_sbar ,

    getGlobalYTps2: state => state.global_Y_tps2 ,
    getGlobalYRequest2: state => state.global_Y_request2 ,
    getGlobalYDuration2: state => state.global_Y_duration2 ,
    getGlobalYRequestSBar2: state => state.global_Y_request_sbar2 ,

    getFromDate: state => state.fromDate ,
    getToDate: state => state.toDate ,
    getFromTime: state => state.fromTime ,
    getToTime: state => state.toTime ,
    getFromTimeTaken: state => state.fromTimeTaken ,
    getToTimeTaken: state => state.toTimeTaken ,
    getCondition: state => state.condition ,
    getSearchKeyword: state => state.searchKeyword ,
    getExcludeSearch: state => state.excludeSearch,

    getFromDate2: state => state.fromDate2 ,
    getToDate2: state => state.toDate2 ,
    getFromTime2: state => state.fromTime2 ,
    getToTime2: state => state.toTime2 ,
    getFromTimeTaken2: state => state.fromTimeTaken2 ,
    getToTimeTaken2: state => state.toTimeTaken2 ,
    getCondition2: state => state.condition2 ,
    getSearchKeyword2: state => state.searchKeyword2 ,
    getExcludeSearch2: state => state.excludeSearch2,

    // statistic detailpopup
    getDetailCondition: state => state.detailcondition ,
    getDetailSearchKeyword: state => state.detailsearchKeyword ,   
    getThreshold: state => state.threshold ,

    // statistic detailpopup
    getDetailCondition2: state => state.detailcondition2 ,
    getDetailSearchKeyword2: state => state.detailsearchKeyword2 ,   

    getToggleSearch: state => state.toggleSearch ,
    getToggleSearch1: state => state.toggleSearch1 ,
    getToggleSearch2: state => state.toggleSearch2 ,

    getUserToken: state => state.userToken ,
    getUserName: state => state.userName ,
      
    getPopupHeader: state => state.popupHeader,
    getPopupBody: state => state.popupBody,
    getPopupButton: state => state.popupButton,
    getPopupReturn: state => state.popupReturn,
    getPopupKind: state => state.popupKind,
    getPopupFormatId: state => state.popupFormatId,
    getPopupFormatKind: state => state.popupFormatKind,
    getPopupDate: state => state.popupDate,
    getPopupDiffId: state => state.popupDiffId,
    
    getMetricId: state => state.MetricId

}
