<template>
    <div class="ui-gnb-action-item">
        <slot />
    </div>
</template>

<script>
export default {
    name: 'ui-gnb-item'
}
</script>

<style lang="scss">
.ui-gnb-action-item {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    padding: 0 16px;
}
.ui-gnb-action-item + .ui-gnb-action-item {
    border-left: 1px solid #767676;
}
</style>