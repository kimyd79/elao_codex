<template>
    <div class="ui-card-item" :class="cardItemClass" :style="cardItemStyle">
        <template v-if="bookmark || tag">
            <div v-if="tag" class="lego-card__tag">
                <slot />
            </div>
            <div v-if="bookmark" class="lego-card__icon">
                <lego-icon primary type="picto">bookmark</lego-icon>
            </div>
        </template>
        <template v-else-if="action">
            <div>
                <slot />
            </div>
            <div v-if="actionLabel" class="lego-card__action-link">
                <span>
                    {{ actionLabel }}
                </span>
                <div class="lego-card__action-link-icon">
                    <lego-icon style="transform: rotate(90deg);" type="picto">collapse_menu</lego-icon>
                </div>
            </div>
        </template>
        <template v-else-if="profile">
            <img src="@/assets/img/thumb/avatar_68x68.png" class="lego-card__avatar"/>
            <div class="lego-card__name">
                <slot name="name"/>
            </div>
            <div class="lego-card__second">
                <slot name="email"/>
            </div>
        </template>
        <template v-else>
            <lego-checkbox v-if="checked != undefined" v-model="checked" class="ui-card-item__check"/>
            <span v-if="badge" class="ui-card-item__badge">{{badge}}</span>
            <slot />
        </template>
    </div>
</template>

<script>
export default {
  name: 'ui-card-item',
  props: {
      second: { type : Boolean, default: false },
      header: { type : Boolean, default: false },
      sub: { type : Boolean, default: false },
      body: { type : Boolean, default: false },
      tag: { type : Boolean, default: false },
      bookmark: { type : Boolean, default: false },
      action : { type : Boolean, default: false },
      actionLabel: { type : String },
      img : { type : Boolean, default: false },
      badge : { type : String },
      checked : {},
      profile : { type : Boolean, default: false },

      fillGap : { type : Boolean, default: false },
      noMargin : { type : Boolean, default: false },
      height: { type : Number },
      marginTop: { type : Number }
  },
  computed: {
    cardItemClass() {
        return [
            {
                'lego-card__profile' : this.profile,
                'lego-card__second': this.second,
                'lego-card__header': this.header,
                'lego-card__sub': this.sub,
                'lego-card__body'  : this.body,
                'lego-card__action': this.action,
                'lego-card__tray' : this.bookmark || this.tag,
                'lego-card__fill' : this.fillGap,
                'ui-card__media' : this.img,
                'ui-card-item__side-margin' : !this.noMargin
            }
        ];
    },
    cardItemStyle() {
        var height = this.height;
        var marginTop = this.marginTop;
        var style = {};

        if (height) {
            style['height']  = height + 'px';
        }
        if (marginTop) {
            style['margin-top'] = marginTop + 'px';
        }

        return style;
    }
  }
}
</script>

<style lang="scss" >
.ui-card-item {
    flex-grow: 0;
}
.ui-card-item__side-margin {
    margin-left: 24px;
    margin-right: 24px;
}
.lego-card__profile {
    margin-bottom: 0 !important;
}
.lego-card__header + .ui-card__media {
    margin-top: 16px;
}
.lego-card__profile + .ui-card__media {
    margin-top: 16px;
}
.ui-card__media {
    position: relative;
}
.ui-card__media > img {
    height: 100%;
    width: 100%;
}
.ui-card-item__badge {
    position: absolute;
    bottom: 8px;
    right: 8px;

    background: #eeecf6;
    color: #553CA5;
    font-size: 14px;
    border-radius: 2px;
    height: 24px;
    padding: 1px 8px 3px 8px;
}
.ui-card-item__check {
    background: #eeecf6;
    position: absolute;
    top: 8px;
    left: 8px;
}
.lego-card__fill {
    flex-grow: 1 !important;
}
.lego-card__sub {
    font-size: 14px;
    line-height: 24px;
    color: $LEGO__COLOR--GRAY-90;
}
.ui-card__media + .lego-card__second {
    margin-top: 16px;
}
.ui-card__media + .lego-card__header {
    margin-top: 16px;
}
.lego-card__second + .lego-card__header {
    margin-top: 8px;
}
.lego-card__header {
    margin-bottom: 0 !important;
}
.lego-card__header + .lego-card__sub {
    margin-top: 4px;
}
.lego-card__header + .lego-card__body {
    margin-top: 16px;
}
.lego-card__sub + .lego-card__body {
    margin-top: 24px;
}
.ui-card__media + .lego-card__body {
    margin-top: 8px;
}
.ui-card__media + .lego-card__second {
    margin-top: 8px;
}
.lego-card__body {
    margin-bottom: 0 !important;
}
.lego-card__body + .lego-card__action {
    margin-top: 16px;
}
.ui-card__media + .lego-card__action {
    margin-top: 16px;
}
.lego-card__header + .lego-card__action {
    margin-top: 16px;
}
.lego-card__action {
    flex-flow: row nowrap;
    justify-content: space-between;
    display: flex;
}
.lego-card__action-link {
    color: $lego__color--primary;
    font-size: 12px;
    display: flex;
}
.lego-card__action-link:hover {
    cursor: pointer;
}
.lego-card__action-link-icon {
    display: flex;
    flex-flow: row nowrap;
    margin-left: 2px;
}

.ui-card__small .lego-card__header {
    font-size: 16px;
}
.ui-card__small .lego-card__body {
    font-size: 12px;
}
.ui-card__small .lego-card__second {
    font-size: 12px;
}
.ui-card__small .lego-card__action {
    font-size: 12px;
}
</style>