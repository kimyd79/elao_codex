<template>
    <div id="logformatresult">

      <div class="page-summary-title">Logformat 조회 결과</div>

      <!-- component :is="currentView"></component -->
      <UpdateLogformatForm :is="currentView" :format="format"></UpdateLogformatForm>   

      <ui-form-item :columns=20 align-right margin-right>
          <lego-button main v-on:click="clickUpdate">수정</lego-button>
          <lego-button main v-on:click="clickAdd">추가</lego-button>
          <lego-button main v-on:click="clickDelete">삭제</lego-button>
      </ui-form-item>    
      <div class="tb_box">
      <table class="page-summary-table">
          <thead>
              <tr>
                  <th>ID</th>
                  <th>제품명</th>
                  <th>포맷명</th>
                  <th>로그포맷</th>
                  <th>생성자</th>
                  <th>생성일시</th>
              </tr>
          </thead>
          <tbody id="list">
              <tr v-for="format_list in format_lists" :key="format_list" v-on:click="clickList(format_list)" :class="{'highlight': (format_list.format_id == selected_format_id) }">
                  <td>{{format_list.format_id}}</td>
                  <td>{{format_list.format_kind}}</td>
                  <td>{{format_list.format_name}}</td>
                  <td>{{format_list.format_strings}}</td>
                  <td>{{format_list.creator}}</td>
                  <td>{{format_list.created}}</td>
              </tr>
          </tbody>
      </table>
      </div>
    </div>

</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import AddLogformatForm from './AddLogformatForm';
import UpdateLogformatForm from './UpdateLogformatForm';

var urlStr = "http://127.0.0.1:8000/logformat/";

export default {
    name: 'LogformatResult',
    components: { 
      AddLogformatForm,
      UpdateLogformatForm,
 
    },
    data: function() {
      return {
        currentView : null,
        selected_format_id : null,
        format_lists : [],
        format : {format_id:'', format_kind:'', format_name:'', format_strings:'', creator:''},
      }
    },
    mounted() {
      EventBus.$on("searchFormat", this.getData);
      EventBus.$on("cancel", () => {
        this.currentView = null;
      });
      EventBus.$on("addFormat", (format) => {
        this.addData(format);
        this.currentView = null;

      });
      EventBus.$on("updateFormat", (format) => {
        this.updateData(format);
        this.currentView = null;
      });
    },

    methods: {
      getData: function(format_kind) {
        //axios.get( 'http://127.0.0.1:8000/logformat/?format_kind='+format_kind)
        axios.get( urlStr + '?format_kind='+format_kind)
        .then((response) => {
                console.log(response);
                this.format_lists = response.data.results;
        })
        .catch((ex) => {
          console.log('getData failed', ex);
        })
      },
      getDataOne: function(id) {
        //axios.get( 'http://127.0.0.1:8000/logformat/'+id)
        axios.get( urlStr + id)
        .then((response) => {
                console.log(response);
                this.format = response.data.results;
        })
        .catch((ex) => {
          console.log('getData failed', ex);
        })
      },
      deleteData: function(format) {
        //axios.delete( 'http://127.0.0.1:8000/logformat/'+format.format_id)
        axios.delete( urlStr + format.format_id)
        .then((response) => {
                console.log(response);
                this.getData(format.format_kind);
        })
        .catch((ex) => {
          console.log('deleteData failed', ex);
        })
      },
      addData: function(format) {
        //axios.post( 'http://127.0.0.1:8000/logformat/', format)
        axios.post( urlStr, format)
        .then((response) => {
                console.log(response);
                this.getData(format.format_kind);
        })
        .catch((ex) => {
          console.log('addData failed', ex);
        })
      },
      updateData: function(format) {
        //axios.put('http://127.0.0.1:8000/logformat/'+format.format_id+'/', format)
        axios.put( urlStr + format.format_id+'/', format)
        .then((response) => {
                console.log(response);
                this.getData(format.format_kind);
        })
        .catch((ex) => {
          console.log('updateData failed', ex);
        })
      },
      clickList: function(format_list) {
        this.selected_format_id = format_list.format_id;
        this.format.format_id = format_list.format_id;
        this.format.format_kind = format_list.format_kind;
        this.format.format_name = format_list.format_name;
        this.format.format_strings = format_list.format_strings;
        this.format.creator = format_list.creator;
        EventBus.$emit("searchFormatDetail", format_list.format_kind);
        console.log(this.format_kind);
        console.log("click ID : " + format_list.format_id);

      },
      clickDelete: function() {
         if ( !this.selected_format_id ) {
          alert('선택된 Logformat이 없습니다.');
        }else{
          if ( confirm('Logformat ID : ' + this.selected_format_id +' 를 삭제하시겠습니까?'))
          {
            this.deleteData(this.format);
          }
        }
      },
      clickAdd: function() {
        this.currentView = 'AddLogformatForm';
      },
      clickSave: function() {
        this.checkSelectedFormatIdNull(); 
        console.log("click ID : " + this.selected_format_id);
      },
      clickUpdate: function() {
        if ( !this.selected_format_id ) {
          alert('선택된 Logformat이 없습니다.');
        }else{
          alert('선택된 Logformat ID는 ' + this.selected_format_id + ' 입니다.');
          //EventBus.$emit("updateFormat", this.format);
          this.currentView = 'updateLogformatForm';
        }
        
        console.log("click ID : " + this.selected_format_id);
      },
      checkSelectedFormatIdNull() {
        if ( !this.selected_format_id ) {
          alert('선택된 Logformat이 없습니다.');
        }else{
          alert('선택된 Logformat ID는 ' + this.selected_format_id + ' 입니다.');
        }
      }
    }
};
</script>

<style scoped>
.highlight {
  background-color: yellow;
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
  max-height:200px;
  overflow-y:auto;
}
.page-summary-table {
  border-spacing: 0;
  width:100%; 
  height:20px;
}
.page-summary-table thead th {
  height: 28px;
  border-top: 1px solid #eaeaea;
  font-weight: normal;
  background-color: #f7f7f7;
}
.page-summary-table thead th + th {
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
.page-summary-table tbody td + td {
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
