<template>
    <div class="ui-form-box">
        <slot />
    </div>
</template>

<script>
export default {
  name: 'ui-form-box'
}
</script>

<style lang="scss">
.ui-form-box {
    display: flex;
    flex-flow: column nowrap;

    padding: 32px 0;
    background: white;
}
</style>