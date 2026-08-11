<template>

    <LNBPage title="Screen with LNB - Stack 06" class="mg-auto">

        <ui-form-box>

            <ui-form-row>
                <ui-form-item :columns=6 label="Lorem Ipsum" required left-label :label-width=140>
                    957383748267284703848327883738
                </ui-form-item>
                <ui-form-item :columns=6 label="Lorem Ipsum" required left-label :label-width=140>
                    General Transit
                </ui-form-item>
                <ui-form-item :columns=6 label="Lorem Ipsum" required left-label :label-width=140>
                    Regular Preventive Maintenace in October
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=6 label="Lorem" required left-label :label-width=140>
                    2019-05-20    13:56:13
                </ui-form-item>
                <ui-form-item :columns=6 label="Ipsum" required left-label :label-width=140>
                    sat, 27th Oct, 2018:23:00 - Sun
                </ui-form-item>
                <ui-form-item :columns=6 label="Lorem Ipsum" required left-label :label-width=140>
                    Supplier Discount
                </ui-form-item>
            </ui-form-row>

        </ui-form-box>

        <div class="ui-form-divider" />

        <ui-tab box no-action :tabs="tabs" class="mt8" />

        <div class="table-title mt32">
            <div class="table-title-header">In process <span style="color: #553CA5;">1</span></div>
            <div class="table-title-link">More<lego-icon xsmall>collapse_menu</lego-icon></div>
        </div>

        <ui-table :columns="columns" :items="items" no-info no-action >
            <template v-slot:cellview-mode="{ item }" >
                <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                    {{item.mode}}
                </lego-badge>
            </template>
        </ui-table>

        <ui-form-row space-between class="mt32">
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
import LNBPage from '../_Frame/LNBPage'

export default {
    name: 'lnb-stack-06',
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
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false }
            ],
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
    margin-right: 20px;
}
.table-title-sub {
    font-size: 14px;
}
.table-title-link {
    margin-left: auto;
}
.table-title-link .lego-icon {
    margin-left: 4px;
    transform: rotate(90deg);
    color: #CCCCCC;
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
</style>