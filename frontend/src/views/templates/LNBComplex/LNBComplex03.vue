<template>

    <LNBPage title="Screen with LNB - Complex 03" class="mg-auto">

        <ui-container-box :columns=16 vertical class="pt16" >

            <div class="ui-title-page">
                <div class="ui-title-page-label">
                    <div class="ui-title-page-label__main">
                        Lorem Ipsum
                    </div>
                </div>
                <div class="ui-title-page-label__sub">
                    <span>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
                    </span>
                    <span>
                        <lego-text-field searchable placeholder="Search" />
                    </span>
                </div>
            </div>

            <div class="contents-info">
                <span class="contents-info__total">
                    Total <b>33</b>
                </span>
                <span class="contents-info__filter">
                    <lego-dropdown v-model="value" small
                        :items="[
                            {value:'A', text:'All'},
                            {value:'Y', text:'Status Y'},
                            {value:'N', text:'Status N'},
                        ]" 
                    />
                </span>
            </div>

            <ui-container-box :columns=16 wrap horizontal>

                <ui-card v-for="(card, index) in cards" :key="index" class="mt16"
                    :columns=4 :height=350 no-border
                >
                    <ui-card-item second>
                        <em>Secondary Text</em> > Menu
                    </ui-card-item>
                    <ui-card-item header>
                        Lorem Ipsum
                    </ui-card-item>
                    <ui-card-item body fill-gap>
                        Lorem Ipsum is simply dummy text of
                        the printing and typesetting industry.
                        Lorem Ipsum has been the industry's
                        standard dummy text ever since the
                        1500s, when an unknown printer took
                        a galley of type and scrambled it to
                        make a type specimen book. It...
                    </ui-card-item>
                    <ui-card-item action>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-card-item>
                </ui-card>

            </ui-container-box>

        </ui-container-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBDesignPage'

export default {
    name: 'lnb-complex-03',
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
            checkValue: false,
            cards: [
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},

                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},

                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
                {title:'Lorem Ipsum', desc:'Lorem Ipsum is simply'},
            ]
        }
    }
}
</script>

<style scoped>
.contents-info {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    margin-top: 32px;
}
.contents-info__total {
    margin-right: 18px;
}
.contents-info__filter {
    width: 110px;
}
.ui-title-page {
    display: flex;
    flex-flow: column nowrap;

    padding-bottom: 24px;

    border-bottom: 1px solid #CCCCCC;
}
.ui-title-page-label__main {
    font-size: 32px;
    font-weight: bold;
}
.ui-title-page-label__sub {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    justify-content: space-between;
    color: #5A5A5A;
    font-size: 16px;

    margin-top: 12px;
}
</style>