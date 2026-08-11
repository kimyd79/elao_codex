<template>
    <div class="ui-step-box">
        <div class="ui-validation-step-progress">
            <div 
                v-for="(step, index) in steps" :key="index" 
                :class="[
                    { 'ui-validation-step-progress-item' : true },
                    { 'ui-validation-step-progress-item__passed' : (index+1 < currentIndex) },
                    { 'ui-validation-step-progress-item__selected' : (index+1 == currentIndex) },
                ]"
            >
                <div class="ui-validation-step-progress-item-label">
                    <div class="ui-validation-step-progress-item-label-title">
                        <template v-if="index+1 < currentIndex">
                            <lego-icon medium spacing type="picto">check</lego-icon>
                        </template>
                        <template v-else>
                            {{index+1}}
                        </template>
                    </div>
                    <div class="ui-validation-step-progress-item-label-desc">
                        {{step}}
                    </div>
                </div>
                <div 
                    v-if="(index+1 < steps.length)"
                    class="ui-validation-step-progress-divider"
                >
                    <lego-icon medium>more</lego-icon>
                </div>
            </div>
        </div>
        <div v-if="!noContent" class="ui-validation-step-contents">
            <slot>Input the basic information of new table.</slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ui-validation-step',
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
.ui-validation-step-progress {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
    padding: 0 16px 32px;
}
.ui-validation-step-progress-item {
    display: flex;
    flex-flow: row nowrap;
    flex: 0 0 auto;
}
.ui-validation-step-progress-item__passed {
    color: #553CA5;
}
.ui-validation-step-progress-item__selected {
    color: #553CA5;
}
.ui-validation-step-progress-item-label {
    display: flex;
    flex-flow: column nowrap;
    flex: 0 0 auto;
    align-items: center;
    width: 160px;
}
.ui-validation-step-progress-item-label-title {
    font-size: 14px;

    width: 40px;
    height: 40px;
    border-width: 1px;
    border-style: solid;
    border-radius: 40px;

    display:flex;
    justify-content: center;
    align-items: center;
}
.ui-validation-step-progress-item-label-desc {
    margin-top: 4px;
    font-size: 14px;
}
.ui-validation-step-progress-item__selected .ui-validation-step-progress-item-label-title {
    background-color: #553CA5;
    color: white;
}
.ui-validation-step-progress-item__selected .ui-validation-step-progress-item-label-desc {
    font-weight: bold;
}

.ui-validation-step-contents {
    border-top: 1px solid #CCCCCC;
    padding: 12px 32px;
}
.ui-validation-step-progress-divider {
    display: flex;
    align-self: flex-start;

    transform: translateY(4px) rotate(90deg);
}
</style>