<template>

    <ui-container-box :columns=24 vertical :title="title">

        <ui-gnb :twoLines="gnbTwoLines" >
            <template v-slot:lead>
                <ui-gnb-title>
                    <template v-slot:title>SDS Platform</template>
                    <template v-slot:sub>slogan / full name</template>
                </ui-gnb-title>
                <ui-gnb-menus :menus="menus" />
            </template>
            <template v-slot:tail>
                <ui-gnb-icons :icons="['notification','setting']" />
                <ui-gnb-profile>Gildong Hong</ui-gnb-profile>
            </template>
            <template v-slot:second-lead>
                <slot name="gnb-second-lead" />
            </template>
            <template v-slot:second-middle>
                <slot name="gnb-second-middle" />
            </template>
            <template v-slot:second-tail>
                <slot name="gnb-second-tail" />
            </template>
        </ui-gnb>

        <ui-container-box :columns=24 vertical align-center style="background-color:#F7F7F7;">
            <slot />
        </ui-container-box>

    </ui-container-box>

</template>

<script>
export default {
    props: {
        title: { type: String },
        gnbTwoLines: { type: Boolean, default: false }
    },
    data() {
        return {
            menus: [
                { label:'Menu1', key:'menu1', isSelected: true },
                { label:'Menu2', key:'menu2', isSelected: false },
                { label:'Menu3', key:'menu3', isSelected: false },
                { label:'Menu4', key:'menu4', isSelected: false },
                { label:'Menu5', key:'menu5', isSelected: false }
            ]
        }
    }
}
</script>

<style scoped>
</style>