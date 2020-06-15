<template>
    <div 
        :style="formItemStyle" 
        :class="[
            { 'ui-form-item' : true },
            { 'ui-form-item__label--top' : topLabel },
            { 'ui-form-item__label--left' : leftLabel }
        ]"
    >
        <div v-if="label" class="ui-form-label" :class="formLabelClass" :style="labelStyle">
            <span>{{label}}</span>
        </div>
        <div class="ui-form-content" :style="formContentStyle">
            <slot />
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-form-item',
    props: {
        label: { type : String },
        required: { type : Boolean, default : false },
        requiredLeft: { type : Boolean, default : false },
        columns: { type : Number , required : true },
        labelWidth : { type : Number , default : 180 },
        alignRight : { type : Boolean, default : false },
        marginRight : { type : Boolean, default : false },
        noMargin : { type : Boolean, default : false },
        topLabel : { type : Boolean, default : false },
        leftLabel : { type : Boolean, default : false },
        labelPadding : { type : Number , default : 32 },
    },
    computed: {
        formLabelClass() {
            return [
                {
                    'ui-form-label__required' : this.required,
                    'ui-form-label__required--left': this.requiredLeft
                }
            ];
        },
        formItemStyle() {
            var width = this.columns * 80 - 16;

            var style = {};
            style['width']  = width + 'px';

            if (this.noMargin) {
                style['margin-left']  = '0';
            }

            return style;
        },
        labelStyle() {
            var width = this.labelWidth;

            var style = {};
            if (!this.topLabel) {
                style['width']  = width + 'px';
            }
            if (!this.topLabel) {
                style['padding-left'] = this.labelPadding + 'px';
            }

            return style;
        },
        formContentStyle() {
            var style = {};

            if (this.alignRight) {
                style['justify-content']  = 'flex-end';
            }
            if (this.marginRight) {
                style['padding-right']  = '32px';
            }

            return style;
        },
    }
}
</script>

<style lang="scss">
.ui-form-item {
    display: flex;
    flex-flow: row nowrap;

    align-items: center;
    margin: 16px 0;
}
.ui-form-item__label--top {
    flex-direction: column;
    align-items: inherit !important;
}
.ui-form-label {
    display: flex;
    flex-grow: 0;
    flex-shrink: 0;
    font-weight: 430;
    font-size: 16px;

    height: 32px;
    justify-content: flex-end;
    align-items: center;
    align-self: flex-start;
}
.ui-form-item__label--top .ui-form-label {
    
    height: 24px;
    padding-left: 0;
    justify-content: flex-start;
}
.ui-form-item__label--left .ui-form-label {
    justify-content: flex-start;
}
.ui-form-label__required::after {
    content: '*';
    color: #E74C3C;
}
.ui-form-label__required--left::before {
    content: '*';
    color: #E74C3C;
}
.ui-form-label + .ui-form-content {
    margin-left: 32px;
}
.ui-form-item__label--top .ui-form-label + .ui-form-content {
    margin-top: 8px;
    margin-left: 0;
}
.ui-form-content {
    display: flex;
    flex: 1 1 auto;
    justify-content: flex-start;
    align-items: center;
}
.ui-form-content > span {
    color: #777;
}

.ui-form-item .lego-dropdown {
    display: block !important;
}
.ui-form-item .lego-date-picker {
    display: -ms-flexbox !important;
    flex-grow: 1;
}
.ui-form-item .lego-date-picker + .lego-date-picker::before {
    content: '~';
    margin: 0 8px;
    color: #333;
}
.ui-form-item .lego-date-picker__text-field {
    flex-grow: 1;
}
.ui-form-item .lego-segment-wrapper {
    display: flex;
    width: 100%;
}
.ui-form-item .lego-segment-button {
    flex-grow: 1;
}
.ui-form-item .lego-radio__label {
    font-size: 14px !important;
}
.ui-form-item .lego-radio {
    display: flex;
    flex-grow: 0;
}
.ui-form-item .lego-radio + .lego-radio {
    margin-left: 24px;
}
.ui-form-item .lego-button {
    min-width: 100px;
}
.ui-form-item .lego-text-field + .lego-text-field {
    margin-left: 16px;
}
.ui-form-item .lego-chip__container + .lego-chip__container {
    margin-left: 4px;
}
.ui-form-item .lego-text-field {
    min-width: inherit;
}
</style>