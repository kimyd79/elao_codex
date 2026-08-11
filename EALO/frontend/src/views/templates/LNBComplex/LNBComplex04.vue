<template>

    <LNBPage title="Screen with LNB - Complex 04" class="mg-auto">

        <ui-container-box :columns=16 vertical class="pt16" >

            <div class="ui-title-page">
                <div class="ui-title-page-label">
                    <div class="ui-title-page-label__main">
                        Lorem Ipsum
                    </div>
                </div>
                <div class="ui-title-page-label__sub">
                    <span>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. <br>
                        Lorem Ipsum has been the industry’s standard dummy text ever since the 1500s, when an unknown printer to…
                    </span>
                </div>
            </div>

            <ui-container-box :columns=16 wrap horizontal>

                <div v-for="(card, index) in cards" :key="index" class="content-card mt24">
                    <span class="content-card-title">{{card.title}}</span>
                    <ui-card :columns=4 :height=228 no-border vertical-align-center>
                        
                        <ui-card-item img :height=160>
                            <img src="@/assets/img/thumb/thumb_76x76.png"/>
                        </ui-card-item>
                        
                    </ui-card>
                </div>

            </ui-container-box>

        </ui-container-box>

    </LNBPage>

</template>

<script>
import LNBPage from '../_Frame/LNBDesignPage'

export default {
    name: 'lnb-complex-04',
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
                {title:'Badge', desc:'Lorem Ipsum is simply'},
                {title:'Button', desc:'Lorem Ipsum is simply'},
                {title:'Card', desc:'Lorem Ipsum is simply'},
                {title:'Checkbox', desc:'Lorem Ipsum is simply'},

                {title:'Chip', desc:'Lorem Ipsum is simply'},
                {title:'Date&Time Picker', desc:'Lorem Ipsum is simply'},
                {title:'Dropdown List', desc:'Lorem Ipsum is simply'},
                {title:'List', desc:'Lorem Ipsum is simply'},

                {title:'Page Navigation', desc:'Lorem Ipsum is simply'},
                {title:'Progress', desc:'Lorem Ipsum is simply'},
                {title:'Radio Button', desc:'Lorem Ipsum is simply'},
                {title:'Slider', desc:'Lorem Ipsum is simply'},
            ]
        }
    }
}
</script>

<style scoped>
.ui-title-page {
    display: flex;
    flex-flow: column nowrap;

    padding-bottom: 24px;
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
.content-card-title {
    display: block;
    padding-bottom: 12px;
}
.content-card:hover {
    cursor: pointer;
    color: #553CA5;
}
.content-card .ui-card{
    border-radius: 4px;
}
.content-card:hover .ui-card {
    background-color: #CCCCCC;
}
</style>