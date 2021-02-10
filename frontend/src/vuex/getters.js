export default {

    getProjectName: state => state.projectName ,
    getProjectDescription: state => state.projectDescription ,
    getFileNames: state => state.fileNames ,
    getLogFormat: state => state.logFormat ,
    getProjectID: state => state.projectID,
    getLogFileID: state => state.logFileID,

    getFromDate: state => state.fromDate ,
    getToDate: state => state.toDate ,
    getFromTime: state => state.fromTime ,
    getToTime: state => state.toTime ,
    getFromTimeTaken: state => state.fromTimeTaken ,
    getToTimeTaken: state => state.toTimeTaken ,
    getCondition: state => state.condition ,
    getSearchKeyword: state => state.searchKeyword ,
    // statistic detailpopup
    getDetailCondition: state => state.detailcondition ,
    getDetailSearchKeyword: state => state.detailsearchKeyword ,   
    getThreshold: state => state.threshold ,

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
    
    getMetricId: state => state.MetricId

}
