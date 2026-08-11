<template>
    <div class="ui-lnb-item">
        <slot />
    </div>
</template>

<script>
export default {
    name: 'ui-lnb-item'
}
</script>

<style lang="scss">
.ui-lnb-item {
    padding: 0 16px;
}
.ui-lnb-item .lego-tab__label-wrapper {
    flex-grow: 1 !important;
}
.ui-lnb-item .lego-tab__label {
    flex-grow: 1 !important;
}
</style>