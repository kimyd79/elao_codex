<template>

    <Page title="Screen without LNB - Split 03" class="mg-auto">

        <ui-container-box :columns=24 vertical align-center class="page-container">

            <ui-container-box :columns=22 horizontal align-center class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
                <span class="page-title__sub">
                    <lego-text-field searchable placeholder="Search" />
                </span>
            </ui-container-box>

            <ui-container-box :columns=22 vertical class="page-main-area">

                <ui-container-box :columns=20 horizontal class="page-table-area">

                <div class="page-main-table page-main-table__left">

                    <ui-table checkable no-paging no-bottom-border :paging-info="pagingInfo" :columns="columns" :items="items">
                        <template v-slot:action-left>
                            <lego-button small>Modify</lego-button>
                            <lego-button small>Delete</lego-button>
                        </template>
                        <template v-slot:action-right><div /></template>
                    </ui-table>

                </div>

                <div class="page-main-table__move">

                    <div class="page_main-table__move-button">
                        <lego-icon medium>next</lego-icon>
                    </div>
                    <div class="page_main-table__move-button">
                        <lego-icon medium>previous</lego-icon>
                    </div>

                </div>

                <div class="page-main-table page-main-table__right">

                    <ui-table checkable no-action no-paging no-bottom-border :paging-info="pagingInfo" :columns="columns" :items="rightItems" />

                </div>

                </ui-container-box>

                <ui-container-box :columns=20 horizontal class="page-button-area">
                    <lego-button large>Delete</lego-button>
                    <lego-button large main>Save</lego-button>
                </ui-container-box>

            </ui-container-box>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'split-01',
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
                {label: 'Name', key: "name", sortable: true, sortValue: "asc", filtable: false, alignRight: false, width: 25 },
                {label: 'Email', key: "email", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 35,
                    filterList: ["@tunivers.com","@samsung.com","Cockatoo","Richard's Pipit"] 
                },
                {label: 'Gender', key: "gender", sortable: false, filtable: false, alignRight: false, width: 15 },
                {label: 'Registrant', key: "registrant", sortable: true, sortValue: "asc", filtable: true, filterValue:[], alignRight: false, width: 25,
                    filterList: ["Cockatoo","Richard's Pipit"]  }
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
            rightItems: [
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
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
.page-container {
    margin: 48px 0 32px;
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
    padding: 0 80px 48px;
    background-color: white;
}
.page-main-table {
    display: flex;
    width: 772px;
    padding: 32px 16px;
    margin-top: 48px;
}
.page-main-table__right {
    padding-top: 72px;
}
.page-main-table__move {
    display: flex;
    flex-flow: column nowrap;
    justify-content: center;
    align-items: center;

    padding: 0 8px;
    border-left: 1px solid #EAEAEA;
    border-right: 1px solid #EAEAEA;
}
.page_main-table__move-button {
    width: 32px;
    height: 74px;

    display: flex;
    align-items: center;

    background-color: #F7F7F7;
}
.page_main-table__move-button + .page_main-table__move-button {
    margin-top: 8px;
}
.page_main-table__move-button:hover {
    cursor: pointer;
}
.page-button-area {
    border-top: 1px solid #CCCCCC;
    padding-top: 24px;
    justify-content: flex-end;
}

</style>