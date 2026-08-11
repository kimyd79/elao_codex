<template>

    <Page title="Popup X-large" class="mg-auto">

        <ui-container-box :columns=15 vertical class="popup-container">

            <div class="popup-header">
                <div class="popup-header__title">
                    Title
                </div>
                <div class="popup-header__desc">
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                </div>
                <div class="popup-header__close">
                    <lego-icon small>close</lego-icon>
                </div>
            </div>

            <ui-validation-step 
                :steps="['Basic Information', 'Select Data Connection', 'Column Settings', 'Additional Information']" :current-index=2
                class="popup-step" no-content
            />

            <div class="popup-table">

                <ui-table checkable no-action
                    :paging-info="pagingInfo" :columns="columns" :items="items">
                    <template v-slot:cellview-mode="{ item }" >
                        <lego-badge :badge-color="item.mode.toLowerCase()" badge-type="status-dot">
                            {{item.mode}}
                        </lego-badge>
                    </template>
                </ui-table>

            </div>

            <div class="popup-buttons">
                <lego-button>Cancel</lego-button>
                <lego-button main>Okay</lego-button>
            </div>

        </ui-container-box>

    </Page>

</template>

<script>
import Page from '../_Frame/PopupPage'

export default {
    name: 'popup-xl',
    components: {
        Page
    },
    data: function() {
        return {
            pagingInfo : {
                rowsPerPage: 10,
                currentPage: 1,
                totalPages: 17,
                totalItems: 163
            },
            columns: [
                {label: 'Name', key: "name", width: 20 },
                {label: 'Email', key: "email", width: 25 },
                {label: 'Mode', key: "mode", width: 15 },
                {label: 'Gender', key: "gender", width: 20 },
                {label: 'Registrant', key: "registrant", width: 20}
            ],
            items: [
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Error', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Success', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
                {name:'Andere Cummings', email:'cummings@samsung.com', mode:'Processing', gender:'Male', registrant:'10-03-2018', size:'1.2 MB', isSelected: false},
            ],
        }
    }
}
</script>

<style scoped>
.popup-container {
    padding: 32px;
    border: 1px solid #D0D0D0;
    background-color: white;
}
.popup-header {
    position: relative;
    display: flex;
    flex-flow: column nowrap;
}
.popup-header__title {
    font-size: 24px;
    font-weight: bold;
}
.popup-header__desc {
    color: #767676;
    margin-top: 16px;
}
.popup-header__close {
    position: absolute;
    top: 0;
    right: 0;
}
.popup-header__close:hover {
    cursor: pointer;
}
.popup-step {
    margin-top: 48px;
}
.popup-table {
    padding: 16px 48px 48px;
}
.popup-buttons {
    display: flex;
    justify-content: flex-end;
}
</style>