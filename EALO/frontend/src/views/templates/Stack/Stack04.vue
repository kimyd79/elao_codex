<template>

    <Page title="Screen without LNB - Stack 04" class="mg-auto">

        <ui-container-box :columns=20 vertical class="mt32">

            <div class="page-title">
                <span class="page-title__label">Anlytic Model</span>
                <span class="page-title__sub">
                    Menu1 > LNB Menu1 > <em>LNB Sub Menu1</em>
                </span>
            </div>

            <ui-container-box :columns=20 horizontal>
                <ui-card v-for="(item, index) in cardItems" :key="index"
                    :columns=5 :height=200
                >
                    <ui-card-item header>
                        Lorem Ipsum
                    </ui-card-item>
                    <ui-card-item sub fill-gap>
                        Lorem Ipsum is simple dummy text
                    </ui-card-item>
                    <ui-card-item action>
                        Lorem Ipsum
                    </ui-card-item>
                </ui-card>
            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=24 vertical align-center class="page-body-area">

            <ui-container-box :columns=18 vertical class="page-info-area">

                <div class="page-info-title">
                    <span class="page-info-title__label">In process</span>
                    <span class="page-info-title__count">3</span>
                </div>

                <div class="page-info-main">
                    <div class="page-info-main__item">
                        <span class="page-info-main__item-name">Task ID</span>
                        <span class="page-info-main__item-desc">RCA_EQP_190425_191225</span>
                        <div class="page-info-main__item-button">
                            <lego-button>Summary</lego-button>
                        </div>
                    </div>

                    <div class="page-info-main__item">
                        <span class="page-info-main__item-name">Model</span>
                        <span class="page-info-main__item-desc">RCA-Equipment</span>
                    </div>

                    <div class="page-info-main__item">
                        <span class="page-info-main__item-name">Data</span>
                        <span class="page-info-main__item-desc">TRACE001_DATA</span>
                    </div>

                    <div class="page-info-main__progress">
                        <span class="page-info-main__progress-info">3h 17m in Process</span>
                        <lego-progress progress-type="line" size="large" determinate :value=50 message="50%" message-direction="right" :width=672 />
                        <div class="page-info-main__item-button">
                            <lego-button>Summary</lego-button>
                        </div>
                    </div>
                </div>

                <div class="page-info-more">
                    <span class="page-info-more__label">more</span>
                    <span class="page-info-more__count">3</span>
                    <span class="page-info-more__icon"><lego-icon xsmall>expand_menu</lego-icon></span>
                </div>

            </ui-container-box>

            <ui-container-box :columns=18 vertical class="page-table-area">

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

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'stack-04',
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
            cardItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
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
    }
}
</script>

<style scoped>
.page-title {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-end;
    justify-content: space-between;
    
    margin-top: 16px;
    margin-bottom: 24px;
}
.page-title__label {
    font-size: 32px;
    font-weight: bold;
}
.page-body-area {
    margin-top: 60px;
    padding: 48px 0 80px;
    background-color: white;
}
.page-table-area {
    align-self: center;
    margin-top: 48px;
    padding-top: 32px;
}

.page-info-title,
.page-info-main {
    display: flex;
    flex-flow: row nowrap;
}
.page-info-title__label,
.page-info-title__count {
    font-size: 20px;
}
.page-info-title {
    padding-bottom: 24px;
    border-bottom: 1px solid #CCCCCC;
}
.page-info-title__count {
    color: #553CA5;
    margin-left: 16px;
}
.page-info-main {
    margin-top: 48px;
    padding-bottom: 24px;
    border-bottom: 1px solid #EAEAEA;
}
.page-info-main__item {
    width: 224px;

    display: flex;
    flex-flow: column nowrap;
    padding-left: 16px;
}
.page-info-main__item + .page-info-main__item {
    margin-left: 16px;
}
.page-info-main__item-desc {
    font-size: 12px;
    color: #767676;
    margin-top: 4px;
}
.page-info-main__item-button {
    margin-top: 12px;
}
.page-info-main__progress {
    flex-grow: 1;
    margin-left: 16px;
    padding-left: 16px;
}
.page-info-main__progress-info {
    display: block;
    margin-bottom: 4px;
}

.page-info-more {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
    padding-top: 12px;
}
.page-info-more__count,
.page-info-more__icon {
    margin-left: 4px;
}
.page-info-more__count {
    color: #553CA5;
}
</style>