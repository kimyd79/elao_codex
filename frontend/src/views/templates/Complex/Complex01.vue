<template>

    <Page title="Screen without LNB - Complex 01" class="mg-auto">

        <ui-container-box :columns=16 vertical class="page-header-area">

            <div class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
            </div>

            <ui-container-box :columns=16 horizontal>
                <ui-card v-for="(item, index) in cardItems" :key="index"
                    :columns=4 :height=264 no-top-padding small>
                    <ui-card-item img :height=172 no-margin badge="Retail">
                        <img src="@/assets/img/thumb/thumb_76x76.png"/>
                    </ui-card-item>
                    <ui-card-item header>
                        Lorem Ipsum is simply dummy
                    </ui-card-item>
                    <ui-card-item body :margin-top=4>
                        Lorem Ipsum is simply now on
                    </ui-card-item>
                </ui-card>
            </ui-container-box>

        </ui-container-box>

        <ui-container-box :columns=24 vertical align-center class="page-body-area">

            <ui-container-box :columns=24 vertical align-center class="page-tab-area">
                <ui-container-box :columns=16 vertical>

                    <ui-tab underline no-bottom-border :tabs="tabs"/>

                </ui-container-box>
            </ui-container-box>

            <ui-container-box :columns=16 horizontal class="page-main-area">

                <ui-container-box :columns=11 vertical align-start class="page-list-area">

                    <div class="page-list-control">
                        <div class="page-list-control__info">
                            <span class="page-list-control__info-total">
                                Total <b>{{pagingInfo.totalItems}}</b>
                            </span>
                            <lego-dropdown
                                    :items="perPageItems" v-model="pagingInfo.rowsPerPage" />
                        </div>
                        <div class="page-list-control__buttons">
                            <span>Filter 1</span>
                            <span>Filter 2</span>
                            <span>Filter 3</span>
                        </div>
                    </div>

                    <div class="page-list">
                        <ui-list v-for="item in listItems" :key="item.key">
                            <ui-list-item sub>Lorem Ipsum</ui-list-item>
                            <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                            <ui-list-item body>
                                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                                industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                            </ui-list-item>
                            <ui-list-item sub>
                                이진호<hr v/>
                                <lego-icon>display_password</lego-icon> 50<hr v/>
                                <lego-icon>recommend</lego-icon> 0<hr v/>
                                <lego-icon>comment</lego-icon> 3
                            </ui-list-item>
                        </ui-list>
                    </div>

                    <lego-pagination :pagination="pagingInfo" class="mt24"/>

                </ui-container-box>

                <div class="page-area-divider" />

                <ui-container-box :columns=4 vertical align-start class="page-sub-area">

                    <div class="page-sub-header">
                        <div class="page-sub-header__title">
                            Title
                        </div>
                        <div class="page-sub-header__buttons">
                            <span>Filter 1</span>
                            <span>Filter 2</span>
                        </div>
                    </div>

                    <div class="page-sub-list">
                        <ui-list v-for="(item, index) in listItems" :key="item.key" :number="index+1">
                            <ui-list-item body>Lorem Ipsum is simply dummy text</ui-list-item>
                            <ui-list-item sub>
                                이진호<hr v/>
                                <lego-icon>display_password</lego-icon> 50<hr v/>
                                <lego-icon>recommend</lego-icon> 0<hr v/>
                                <lego-icon>comment</lego-icon> 3
                            </ui-list-item>
                        </ui-list>
                    </div>

                </ui-container-box>

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
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false },
                { label: "Tab_5",  isSelected: false },
                { label: "Tab_6",  isSelected: false },
                { label: "Tab_7",  isSelected: false }
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
            cardItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
            ],
            listItems : [
                { key: "1" },
                { key: "2" },
                { key: "3" },
                { key: "4" },
                { key: "5" },
            ]
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
    background-color: white;
}
.page-tab-area {
    border-bottom: 1px solid #CCCCCC;
}
.page-list-area {
    margin-top: 32px;
    margin-bottom: 56px;
}

.page-list-control,
.page-list-control__info,
.page-list-control__info-total,
.page-list-control__buttons {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.page-list-control {
    justify-content: space-between;
}
.page-list-control__info-total {
    padding-right: 12px;
    margin-right: 12px;
    border-right: 1px solid #A5A5A5;
}
.page-list-control__info-total b {
    margin-left: 4px;
}
.page-list-control__buttons span,
.page-sub-header__buttons span {
    padding:0 16px;
    font-size: 12px;
}
.page-list-control__buttons span:hover,
.page-sub-header__buttons span:hover {
    cursor: pointer;
}
.page-list-control__buttons span + span,
.page-sub-header__buttons span + span {
    border-left: 1px solid #CCCCCC;
}

.page-list,
.page-sub-list {
    margin-top: 16px;
    border-top: 1px solid #A5A5A5;
}

.page-sub-area {
    margin-top: 32px;
}
.page-sub-header,
.page-sub-header__buttons {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.page-sub-header {
    height: 32px;
    justify-content: space-between;
}
.page-sub-header__title {
    font-size: 16px;
    font-weight: bold;
}

.ui-list{
    border-bottom: 1px solid #EAEAEA;
}

.page-area-divider {
    width: 64px;
    margin-right: 32px;
    border-right: 1px solid #EAEAEA;
}
</style>