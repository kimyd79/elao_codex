<template>

    <LNBPage title="Screen with LNB - Stack 08" class="mg-auto">

        <ui-step :steps="['Data Selection', 'Table Information', 'Field Setting', 'Chart Setting']">
            <div class="mt20">Input the basic information of new table.</div>
        </ui-step>

        <ui-form-box style="padding-top: 8px;">

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <span class="fs16">Lorem Ipsum</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <span class="fs16">Lorem Ipsum</span>
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <lego-text-field disabled value="Lorem ipsum" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <lego-text-field disabled textarea rows="4" value="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry’s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum." />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <lego-text-field value="Lorem ipsum" />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=18 label="Lorem ipsum" required left-label>
                    <lego-text-field disabled textarea rows="4" value="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry’s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum." />
                </ui-form-item>
            </ui-form-row>

            <ui-form-row>
                <ui-form-item :columns=7 label="Lorem ipsum" required left-label>
                    <lego-radio v-model="radioValue" value="1">Lorem ipsum</lego-radio>
                    <lego-radio v-model="radioValue" value="2">Lorem ipsum</lego-radio>
                </ui-form-item>
            </ui-form-row>

        </ui-form-box>

        <ui-form-buttons divider class="page-buttons">
            <lego-button large>Delete</lego-button>
            <lego-button large main>Save</lego-button>
        </ui-form-buttons>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBTitlePage'

export default {
    name: 'lnb-stack-08',
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
            checkValue: [],
            tabs: [
                { label: "Tab_1",  isSelected: true },
                { label: "Tab_2",  isSelected: false },
                { label: "Tab_3",  isSelected: false },
                { label: "Tab_4",  isSelected: false }
            ]
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
    margin: 32px 0;
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
.table-checkbox {
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-end;
    margin: 20px 0;
}
.page-buttons {
    border-top-color: #cccccc;
    margin: 24px 0 0 0;
}
.fs16 {
    font-size: 16px;
}
</style>