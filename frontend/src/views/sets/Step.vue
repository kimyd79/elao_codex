<template>
    <ui-page-box align-center>

        <ui-container-box :columns=18 vertical class="mt50" title="Normal">

            <ui-step :steps="['Data Selection', 'Table Information', 'Field Setting', 'Chart Setting']">
                Input the basic information of new table.
            </ui-step>

        </ui-container-box>

        <ui-container-box :columns=18 vertical class="mb50" title="Validation">

            <ui-validation-step :steps="['Basic Information', 'Select Data Connection', 'Column Settings', 'Additional Information']" :current-index=3>
                Input the basic information of new table.
            </ui-validation-step>

        </ui-container-box>

    </ui-page-box>

</template>

<script>
export default {
    name: 'step'
}
</script>