<template>

    <Page title="Screen without LNB - Stack 02" class="mg-auto">

        <ui-container-box :columns=22 vertical class="mt32">

            <ui-tab box :tabs="tabs" no-action />

        </ui-container-box>

        <ui-container-box :columns=22 vertical class="page-body-area">

            <div class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
                <span class="page-title__sub">
                    Menu1 > LNB Menu1 > <em>LNB Sub Menu1</em>
                </span>
            </div>

            <div class="page-body-form">
                <span class="page-body-form__title">Lorem Ipsum</span>
                <ui-form-box class="page-body-form__content">
                    <ui-form-row space-between>
                        <ui-form-item :columns=8 label="Lorem Ipsum" required left-label >
                            Lorem Ipsum is simply dummy text
                        </ui-form-item>
                        <ui-form-item :columns=10 label="Lorem Ipsum" required left-label >
                            Lorem Ipsum is simply dummy text
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row space-between>
                        <ui-form-item :columns=8 label="Lorem Ipsum" required left-label >
                            Lorem Ipsum is simply dummy text
                        </ui-form-item>
                        <ui-form-item :columns=10 label="Lorem Ipsum" required left-label >
                            Lorem Ipsum is simply dummy text
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=6 label="Lorem Ipsum" required left-label >
                            <lego-segment-wrapper solid primary v-model="segmentValue">
                                <lego-segment-button value="1">Lorem</lego-segment-button>
                                <lego-segment-button value="2">Lorem</lego-segment-button>
                            </lego-segment-wrapper>
                        </ui-form-item>
                        <ui-form-item :columns=3>
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                    </ui-form-row>

                    <ui-form-row>
                        <ui-form-item :columns=6 label="Lorem Ipsum" required left-label >
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                        <ui-form-item :columns=7>
                            * Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        </ui-form-item>
                    </ui-form-row>

                </ui-form-box>
            </div>

            <ui-container-box :columns=18 vertical class="page-table-area">

                <div class="ui-tab-lite">
                    <div class="ui-tab-lite-item ui-tab-lite-item--selected">Tab_1</div>
                    <div class="ui-tab-lite-item">Tab_2</div>
                    <div class="ui-tab-lite-item">Tab_3</div>
                    <div class="ui-tab-lite-item">Tab_4</div>
                </div>

                <div class="page-table-control">
                    <div class="page-table-control__info">
                        <span class="page-table-control__info-total">
                            Total <b>{{pagingInfo.totalItems}}</b>
                        </span>
                        <lego-dropdown class="lego-table__counter__per-page"
                                :items="perPageItems" v-model="pagingInfo.rowsPerPage" />
                    </div>
                    <div class="page-table-control__buttons">
                        <lego-button small>Lorem</lego-button>
                        <lego-button small>Lorem</lego-button>
                        <lego-button small>Lorem</lego-button>
                        <lego-icon-button small>more</lego-icon-button>
                    </div>
                </div>

                <div class="page-table-header">
                    <span class="page-table-header__item fg11">Title</span>
                    <span class="page-table-header__item fg2">Lorem Ipsum</span>
                    <span class="page-table-header__item fg3">Requirement</span>
                    <span class="page-table-header__item fg2">Date</span>
                </div>

                <div class="page-table-body">
                    <div v-for="(item, index) in tableItems" :key="index"
                        class="page-table-body__item"
                    >
                        <div class="page-table-body__item-column fg11">
                            <ui-list>
                                <template v-slot:thumbnail>
                                    <ui-list-thumbnail :width=80 :height=80 />
                                </template>
                                <template v-slot:default>
                                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                                    <ui-list-item body>
                                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                                        industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                                    </ui-list-item>
                                </template>
                            </ui-list>
                        </div>
                        <div class="page-table-body__item-column fg2">
                            Lorem Ipsum
                        </div>
                        <div class="page-table-body__item-column fg3">
                            Lorem Ipsum
                        </div>
                        <div class="page-table-body__item-column fg2">
                            2019.03.02
                        </div>
                    </div>
                </div>

                <lego-pagination :pagination="pagingInfo" class="mt24"/>

            </ui-container-box>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'stack-02',
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
            tableItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
                { label: "5" },
                { label: "6" },
                { label: "7" },
            ]
        }
    }
}
</script>

<style scoped>
.page-body-area {
    padding: 48px 80px;
    background-color: white;
}
.page-title {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-end;
    justify-content: space-between;
    
    padding-bottom: 18px;
    border-bottom: 1px solid #CCCCCC;
}
.page-title__label {
    font-size: 32px;
    font-weight: bold;
}
.page-title__search {
    width: 208px;
}
.page-body-form {
    padding-top: 32px;
}
.page-body-form__title {
    display: block;
    font-size: 20px;
    font-weight: bold;
    margin: 16px 0 24px 32px;
}
.page-body-form__content {
    padding: 0 0 0 64px;
}

.page-table-area {
    align-self: center;
    margin-top: 60px;
    border-top: 1px solid #CCCCCC;
}
.page-table-control,
.page-table-control__info,
.page-table-control__info-total,
.page-table-control__buttons {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.page-table-control {
    justify-content: space-between;
}
.page-table-control__info-total {
    padding-right: 12px;
    margin-right: 12px;
    border-right: 1px solid #A5A5A5;
}
.page-table-control__info-total b {
    margin-left: 4px;
}
.page-table-header {
    display: flex;
    flex-flow: row nowrap;
    padding: 16px;
    border-top: 1px solid #EAEAEA;
    border-bottom: 1px solid #A5A5A5;
    margin-top: 16px;
}
.fg11 {
    flex-grow: 11;
    flex-basis: 10px;
}
.fg3 {
    flex-grow: 3;
    flex-basis: 10px;
}
.fg2 {
    flex-grow: 2;
    flex-basis: 10px;
}
.page-table-body {
    display: flex;
    flex-flow: column nowrap;
}
.page-table-body__item {
    display: flex;
    flex-flow: row nowrap;
    padding: 16px;
    border-bottom: 1px solid #EAEAEA;
}
.page-table-body__item-column {
    display: flex;
    align-items: center;
}

.ui-tab-lite {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;

    padding: 40px 0;
}
.ui-tab-lite-item {
    display: flex;
    justify-content: center;
    align-items: center;

    height: 36px;
    width: 160px;

    background-color: white;
    border-radius: 3px;

    font-size: 14px;
}
.ui-tab-lite-item:hover {
    cursor: pointer;
}
.ui-tab-lite-item--selected {
    color: #553CA5;
    font-weight: bold;
    background-color: rgba(85,60,165,0.1);
}
.ui-tab-lite-item + .ui-tab-lite-item {
    margin-left: 8px;
}
</style>