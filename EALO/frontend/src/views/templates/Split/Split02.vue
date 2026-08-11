<template>

    <Page title="Screen without LNB - Split 02" class="mg-auto">

        <ui-container-box :columns=22 vertical class="page-tabs">
            <ui-tab box no-action :tabs="tabs" />
        </ui-container-box>

        <ui-container-box :columns=22 vertical align-center class="page-container">

            <ui-container-box :columns=20 horizontal align-center class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
                <span class="page-title__sub">
                    <lego-text-field searchable placeholder="Search" />
                </span>
            </ui-container-box>

            <ui-container-box :columns=20 horizontal class="page-main-area">

                <ui-container-box :columns=4 vertical class="page-main-lnb">

                    <ui-lnb title="Title" no-fix-width transparent>
                        <ui-lnb-menus :menus="badgeMenus" @selectMenu="selectMenu"/>
                    </ui-lnb>

                </ui-container-box>

                <ui-container-box :columns=16 vertical align-center class="page-main-table">

                    <ui-table checkable :paging-info="pagingInfo" :columns="columns" :items="items">
                        <template v-slot:control >Unit&nbsp;<b>KRW</b></template>
                        <template v-slot:cellview-mode="{ item }" >
                            <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                                {{item.mode}}
                            </lego-badge>
                        </template>
                    </ui-table>

                </ui-container-box>

            </ui-container-box>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'split-02',
    components: {
        Page
    },
    data: function() {
        return {
            value: 'A',
            dateValue: '',
            segmentValue: '2',
            radioValue: '1',
            textValue: '',
            checkValue: false,
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false }
            ],
            badgeMenus: [
                {   label:'LNB Menu1', key:'LNBmenu1', isSelected: false, badgeLabel: 'N',
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu2', key:'LNBmenu2', isSelected: false,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: false },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                {   label:'LNB Menu3', key:'LNBmenu3', isSelected: true,
                    menus: [
                        { label:'2depth Menu1', key:'2depthMenu1', isSelected: false },
                        { label:'2depth Menu2', key:'2depthMenu2', isSelected: true },
                        { label:'2depth Menu3', key:'2depthMenu3', isSelected: false },
                        { label:'2depth Menu4', key:'2depthMenu4', isSelected: false },
                    ]
                },
                { label:'LNB Menu4', key:'LNBmenu4', isSelected: false, badgeLabel: 99 },
                { label:'LNB Menu5', key:'LNBmenu5', isSelected: false, badgeLabel: 'N' }
            ],
            perPageItems : [
                {text: '10 Per page', value: 10},
                {text: '20 Per page', value: 20},
                {text: '30 Per page', value: 30}
            ],
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
            ]
        }
    },
    methods: {
        selectMenu(clickedMenu, clickedMenuSiblings){

            if (clickedMenu.isSelected && clickedMenu.menus) {
                this.releaseMenuSelection(clickedMenuSiblings);
                clickedMenu.isSelected = false;
            } else {
                this.releaseMenuSelection(clickedMenuSiblings);
                clickedMenu.isSelected = true;
            }
        },
        releaseMenuSelection(menus){
            menus.forEach(menu => {
                menu.isSelected = false;
                if(menu.menus) this.releaseMenuSelection(menu.menus);
            });
        }
    }
}
</script>

<style scoped>
.page-tabs {
    margin-top: 48px;
}
.page-container {
    margin: 0 0 32px;
    padding: 48px 80px;
    background-color: white;
}
.page-title {
    margin-bottom: 16px;
}
.page-title__label {
    font-size: 32px;
    font-weight: bold;
}
.page-title__sub {
    width: 208px;
    align-self: flex-end;
}
.page-main-area {
    border-top: 1px solid #CCCCCC;
}
.page-main-lnb {
    border-right: 1px solid #EAEAEA;
    background-color: #F7F7F7;
}
.page-main-table {
    padding: 32px 80px 24px;
}

</style>