<template>

    <LNBPage title="Screen with LNB - Split 03" class="mg-auto">

        <div class="table-title mt32">
            <div class="table-title-header">Product</div>
        </div>

        <ui-table :paging-info="pagingInfo" :columns="columns" :items="items" editable>
            <template v-slot:cellview-mode="{ item }" >
                <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                    {{item.mode}}
                </lego-badge>
            </template>
            <template v-slot:celledit-mode="{ item }" >
                <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                    {{item.mode}}
                </lego-badge>
            </template>
            <template v-slot:celledit-email="{ item }" >
                <lego-text-field v-model="item.email" />
            </template>

        </ui-table>

        <template v-slot:side>
            <div class="page-side">
                <div class="page-side-title">
                    <span>SDSAP EAMS</span>
                    <lego-icon small type="picto">setting</lego-icon>
                </div>
                <div class="page-side-search">
                    <lego-text-field searchable value="Total 15" />
                </div>
                <div class="page-side-list">
                    <div v-for="(item, index) in sideList" :key="index"
                        class="page-side-list__item"
                    >
                        <span>{{item.name}}</span>
                        <span>{{item.position}}</span>
                    </div>
                </div>
            </div>
        </template>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBRightPage'

export default {
    name: 'lnb-split-03',
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
            pagingInfo : {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 17,
                totalItems: 163
            },
            columns: [
                {label: 'Name', key: "name", sortable: true, sortValue: "asc", filtable: false, alignRight: false, width: 20 },
                {label: 'Email', key: "email", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 25,
                    filterList: ["@tunivers.com","@samsung.com","Cockatoo","Richard's Pipit"] 
                },
                {label: 'Mode', key: "mode", sortable: false, filtable: true, filterValue:[], alignRight: false, width: 15,
                    filterList: ["Success","Error","Processing"]  },
                {label: 'Gender', key: "gender", sortable: false, filtable: false, alignRight: false, width: 15 },
                {label: 'Registrant', key: "registrant", sortable: true, sortValue: "asc", filtable: true, filterValue:[], alignRight: false, width: 15,
                    filterList: ["Cockatoo","Richard's Pipit"]  },
                {label: 'Size', key: "size", sortable: false, filtable: false, alignRight: true, width: 10 },
            ],
            items: [
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Processing', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
            ],
            sideList: [
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'},
                {name:'Gildong (GAildong.Hong)', position:'L2(Assistant Engineer)'}
            ]
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
    margin: 0 0 32px 0;
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
    margin-bottom: 0;
}
.table-checkbox {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
    margin: 20px 0;
}
.page-buttons {
    border-top-color: #cccccc;
    margin: 252px 0 0 0;
}
.page-side {
    width: 320px;
    display: flex;
    flex-flow: column nowrap;
    padding: 84px 32px 0;
}
.page-side-title {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.page-side-title span {
    font-size: 20px;
    font-weight: bold;
    margin-right: 8px;
}
.page-side-title .lego-icon {
    color: #A5A5A5;    
}
.page-side-search {
    margin-top: 16px;
}
.page-side-list {
    margin-top: 16px;
}
.page-side-list__item {
    display: flex;
    flex-flow: column nowrap;
    padding: 16px 0;
}
.page-side-list__item + .page-side-list__item {
    border-top: 1px solid #EAEAEA;
}
.page-side-list__item span + span {
    margin-top: 8px;
}
</style>