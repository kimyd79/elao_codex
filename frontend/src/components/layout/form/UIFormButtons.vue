<template>
    <div class="ui-form-footer" 
        :class="[
            { 'ui-form-footer__divider' : divider },
            { 'ui-form-footer--no-margin' : noMargin }
        ]"
    >
        <slot name="items" />
        <div class="ui-form-buttons" >
            <slot />
        </div>
    </div>
</template>

<script>
export default {
  name: 'ui-form-buttons',
  props: {
      divider : { type : Boolean, default : false },
      noMargin : { type : Boolean, default : false },
  }
}
</script>

<style lang="scss">
.ui-form-footer {
    margin: 16px 32px 0;
}
.ui-form-footer--no-margin {
    margin: 0;
}
.ui-form-footer__divider {
    border-top: 1px solid #CCCCCC;
}
.ui-form-footer .ui-form-item {
    min-height: 40px;
    margin-top: 0px;
    margin-bottom: 0px;
}
.ui-form-buttons {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-end;
    margin-top: 24px;
}
.ui-form-footer > *:first-child {
    margin-top: 24px;
}

</style>