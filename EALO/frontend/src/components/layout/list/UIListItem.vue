<template>
    <div class="ui-list-content-item" :class="listItemClass" :style="listItemStyle" v-on="listeners">
        <slot />
    </div>
</template>

<script>
export default {
  name: 'ui-list-item',
  props: {
      header: { type : Boolean, default: false },
      sub: { type : Boolean, default: false },
      body: { type : Boolean, default: false },
      info: { type : Boolean, default: false },
      icons: { type : Boolean, default: false },
      box: { type : Boolean, default: false },
      boxRatio: { type : Number, default: 1},

      fillGap : { type : Boolean, default: false },
      elipsis : { type : Boolean, default: false }
  },
  computed: {
    listItemClass() {
        return [
            {
                'ui-list-content-item__header' : this.header,
                'ui-list-content-item__sub' : this.sub,
                'ui-list-content-item__body' : this.body,
                'ui-list-content-item__info' : this.info,
                'ui-list-content-item__icons' : this.icons,
                'ui-list-content-item__box' : this.box,

                'ui-list-content-item__fill--gap' : this.fillGap,
                'ui-list-content-item__elipsis' : this.elipsis,
            }
        ];
    },
    listItemStyle() {
        var style = {};

        if (this.box) {
            style['flex-grow']  = this.boxRatio;
        }

        return style;
    },
    listeners() {
        return this.$listeners;
    }
  }
}
</script>

<style lang="scss">
.ui-list-content-item {
    display: flex;
    flex-flow: row nowrap;
    flex-grow: 0;
    flex-shrink: 0;
}
.ui-list-content-item__fill--gap {
    flex-grow: 1 !important;
}
.ui-list-content-item__elipsis {
    display: block;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}
.ui-list-content-item__header {
    font-size: 16px;
    font-weight: 450;
}
.ui-list-content-item__sub {
    font-size: 12px;
    color: #767676;
}
.ui-list-content-item__sub > hr {
    margin: 4px 8px;
}
.ui-list-content-item__sub > i {
    margin-right: 4px;
}
.ui-list-content-item__body {
    font-size: 14px;
    color: #767676;
}
.ui-list-content-item__info {
    font-size: 16px;
}
.ui-list-content-item__icons > .lego-icon + .lego-icon {
    margin-left: 16px;
}
.ui-list-content-item__box {
    flex-grow: 1;
    flex-shrink: 1;
    justify-content: space-between;
    align-items: center;
}

.ui-list-content-item__sub + .ui-list-content-item__header {
    margin-top: 2px;
}
.ui-list-content-item__header + .ui-list-content-item__sub {
    margin-top: 10px;
}
.ui-list-content-item__header + .ui-list-content-item__body {
    margin-top: 8px;
}
.ui-list-content-item__body + .ui-list-content-item__sub {
    margin-top: 10px;
}
.ui-list-content-item__header + .ui-list-content-item__info {
    margin-top: 8px;
}
.ui-list-content-item__body + .ui-list-content-item__info {
    margin-top: 8px;
}
</style>