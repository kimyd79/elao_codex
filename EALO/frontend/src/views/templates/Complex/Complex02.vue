<template>

    <Page title="Screen without LNB - Complex 02" class="mg-auto">

        <ui-container-box :columns=24 vertical align-center class="bg-white">

            <ui-container-box :columns=18 vertical class="page-tab-area">

                <ui-tab box no-action :tabs="tabs"/>

            </ui-container-box>

            <ui-container-box :columns=18 vertical class="page-header-area">

                <div class="page-title">
                    <span class="page-title__label">Lorem Ipsum</span>
                </div>

                <div class="page-description">
                    <span class="page-description__text">
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's...
                    </span>
                    <div class="page-description__search">
                        <lego-text-field searchable placeholder="Search" />
                    </div>
                </div>

            </ui-container-box>

            <ui-container-box :columns=18 vertical class="page-body-area">

                <ui-container-box :columns=18 horizontal wrap >

                    <div v-for="(card, index) in cardItems" :key="index"
                        class="page-item">
                        <div class="page-item__thumb">
                            <img src="@/assets/img/thumb/thumb_76x76.png" style="width: 64px; height: 64px;"/>
                            <div class="page-item__thumb-name">Lorem</div>
                        </div>

                        <div class="page-item__list">

                            <ui-card v-for="subCard in cardSubItems" :key="index+subCard.label"
                                small :columns=7 :height=140 :padding=16 no-border
                            >
                                <ui-card-item header>
                                    Lorem Ipsum is simply dummy text
                                </ui-card-item>
                                <ui-card-item body :margin-top=8>
                                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s
                                </ui-card-item>
                                <ui-card-item action :margin-top=8>
                                    <span>Detail View ></span>
                                </ui-card-item>
                            </ui-card>
                        </div>
                    </div>
                </ui-container-box>


                <lego-pagination :pagination="pagingInfo" class="mt24"/>

            </ui-container-box>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'complex-03',
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
            cardItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
                { label: "5" },
                { label: "6" },
            ],
            cardSubItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
            ],
            pagingInfo : {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 17,
                totalItems: 163
            },
        }
    }
}
</script>

<style scoped>
.page-tab-area {
    margin-top: 48px;
}
.page-header-area {
    margin-top: 32px;
    padding-bottom: 12px;
    border-bottom: 1px solid #CCCCCC;
}
.page-title__label {
    font-size: 32px;
    font-weight: bold;
}

.page-description {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
}
.page-description__search {
    width: 208px;
}

.page-body-area {
    padding-bottom: 56px;
}

.page-item {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-start;
    justify-content: space-between;
    
    padding: 32px 64px 32px 32px;
    width: 712px;
    margin-top: 32px;

    border-bottom: 1px solid #CCCCCC;
}
.page-item__thumb {
    margin-top: 16px;
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
}
.page-item__thumb-name {
    margin-top: 4px;
}
.page-item__list .ui-card {
    border-bottom: 1px solid #EAEAEA;
}

</style>