<template>
    <div class="ui-card" :style="cardStyle" 
        :class="[
            { 'ui-card__small' : small },
            { 'ui-card--no-border' : noBorder },
        ]"
    >
        <div v-if="leftImg" :class="leftImgClass">
            <slot name="img"></slot>
        </div>
        <div class="ui-card__contents" :style="contentsStyle">
            <slot></slot>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ui-card',
        props: {
            // $ver: v0.1.0
            // 카드의 폭을 지정합니다. 단위는 columns 입니다.
            columns : { type: Number, required: true },

            // $ver: v0.1.0
            // 카드의 높이를 지정합니다. 단위는 px 입니다.
            height: { type: Number, default: 0 },
            padding: { type: Number, default: 24 },

            leftImg : { type: Boolean, default: false },
            noTopPadding : { type: Boolean, default: false },
            noImgMargin : { type: Boolean, default: false },
            small : { type: Boolean, default: false },
            noBorder : { type: Boolean, default: false },
            verticalAlignCenter : { type: Boolean, default: false },
        },
        data() {return {}},
        computed: {
            cardStyle() {
                var width = this.columns * 80 - (this.columns > 1 ? 16 : 0);
                var height = this.height;

                var style = {};
                
                style['width']  = width + 'px';
                if (height) {
                    style['height']  = height + 'px';
                }

                return style;
            },
            contentsStyle() {
                var style = {};

                style['padding'] = this.padding + 'px 0';
                
                if (this.noTopPadding) {
                    style['padding-top']  = '0';
                }
                if (this.verticalAlignCenter) {
                    style['justify-content']  = 'center';
                }

                return style;
            },
            leftImgClass() {
                return [
                    {
                        'ui-card__left-img' : true,
                        'ui-card__left-img-margin': !this.noImgMargin
                    }
                ];
            }
        }
    };
</script>

<style lang="scss" scoped>
.ui-card {
    border    : 1px solid #DBDBDB;
    background: white;
    display: flex;
}
.ui-card--no-border {
    border: none;
}
.ui-card__left-img {
    height: 100%;
    flex-basis: 1;
}
.ui-card__left-img-margin {
    padding: 24px 0 24px 24px;
}
.ui-card__left-img > img {
    height: 100%;
}
.ui-card__contents {
    display: flex;
    flex-flow: column nowrap;
    height: 100%;
    flex-grow: 1;
    flex-basis: 0;
}
</style>