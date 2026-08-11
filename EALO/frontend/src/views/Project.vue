<template>
<ui-container-box :columns=22 vertical align-center class="page-container">

    <ui-container-box :columns=20 horizontal align-center class="page-title">
        <span class="page-title__label">Project</span>
    </ui-container-box>

    <ui-container-box :columns=20 horizontal class="page-form-area">
        <ProjectSearch></ProjectSearch>
    </ui-container-box>

    <ui-container-box :columns=20 vertical class="page-summary-area">
        <ProjectResult></ProjectResult>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal>
        <ui-container-box :columns="10" vertical class="mt20">
            <font size="4">CI-TEC</font>
        </ui-container-box>
        <ui-container-box :columns="3" vertical class="mt20">
            <img src="@/assets/ico_footer.png" alt="Samsung SDS" />
        </ui-container-box>
    </ui-container-box>

</ui-container-box>
</template>

<script>
import ProjectSearch from "@/components/layout/ProjectSearch";
import ProjectResult from "@/components/layout/ProjectResult";

export default {
    name: 'Logformat',
    components: {
        ProjectSearch: ProjectSearch,
        ProjectResult: ProjectResult,
    },
    data: function () {
        return {

        }
    }
}
</script>

<style scoped>
.page-container {
    margin: 48px 0 32px;
    padding: 48px 80px;
    background-color: white;
}

.page-title {
    margin-top: 16px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #CCCCCC;
}

.page-title__label {
    font-size: 32px;
    font-weight: bold;
}

.page-form-area {
    padding: 16px 0;
    border-bottom: 1px solid #CCCCCC;
}

.page-summary-area {
    margin-top: 16px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid #CCCCCC;
}

.page-summary-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 24px;
}

.page-summary-table {
    border-spacing: 0;
}

.page-summary-table thead th {
    height: 28px;
    border-top: 1px solid #EAEAEA;
    font-weight: normal;
    background-color: #F7F7F7;
}

.page-summary-table thead th+th {
    border-left: 1px solid #EAEAEA;
}

.page-summary-table tbody td {
    height: 44px;
    text-align: center;
    border-bottom: 1px solid #EAEAEA;
}

.page-summary-table tbody tr:first-child td {
    border-top: 1px solid #A5A5A5;
}

.page-summary-table tbody td+td {
    border-left: 1px solid #EAEAEA;
}

.page-tab-area {
    margin-top: 60px;
    border-bottom: 1px solid #CCCCCC;
}

.page-table-area {
    margin: 32px 0 24px;
}
</style>
