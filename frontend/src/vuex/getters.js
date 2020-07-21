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

    getToggleSearch: state => state.toggleSearch ,

    getUserToken: state => state.userToken ,
    getUserName: state => state.userName  

}
