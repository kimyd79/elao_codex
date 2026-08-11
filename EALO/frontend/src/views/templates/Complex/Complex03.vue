<template>

    <Page title="Screen without LNB - Complex 03" class="mg-auto">

        <ui-container-box :columns=16 vertical class="page-header-area">

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

        <ui-container-box :columns=16 vertical class="page-body-area">

            <div class="page-list-info">
                <span class="page-list-info__total">
                    Total 33
                </span>
                <div class="page-list-info__order">
                    <lego-dropdown :items="[{text:'Sort by', value:'sort'}]" value="sort" />
                </div>
            </div>

            <ui-container-box :columns=16 horizontal wrap class="page-list-area">

                <ui-card v-for="(item, index) in cardItems" :key="index" class="page-list-card"
                    :columns=8 :height=290>
                    <ui-card-item tag bookmark>
                        Retail
                    </ui-card-item>
                    <ui-card-item header>
                        Lorem Ipsum is dummy text of the <br>
                        printing and typesetting industry.
                    </ui-card-item>
                    <ui-card-item body fill-gap>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
                        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
                        exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat...
                    </ui-card-item>
                    <ui-card-item action action-label="View Detail &amp; Simulation">
                        By Senior Engineer<hr v/>
                        <lego-icon>display_password</lego-icon> 50
                    </ui-card-item>
                </ui-card>

            </ui-container-box>

            <lego-pagination :pagination="pagingInfo" class="mt24"/>


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
            cardItems : [
                { label: "1" },
                { label: "2" },
                { label: "3" },
                { label: "4" },
                { label: "5" },
                { label: "6" },
                { label: "7" },
                { label: "8" },
                { label: "9" },
                { label: "10" },
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
.page-header-area {
    margin-top: 48px;
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
    margin-top: 32px;
    padding-bottom: 56px;
}

.page-list-info {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
}
.page-list-info__total {
    margin-right: 16px;
}
.page-list-info__order {
    width: 112px;
}

.page-list-card {
    margin-top: 16px;
}
</style>