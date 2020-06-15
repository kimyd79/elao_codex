<template>

    <Page title="Screen without LNB - Split 04" gnbTwoLines class="mg-auto">
        <template v-slot:gnb-second-lead>
            <ui-form-row style="align-items: center;">
                <ui-form-item :columns=5 label="LoremIpm" :label-width=144>
                    <lego-dropdown :items="[{value: 'L', text: '2018.11.10 - 2018.12.9'}]" value="L"/>
                </ui-form-item>
                <ui-form-item :columns=5 label="LoremIpm" :label-width=144>
                    <lego-dropdown :items="[{value: 'L', text: '2018.11.10 - 2018.12.9'}]" value="L"/>
                </ui-form-item>
                <ui-form-item :columns=5 label="LoremIpm" :label-width=144>
                    <lego-dropdown :items="[{value: 'L', text: '2018.11.10 - 2018.12.9'}]" value="L"/>
                </ui-form-item>
            </ui-form-row>
        </template>

        <ui-container-box :columns=24 vertical align-center class="page-container">

            <ui-container-box :columns=22 vertical class="page-main-area">

                <div class="page-header-area">
                    <div class="page-header-info">
                        <span class="page-header-info__label">Total</span>
                        <b class="page-header-info__count">15</b>
                    </div>
                    <div class="page-header-action">
                        <lego-button primary icon="add">New Action</lego-button>
                    </div>
                </div>

                <ui-container-box :columns=20 horizontal class="page-body-area">

                    <ui-container-box :columns=13 vertical class="page-body-list">
                        <div v-for="item in listItems" :key="item.key"
                            class="page-body-list__item"
                        >
                            <div class="page-body-list__item-status">
                                On Workflow 
                            </div>
                            <div class="page-body-list__item-info">
                                <div class="page-body-list__item-header">
                                    <span class="page-body-list__item-header-main">Data Ingestion Rule 1</span>
                                    <span class="page-body-list__item-header-sub">Scarlet</span>
                                </div>
                                <div class="page-body-list__item-detail">
                                    <div class="page-body-list__item-detail-main">
                                        <div class="source">Source:  Oracle, company</div>
                                        <div class="dash" />
                                        <div class="target">target:  Oracle, company</div>
                                    </div>
                                    <div class="page-body-list__item-detail-sub">
                                        <div class="status">Saved on</div>
                                        <div class="date">10-03-2018</div>
                                        <div class="time">12:00:00</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </ui-container-box>

                    <ui-container-box :columns=6 vertical class="page-body-detail">

                        <div class="item">
                            <div class="item-name">Data Setup Rule 1</div>
                            <div class="item-contents">
                                <img src="@/assets/img/thumb/thumb_76x76.png" style="width: 400px; height: 192px;"/>
                            </div>
                        </div>

                        <div class="item">
                            <div class="item-name">Workflow Information</div>
                            <div class="item-contents">Data Setup Rule 1</div>
                        </div>

                        <div class="item">
                            <div class="item-name">Action History</div>
                            <div class="item-sub">01 / 31/ 2019</div>
                            <div class="item-contents">
                                <div class="item-contents-text">11:00   Committed By Bokyung Sohn</div>
                                <div class="item-contents-text">11:00   Committed By Bokyung Sohn</div>
                                <div class="item-contents-text">11:00   Committed By Bokyung Sohn</div>
                                <div class="item-contents-text">11:00   Committed By Bokyung Sohn</div>
                                <div class="item-contents-text">11:00   Committed By Bokyung Sohn</div>
                            </div>
                        </div>

                        <div class="buttons">
                            <lego-button large>Cancel BTN</lego-button>
                            <lego-button large main>Action BTN</lego-button>
                        </div>

                    </ui-container-box>

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
            listItems: [
                {key: '1'},
                {key: '2'},
                {key: '3'},
                {key: '4'},
                {key: '5'},
                {key: '6'},
                {key: '7'},
                {key: '8'},
                {key: '9'},
                {key: '10'},
            ]
        }
    }
}
</script>

<style scoped>
.page-container {
    margin: 48px 0 32px;
}
.page-main-area {
    padding: 48px 80px;
    background-color: white;
}
.page-header-area,
.page-header-info,
.page-header-action {
    display: flex;
    flex-flow: row nowrap;
}
.page-header-area {
    justify-content: space-between;
    align-items: center;
}
.page-header-info__count {
    margin-left: 4px;
}
.page-body-area {
    margin-top: 16px;
    border-top: 1px solid #A5A5A5;
    border-bottom: 1px solid #A5A5A5;
}
.page-body-list__item {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;

    padding: 16px 48px;
}
.page-body-list__item-info {
    display: flex;
    flex-flow: column nowrap;
    flex-grow: 1;

    margin-left: 48px;
}
.page-body-list__item-header,
.page-body-list__item-detail,
.page-body-list__item-detail-main,
.page-body-list__item-detail-sub {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.page-body-list__item-header,
.page-body-list__item-detail {
    justify-content: space-between;
}
.page-body-list__item-header {
    font-size: 16px;
}
.page-body-list__item-detail-main div + div,
.page-body-list__item-detail-sub div + div {
    margin-left: 12px;
}
.page-body-list__item-detail-main .dash {
    width: 25px;
    height: 1px;
    margin-top: 4px;
    background-color: #A5A5A5;
}
.page-body-list__item + .page-body-list__item {
    border-top: 1px solid #EAEAEA;
}

.page-body-detail,
.page-body-detail .item
.page-body-detail .item-contents {
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
}
.page-body-detail {
    background-color: #F7F7F7;
    padding: 32px;
}
.page-body-detail .item + .item {
    margin-top: 32px;
}
.page-body-detail .item-name {
    font-size: 16px;
    font-weight: bold;
}
.page-body-detail .item-sub {
    margin-top: 6px;
    font-weight: bold;
}
.page-body-detail .item-contents {
    margin-top: 12px;
}
.page-body-detail .item-contents-text + .item-contents-text {
    margin-top: 6px;
}
.page-body-detail .buttons {
    margin-top: auto;
    align-self: center;
}

</style>