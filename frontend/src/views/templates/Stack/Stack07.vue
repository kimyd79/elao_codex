<template>

    <Page title="Screen without LNB - Stack 07" class="mg-auto">

        <ui-container-box :columns=22 vertical align-center class="page-container">

            <ui-container-box :columns=20 horizontal align-center class="page-title">
                <span class="page-title__label">Lorem Ipsum</span>
                <span class="page-title__sub">
                    Menu1 > LNB Menu1 > <em>LNB Sub Menu1</em>
                </span>
            </ui-container-box>

            <ui-container-box :columns=20 horizontal class="page-form-area">

                <ui-form-box>

                    <ui-form-row>
                        <ui-form-item :columns=6 label="Lorem Ipsum">
                            <lego-dropdown :items="[{value: 'L', text: 'Lorem Ipsum'}]" value="L"/>
                        </ui-form-item>
                        <ui-form-item :columns=6 label="Lorem Ipsum" required-left>
                            <lego-date-picker v-model="dateValue" />
                        </ui-form-item>
                        <ui-form-item :columns=8 align-right margin-right>
                            <lego-button main>Lorem</lego-button>
                        </ui-form-item>
                    </ui-form-row>

                </ui-form-box>

            </ui-container-box>

            <ui-container-box :columns=20 vertical class="page-summary-area">

                <div class="page-summary-title">Lorem Ipsum</div>

                <table class="page-summary-table">
                    <thead>
                        <tr>
                            <th rowspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                            <th colspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                            <th rowspan="2">Lorem</th>
                        </tr>
                        <tr>
                            <th>Lorem</th>
                            <th>Lorem</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Lorem</td>
                            <td>ipsum</td>
                            <td>ipsum dolor sit amet</td>
                            <td>ppt</td>
                            <td>All</td>
                            <td>All</td>
                            <td>ipsum dolor sit amet</td>
                            <td>ipsum</td>
                            <td>ipsum</td>
                            <td>ipsum</td>
                        </tr>
                        <tr>
                            <td>Lorem</td>
                            <td>File</td>
                            <td>ipsum dolor sit amet</td>
                            <td>ppt</td>
                            <td>All</td>
                            <td>All</td>
                            <td>ipsum dolor sit amet</td>
                            <td>ipsum</td>
                            <td>ipsum</td>
                            <td>ipsum</td>
                        </tr>
                    </tbody>
                </table>

            </ui-container-box>

            <ui-container-box :columns=20 horizontal class="page-tab-area">

                <ui-tab box :tabs="tabs" no-action />

            </ui-container-box>

            <ui-container-box :columns=18 vertical class="page-table-area">

                <ui-table left-header
                    :paging-info="pagingInfo" :columns="leftHeaderColumns" :items="leftHeaderItems"  />

            </ui-container-box>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/Page'

export default {
    name: 'stack-07',
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
            leftHeaderColumns: [
                {label: 'Floor', key: "floor", alignCenter: true, width: 20 },
                {label: '1', key: "one", alignCenter: true, width: 20 },
                {label: '2', key: "two", alignCenter: true, width: 20 },
                {label: '3', key: "three", alignCenter: true, width: 20 },
                {label: '4', key: "four", alignCenter: true, width: 20 },
                {label: '5', key: "five", alignCenter: true, width: 20 },
                {label: '6', key: "six", alignCenter: true, width: 20 },
                {label: '7', key: "seven", alignCenter: true, width: 20 },
                {label: '8', key: "eight", alignCenter: true, width: 20 }
            ],
            leftHeaderItems: [
                {floor:'63F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'62F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'61F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'60F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'59F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'58F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'57F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'56F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'55F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'},
                {floor:'54F', one:'89', two:'97', three:'109', four:'188', five:'176', six:'213', seven:'229', eight:'302'}
            ]
        }
    }
}
</script>

<style scoped>
.page-container {
    margin: 48px 0 32px;
    padding: 48px 80px;
    background-color: white;
}
.page-title {
    margin-top: 16px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #CCCCCC;
}
.page-title__label {
    font-size: 32px;
    font-weight: bold;
}
.page-form-area {
    padding: 16px 0;
    border-bottom: 1px solid #CCCCCC;
}
.page-summary-area {
    margin-top: 48px;
}
.page-summary-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 24px;
}
.page-summary-table {
    border-spacing: 0;
}
.page-summary-table thead th {
    height: 28px;
    border-top: 1px solid #EAEAEA;
    font-weight: normal;
    background-color: #F7F7F7;
}
.page-summary-table thead th + th {
    border-left: 1px solid #EAEAEA;
}
.page-summary-table tbody td {
    height: 44px;
    text-align: center;
    border-bottom: 1px solid #EAEAEA;
}
.page-summary-table tbody tr:first-child td {
    border-top: 1px solid #A5A5A5;
}
.page-summary-table tbody td + td {
    border-left: 1px solid #EAEAEA;
}
.page-tab-area {
    margin-top: 60px;
    border-bottom: 1px solid #CCCCCC;
}
.page-table-area {
    margin: 32px 0 24px;
}
</style>