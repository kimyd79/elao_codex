<template>

    <LNBPage title="Screen with LNB - Stack 11" class="mg-auto">

        <ui-form-box>
            <ui-form-row>
                <ui-form-item :columns=20 label="보고서명" required left-label :label-width=224>
                    <lego-text-field>
                        [개발계획승인] 005 고휘도 LED 헤드램프 추가개발 (램프 리어램프) W사용
                    </lego-text-field>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=9 label="등록자" left-label :label-width=224>
                    <span class="fs16">김관리 수석</span>
                </ui-form-item>
                <ui-form-item :columns=10 label="등록일" left-label :label-width=224>
                    <span class="fs16">2019.02.19</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=9 label="상태" left-label :label-width=224>
                    <span class="fs16">작성</span>
                </ui-form-item>
                <ui-form-item :columns=10 label="승인일" left-label :label-width=224>
                    <span class="fs16">2019.02.21</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row space-between>
                <ui-form-item :columns=9 label="대상 프로젝트" left-label :label-width=224>
                    <lego-text-field>
                        005 고휘도 LED 헤드램프 추가개발 (램프 리어램프) W사용
                    </lego-text-field>
                </ui-form-item>
                <ui-form-item :columns=10 label="보고서 유형" left-label :label-width=224>
                    <lego-text-field>
                        Gate 리뷰
                    </lego-text-field>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=20 label="보고내용" left-label :label-width=224>
                    <lego-text-field textarea rows="4">
                        [개발계획승인] 005 고휘도 LED 헤드램프 추가개발 (램프 리어램프) W사용
                        [개발계획승인] 005 고휘도 LED 헤드램프 추가개발 (램프 리어램프) W사용
                        [개발계획승인] 005 고휘도 LED 헤드램프 추가개발 (램프 리어램프) W사용
                        [개발계획승인] 005 고휘도 LED 헤드램프 추가개발 (램프 리어램프) W사용
                    </lego-text-field>
                </ui-form-item>
            </ui-form-row>
            
            <ui-form-row>
                <ui-form-item :columns=20 label="첨부파일" left-label :label-width=224>
                    
                    <ui-table checkable :columns="columns" :items="items" no-info editable>
                        <template v-slot:celledit-regdate="{ item }" >
                            <lego-text-field v-model="item.regdate" />
                        </template>
                        <template v-slot:celledit-servicename1="{ item }" >
                            <lego-text-field v-model="item.servicename1" />
                        </template>
                        <template v-slot:celledit-servicename2="{ item }" >
                            <lego-text-field v-model="item.servicename2" />
                        </template>
                        <template v-slot:celledit-servicename3="{ item }" >
                            <lego-text-field v-model="item.servicename3" />
                        </template>
                        <template v-slot:celledit-servicename4="{ item }" >
                            <lego-text-field v-model="item.servicename4" />
                        </template>
                        <template v-slot:summary>
                            <div class="table-checkbox">
                                <lego-checkbox v-model="checkValue" small>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</lego-checkbox>
                            </div>
                        </template>
                    </ui-table>

                </ui-form-item>
            </ui-form-row>

        </ui-form-box>

        <ui-form-row space-between class="page-button-area">
            <div>
                <lego-button large>List</lego-button>
            </div>
            <div>
                <lego-button large>Cancel</lego-button>
                <lego-button large main>Save</lego-button>
            </div>
        </ui-form-row>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBLightPage'

export default {
    name: 'lnb-stack-11',
    components: {
        LNBPage
    },
    data: function() {
        return {
            value: 'A',
            dateValue: '',
            segmentValue: '2',
            radioValue: '1',
            textValue: '',
            checkValue: false,
            columns: [
                {label: 'Reg. Date', key: "regdate", alignCenter: true, width: 20},
                {label: 'Service name', key: "servicename1", alignCenter: true, width: 20 },
                {label: 'Service name', key: "servicename2", alignCenter: true, width: 20 },
                {label: 'Service name', key: "servicename3", alignCenter: true, width: 20 },
                {label: 'Service name', key: "servicename4", alignCenter: true, width: 20 },
            ],
            items: [
                {regdate:'-', servicename1:'-', servicename2:'-', servicename3:'-', servicename4:'-', isSelected: false}
            ],
        }
    },
    computed : {
        dropdownItems() {
            let rtn = [];
            rtn.push({value:'A',text:'Lorem Ipsum'});
            rtn.push({value:'B',text:'Lorem Ipsum'});
            return rtn;
        }
    }
}
</script>

<style scoped>
.mt0 {
    margin-top: 0px;
}
.ui-form-divider {
    width: 100%;
    height: 1px;
    background-color: #EAEAEA;
    margin: 32px 0;
}
.table-title {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-end;
    margin-bottom: 16px;
}
.table-title-header {
    font-size: 20px;
    font-weight: bold;
    margin-right: 20px;
}
.table-title-sub {
    font-size: 14px;
}
.table-checkbox {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
    margin: 20px 0;
}
.page-button-area {
    border-top: 1px solid #cccccc;
    padding-top: 24px;
}
.fs16 {
    font-size: 16px;
}
</style>