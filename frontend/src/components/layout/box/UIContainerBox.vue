<template>
    <div v-if="title" class="container-box">
        <div class="container-box__title">
            <h1 v-if="titleLevel == 1">{{ title }}</h1>
            <h2 v-else-if="titleLevel == 2">{{ title }}</h2>
            <h3 v-else-if="titleLevel == 3">{{ title }}</h3>
            <h4 v-else-if="titleLevel == 4">{{ title }}</h4>
            <h5 v-else-if="titleLevel == 5">{{ title }}</h5>
            <h6 v-else-if="titleLevel == 6">{{ title }}</h6>
            <h1 v-else>{{ title }}</h1>
        </div>
        <div class="container-box__stretch" :class="containerClass" :style="containerStyle">
            <slot />
        </div>
    </div>
    <div v-else :class="containerClass" :style="containerStyle">
        <slot />
    </div>
</template>

<script>
export default {
  name: 'ui-container-box',
  props: {
        columns: { type : Number, required: true },
        height: { type : Number, default: undefined },
        vertical: { type : Boolean, default: false },
        horizontal: { type : Boolean, default: false },
        wrap: { type : Boolean, default: false },
        
        alignStart: { type : Boolean, default: false },
        alignEnd: { type : Boolean, default: false },
        alignCenter: { type : Boolean, default: false },

        title: { type : String },
        titleLevel: { type : Number, default: 1 }
  },
  computed: {
    containerStyle() {
        var width = this.columns * 80 - (this.columns > 1 ? 16 : 0);

        var style = {};
        
        style['width'] = width + 'px';
        if (this.height) {
            style['height'] = this.height + 'px';
        }

        return style;
    },
    containerClass() {
        return [
            {
                'container-box' : true,
                'container-box__vertical': this.vertical,
                'container-box__horizontal': this.horizontal,
                'container-box__wrap': this.wrap,
                'container-box__align--start': this.alignStart,
                'container-box__align--end': this.alignEnd,
                'container-box__align--center': this.alignCenter,
            }
        ];
    }
  }
}
</script>

<style lang="scss" scoped>
.container-box {
    display: flex;
    flex-flow: column nowrap;
    justify-content: space-between;
    align-content: space-between;

    flex-grow: 0;
    flex-shrink: 1;

    height: inherit;
}
.container-box__title {
    margin: 16px 0 16px 24px;
}
.container-box__stretch {
    flex-grow: 1;
}
.container-box__vertical {
    flex-direction: column;
}
.container-box__horizontal {
    flex-direction: row;
}
.container-box__wrap {
    flex-wrap: wrap;
}
.container-box__align--start {
    justify-content: flex-start;
}
.container-box__align--end {
    justify-content: flex-end;
}
.container-box__align--center {
    align-items: center;
}
</style>