<template>

    <ui-container-box :columns=24 vertical :title="title" class="page-popup">

        <ui-container-box :columns=24 vertical align-center>
            <slot />
        </ui-container-box>

    </ui-container-box>

</template>

<script>
export default {
    props: {
        title: { type: String }
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
.page-popup {
    padding: 80px 0;
    background-color: #EAEAEA;
}
</style>