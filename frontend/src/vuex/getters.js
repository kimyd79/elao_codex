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
      
    getPopupHeader: state => state.PopupHeader,
    getPopupBody: state => state.PopupBody,
    getPopupButton: state => state.PopupButton,
    getPopupReturn: state => state.PopupReturn,
    getPopupKind: state => state.PopupKind,
    getPopupFormatId: state => state.PopupFormatId,
    getPopupFormatKind: state => state.PopupFormatKind,
    
    getMetricId: state => state.MetricId

}
