<template>
    <div class="ui-step-box">
        <div class="ui-step-progress">
            <div 
                v-for="(step, index) in steps" :key="index" 
                :class="[
                    { 'ui-step-progress-item' : true },
                    { 'ui-step-progress-item__selected' : (index+1 == currentIndex) }
                ]"
            >
                <div class="ui-step-progress-item-label">
                    <div class="ui-step-progress-item-label-title">
                        Step{{index+1}}
                    </div>
                    <div class="ui-step-progress-item-label-desc">
                        {{step}}
                    </div>
                </div>
                <div 
                    v-if="(index+1 < steps.length)"
                    class="ui-step-progress-divider"
                >
                    <lego-icon medium>collapse_menu</lego-icon>
                </div>
            </div>
        </div>
        <div v-if="!noContent" class="ui-step-contents">
            <slot>Input the basic information of new table.</slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-step',
    props: {
        steps: { type: Array, required: true },
        currentIndex: { type: Number, default: 1 },
        noContent: { type: Boolean, default: false }
    }
}
</script>
<style>
.ui-step-box {
    display: flex;
    flex-flow: column nowrap;
    background: white;
    color: #959595;
}
.ui-step-progress {
    display: flex;
    flex-flow: row nowrap;
    padding: 0 16px 32px;
}
.ui-step-progress-item {
    display: flex;
    flex-flow: row nowrap;
    flex: 1 0 auto;
}
.ui-step-progress-item__selected {
    color: #553CA5;
}
.ui-step-progress-item-label {
    display: flex;
    flex-flow: column nowrap;
    flex: 1 0 auto;
}
.ui-step-progress-item-label-title {
    font-size: 24px;
    font-weight: bold;
}
.ui-step-progress-item-label-desc {
    margin-top: 4px;
    font-size: 16px;
}

.ui-step-contents {
    border-top: 1px solid #CCCCCC;
    padding: 12px 32px;
}
.ui-step-progress-divider {
    transform: rotate(90deg);
    display: flex;
    align-items: center;
    margin: 0 32px;
}
</style>