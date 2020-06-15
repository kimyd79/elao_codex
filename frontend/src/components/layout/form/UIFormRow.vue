<template>
    <div :class="[
        { 'ui-form-row' : true },
        { 'ui-form-row--right' : alignRight },
        { 'ui-form-row--space-between' : spaceBetween }
    ]"
    >
        <slot />
    </div>
</template>

<script>
export default {
  name: 'ui-form-row',
  props: {
      alignRight: { type: Boolean, default: false },
      spaceBetween: { type: Boolean, default: false },
  }
}
</script>

<style lang="scss">
.ui-form-row {
    display: flex;
    flex-flow: row wrap;
}
.ui-form-row--right {
    justify-content: flex-end;
}
.ui-form-row--space-between {
    justify-content: space-between;
}
.ui-form-row .ui-form-item + .ui-form-item {
    margin-left: 16px;
}
</style>