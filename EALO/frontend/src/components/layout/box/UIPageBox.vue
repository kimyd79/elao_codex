<template>
    <div class="page-box" :style="pageStyle" :class="{'page-box__center' : alignCenter}">
        <slot />
    </div>
</template>

<script>
export default {
  name: 'ui-page-box',
  props: {
      columns: { default: 24 },
      height: { default: undefined },
      alignCenter: { type: Boolean, default: false }
  },
  computed: {
    pageStyle() {
        var width = this.columns * 80;
        var height = this.height;

        var style = {};
        
        style['width']  = width + 'px';
        if (height) {
            style['height']  = height + 'px';
        }

        return style;
    }
  }
}
</script>

<style lang="scss" scoped>
.page-box {
    display: flex;
    flex-flow: row wrap;
    margin: auto;
}
.page-box__center {
    justify-content: center;
}
</style>