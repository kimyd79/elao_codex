<template>
    <div class="ui-lnb-lite">
        <div class="ui-lnb-lite-menus">
            <slot name="menus" />
        </div>
        <div class="ui-lnb-lite-functions">
            <slot name="functions" />
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-lnb-lite'
}
</script>

<style lang="scss">
.ui-lnb-lite {
    display: flex;
    flex-flow: column nowrap;

    width: 80px;
    padding-bottom: 32px;
    color: #333333;
    background: white;

    overflow-y: hidden;
    overflow-x: hidden;
}
.ui-lnb-lite-menus {
    display: flex;
    flex-flow: column nowrap;
    flex-grow: 1;
}
.ui-lnb-lite-functions {
    display: flex;
    flex-flow: column nowrap;
    flex-grow: 0;
}
</style>