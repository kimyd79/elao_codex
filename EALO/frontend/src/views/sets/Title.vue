<template>
    <ui-page-box align-center>

        <ui-container-box :columns=16 vertical class="mt50 mb50">

            <div class="ui-title">
                <div class="ui-title-label">
                    <div class="ui-title-label__main">
                        Lorem Ipsum
                    </div>
                    <div class="ui-title-label__sub">
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's...
                    </div>
                </div>
                <div class="ui-title-side">
                    <lego-text-field v-model="textValue" placeholder="Search" searchable />
                </div>
            </div>

            <div class="ui-title mt50">
                <div class="ui-title-label">
                    <div class="ui-title-label__main">
                        Lorem Ipsum
                    </div>
                    <div class="ui-title-label__sub">
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's...
                    </div>
                </div>
                <div class="ui-title-side">
                    Menu1 > LNB Menu1 > <em> LNB Sub Menu1</em>
                </div>
            </div>

            <div class="ui-title mt50">
                <div class="ui-title-label">
                    <div class="ui-title-label__main">
                        Lorem Ipsum
                    </div>
                </div>
                <div class="ui-title-side">
                    <lego-text-field v-model="textValue" placeholder="Search" searchable />
                </div>
            </div>

            <div class="ui-title mt50">
                <div class="ui-title-label">
                    <div class="ui-title-label__main">
                        Lorem Ipsum
                    </div>
                </div>
                <div class="ui-title-side">
                    Menu1 > LNB Menu1 > <em> LNB Sub Menu1</em>
                </div>
            </div>

        </ui-container-box>

    </ui-page-box>

</template>

<script>
export default {
    name: 'tab',
    data() {
        return {
            textValue: ''
        }
    }
}
</script>

<style scoped>
.ui-title {
    display: flex;
    flex-flow: row nowrap;

    background-color:white;
    padding-bottom: 16px;
}
.ui-title-label {
    display: flex;
    flex-flow: column nowrap;
}
.ui-title-label__main {
    font-size: 32px;
    font-weight: bold;
}
.ui-title-label__sub {
    color: #5A5A5A;
    font-size: 16px;

    margin-top: 12px;
}
.ui-title-side {
    margin-left: auto;

    display: flex;
    align-items: flex-end;
    color: #767676;
}
.ui-title-side > em {
    color: #333333;
}
</style>