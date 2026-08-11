<template>
    <ui-page-box align-center>

        <ui-container-box title="Form" :columns=18 vertical class="mt50 mb50">

            <ui-form-box>
                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=6 label="Lorem Ipsum" required :label-width=240>
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-segment-wrapper solid primary v-model="segmentValue">
                            <lego-segment-button value="1">Lorem</lego-segment-button>
                            <lego-segment-button value="2">Lorem</lego-segment-button>
                        </lego-segment-wrapper>
                    </ui-form-item>
                    <ui-form-item :columns=9 label="Lorem ipsum dilor" :label-width=240>
                        <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="3">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="4">Lorem Ipsum</lego-radio>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-buttons divider>
                    <lego-button>Lorem</lego-button>
                    <lego-button main>Lorem</lego-button>
                </ui-form-buttons>

            </ui-form-box>

            <ui-form-box class="mt20">

                <ui-form-row>
                    <ui-form-item :columns=8 label="Lorem ipsum dilor" >
                        <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="3">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="4">Lorem Ipsum</lego-radio>
                    </ui-form-item>
                    <ui-form-item :columns=6 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=7>
                        <span>* Lorem Ipsum is simply dummy text of the printing and typesetting industry.</span>
                    </ui-form-item>
                    <ui-form-item :columns=6 align-right margin-right>
                        <lego-button main>Lorem</lego-button>
                    </ui-form-item>
                </ui-form-row>

            </ui-form-box>

            <ui-form-box class="mt20">

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=7>
                        <span>* Lorem Ipsum is simply dummy text of the printing and typesetting industry.</span>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=8 label="Lorem ipsum dilor" >
                        <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="3">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="4">Lorem Ipsum</lego-radio>
                    </ui-form-item>
                    <ui-form-item :columns=6 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                    </ui-form-item>
                    <ui-form-item :columns=4 align-right margin-right>
                        <lego-button main>Lorem</lego-button>
                    </ui-form-item>
                </ui-form-row>

            </ui-form-box>

            <ui-form-box class="mt20">

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Enter your keyword" searchable/>
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-segment-wrapper solid primary v-model="segmentValue">
                            <lego-segment-button value="1">Lorem</lego-segment-button>
                            <lego-segment-button value="2">Lorem</lego-segment-button>
                        </lego-segment-wrapper>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=10 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem Ipsum" />
                    </ui-form-item>
                    <ui-form-item :columns=7>
                        <lego-text-field v-model="textValue" placeholder="Lorem Ipsum" />
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=10 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem Ipsum" />
                    </ui-form-item>
                    <ui-form-item :columns=7>
                        <lego-text-field v-model="textValue" placeholder="Lorem Ipsum" />
                        <lego-button>Copy</lego-button>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=10 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem Ipsum" />
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=3 align-right margin-right>
                        <lego-button main>Lorem</lego-button>
                    </ui-form-item>
                </ui-form-row>

            </ui-form-box>

            <ui-form-box class="mt20">

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=5>
                        <lego-date-picker v-model="dateValue" />
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=9 label="Lorem ipsum dilor" :label-width=240>
                        <lego-radio v-model="radioValue" value="1">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="2">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="3">Lorem</lego-radio>
                        <lego-radio v-model="radioValue" value="4">Lorem Ipsum</lego-radio>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=6 label="Lorem Ipsum" required >
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                    </ui-form-item>
                    <ui-form-item :columns=12 align-right margin-right>
                        <lego-button main>Lorem</lego-button>
                    </ui-form-item>
                </ui-form-row>

            </ui-form-box>

            <ui-form-box class="mt20">
                <ui-form-row>
                    <ui-form-item :columns=8 label="Lorem Ipsum" required >
                        <lego-date-picker v-model="dateValue" />
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                    <ui-form-item :columns=9 label="Lorem Ipsum" required :label-width=320>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=7 label="Lorem Ipsum" required >
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=10 label="Lorem Ipsum" required :label-width=400>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-buttons divider>
                    <template v-slot:items>
                        <ui-form-row>
                            <ui-form-item :columns=18 label="Mechant" :label-width=148>
                                <lego-chip small removable>Seoul</lego-chip>
                                <lego-chip small removable>Paris</lego-chip>
                                <lego-chip small removable>Newyork</lego-chip>
                                <lego-chip small removable>London</lego-chip>
                                <lego-chip small removable>Budapest</lego-chip>
                            </ui-form-item>
                        </ui-form-row>
                        <ui-form-row>
                            <ui-form-item :columns=18 label="Store" :label-width=148>
                                <lego-chip small removable>Bixby</lego-chip>
                                <lego-chip small removable>Hotels.com</lego-chip>
                                <lego-chip small removable>Samsung Pay</lego-chip>
                                <lego-chip small removable>Kakao</lego-chip>
                                <lego-chip small removable>Hotels.com</lego-chip>
                                <lego-chip small removable>Samsung Pay</lego-chip>
                                <lego-chip small removable>Hotels.com</lego-chip>
                                <lego-chip small removable>Samsung Pay</lego-chip>
                                <lego-chip small removable>Bixby</lego-chip>
                                <lego-chip small removable>Kakao</lego-chip>
                                <lego-chip small removable>Samsung Pay</lego-chip>
                            </ui-form-item>
                        </ui-form-row>
                    </template>
                    <lego-button>Lorem</lego-button>
                    <lego-button main>Lorem</lego-button>
                </ui-form-buttons>

            </ui-form-box>

            <ui-form-box class="mt20">

                <ui-form-row>
                    <ui-form-item :columns=1 />
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=1 />
                    <ui-form-item :columns=6 label="Lorem Ipsum" required top-label>
                        <lego-date-picker v-model="dateValue" />
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                        <lego-text-field v-model="textValue" placeholder="Lorem" />
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=3 label="Lorem Ipsum" required top-label>
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>
                <ui-form-buttons divider>
                    <lego-button>Lorem</lego-button>
                    <lego-button main>Lorem</lego-button>
                </ui-form-buttons>

            </ui-form-box>

            <ui-form-box class="mt20">

                <ui-form-row>
                    <ui-form-item :columns=5 label="Patient Name" required-left>
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Primary ID Type">
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Primary ID">
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Contact No.">
                        <lego-text-field v-model="textValue" placeholder="Enter your keyword" searchable/>
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Name in English">
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                    <ui-form-item :columns=6 label="Gender" required-left>
                        <lego-segment-wrapper solid primary v-model="segmentValue">
                            <lego-segment-button value="1">Lorem</lego-segment-button>
                            <lego-segment-button value="2">Lorem</lego-segment-button>
                        </lego-segment-wrapper>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-row>
                    <ui-form-item :columns=5 label="Date of Birth" required-left>
                        <lego-date-picker v-model="dateValue" />
                    </ui-form-item>
                    <ui-form-item :columns=5 label="Age">
                        <lego-dropdown :items="items" v-model="value"/>
                    </ui-form-item>
                </ui-form-row>

                <ui-form-buttons divider>
                    <lego-button>Lorem</lego-button>
                    <lego-button main>Lorem</lego-button>
                </ui-form-buttons>

            </ui-form-box>

        </ui-container-box>

    </ui-page-box>
</template>

<script>
export default {
    name: 'sets-form',
    data: function() {
        return {
            value: 'A',
            dateValue: '',
            segmentValue: '2',
            radioValue: '1',
            textValue: ''
        }
    },
    computed : {
        items() {
            let rtn = [];
            rtn.push({value:'A',text:'Lorem Ipsum'});
            rtn.push({value:'B',text:'Lorem Ipsum'});
            return rtn;
        }
    }
}
</script>