<template>
    <ui-page-box align-center>

        <ui-container-box :columns=11 vertical class="mt50 mb50">

            <ui-list>
                <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=40 :height=40 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=80 :height=40 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item sub>Lorem Ipsum</ui-list-item>
                <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item header>
                    Lorem Ipsum is simply dummy text
                </ui-list-item>
                <ui-list-item body>
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the...
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=52 :height=52 />
                </template>
                <template v-slot:default>
                    <ui-list-item header fill-gap>
                        Lorem Ipsum is simply dummy text
                    </ui-list-item>
                    <ui-list-item body>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the...
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=104 :height=52 />
                </template>
                <template v-slot:default>
                    <ui-list-item header fill-gap>
                        Lorem Ipsum is simply dummy text
                    </ui-list-item>
                    <ui-list-item body>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the...
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
                <ui-list-item sub>
                    이진호<hr v/>
                    <lego-icon>display_password</lego-icon> 50<hr v/>
                    <lego-icon>recommend</lego-icon> 0<hr v/>
                    <lego-icon>comment</lego-icon> 3
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=52 :height=52 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=104 :height=52 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item sub>Lorem Ipsum</ui-list-item>
                <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                <ui-list-item sub>
                    이진호<hr v/>
                    <lego-icon>display_password</lego-icon> 50<hr v/>
                    <lego-icon>recommend</lego-icon> 0<hr v/>
                    <lego-icon>comment</lego-icon> 3
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item sub>Lorem Ipsum</ui-list-item>
                <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                <ui-list-item body>
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has...
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                <ui-list-item body>
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                </ui-list-item>
                <ui-list-item sub>
                    이진호<hr v/>
                    <lego-icon>display_password</lego-icon> 50<hr v/>
                    <lego-icon>recommend</lego-icon> 0<hr v/>
                    <lego-icon>comment</lego-icon> 3
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=80 :height=80 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body elipsis>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                    </ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=160 :height=80 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body elipsis>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                    </ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=72 :height=72 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item info>$ 000.00</ui-list-item>
                </template>
                <template v-slot:support>
                    <lego-button>Buy</lego-button>
                    <lego-button>Add Cart</lego-button>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=84 :height=84 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body elipsis>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                    </ui-list-item>
                    <ui-list-item info>$ 000.00</ui-list-item>
                </template>
                <template v-slot:support>
                    <lego-button>Buy</lego-button>
                    <lego-button>Add Cart</lego-button>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=112 :height=112 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body fill-gap>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown...
                    </ui-list-item>
                    <ui-list-item info>$ 000.00</ui-list-item>
                </template>
                <template v-slot:support>
                    <lego-button>Buy</lego-button>
                    <lego-button>Add Cart</lego-button>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                <ui-list-item body>
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                    industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=80 :height=80 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                        industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=160 :height=80 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been 
                        the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item sub>Lorem Ipsum</ui-list-item>
                <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                <ui-list-item body elipsis>
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                    industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                </ui-list-item>
                <ui-list-item sub>
                    이진호<hr v/>
                    <lego-icon>display_password</lego-icon> 50<hr v/>
                    <lego-icon>recommend</lego-icon> 0<hr v/>
                    <lego-icon>comment</lego-icon> 3
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                <ui-list-item body>
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
                    industry's standard dummy text ever since the 1500s, when an unknown printer took a galley...
                </ui-list-item>
                <ui-list-item sub>
                    이진호<hr v/>
                    <lego-icon>display_password</lego-icon> 50<hr v/>
                    <lego-icon>recommend</lego-icon> 0<hr v/>
                    <lego-icon>comment</lego-icon> 3
                </ui-list-item>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=108 :height=108 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer dummy text dummy te…
                    </ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=216 :height=108 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem 
                        Ipsum has been the industry's standard dummy text ever since the 1500s, when…
                    </ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <ui-list-file>
                    <template v-slot:filename>OPUS_mobile_guide.html</template>
                    <template v-slot:filesize>398</template>
                    <template v-slot:date>2019.02.21</template>
                </ui-list-file>
            </ui-list>

            <ui-list-group class="mt20">
                <ui-list v-for="count in list" :key="count">
                    <ui-list-file>
                        <template v-slot:filename>OPUS_mobile_guide.html</template>
                        <template v-slot:filesize>398</template>
                        <template v-slot:date>2019.02.21</template>
                    </ui-list-file>
                </ui-list>
            </ui-list-group>

            <ui-list class="mt20">
                <template v-slot:default>
                    <ui-list-item second>Lorem Ipsum</ui-list-item>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
                <template v-slot:support>
                    <ui-list-item icons>
                        <lego-icon small type="picto">slide_down</lego-icon>
                        <lego-icon small type="picto">more</lego-icon>
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=80 :height=80 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body elipsis>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been...</ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
                <template v-slot:support>
                    <ui-list-item icons>
                        <lego-icon small type="picto">slide_down</lego-icon>
                        <lego-icon small type="picto">more</lego-icon>
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:default>
                    <ui-list-item second>Lorem Ipsum</ui-list-item>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
                <template v-slot:support>
                    <ui-list-item icons>
                        <lego-icon small type="picto" style="transform: rotate(90deg);">collapse_menu</lego-icon>
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body elipsis>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                    </ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
                <template v-slot:support>
                    <ui-list-item icons>
                        <lego-icon small type="picto">expand_menu</lego-icon>
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list class="mt20">
                <template v-slot:thumbnail>
                    <ui-list-thumbnail :width=80 :height=80 />
                </template>
                <template v-slot:default>
                    <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                    <ui-list-item body elipsis>
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                    </ui-list-item>
                    <ui-list-item sub>
                        이진호<hr v/>
                        <lego-icon>display_password</lego-icon> 50<hr v/>
                        <lego-icon>recommend</lego-icon> 0<hr v/>
                        <lego-icon>comment</lego-icon> 3
                    </ui-list-item>
                </template>
                <template v-slot:support>
                    <ui-list-item sub>
                        5 minutes ago
                    </ui-list-item>
                </template>
            </ui-list>

            <ui-list-container class="mt20" >
                <ui-list-group title="Group01">
                    <ui-list v-for="count in list" :key="count">
                        <template v-slot:default>
                            <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                            <ui-list-item body elipsis>
                                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                            </ui-list-item>
                            <ui-list-item sub>
                                이진호<hr v/>
                                <lego-icon>display_password</lego-icon> 50<hr v/>
                                <lego-icon>recommend</lego-icon> 0<hr v/>
                                <lego-icon>comment</lego-icon> 3
                            </ui-list-item>
                        </template>
                    </ui-list>
                </ui-list-group>
                <ui-list-group title="Group02">
                    <ui-list v-for="count in list" :key="count">
                        <template v-slot:default>
                            <ui-list-item header>Lorem Ipsum is simply dummy text</ui-list-item>
                            <ui-list-item body elipsis>
                                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry...
                            </ui-list-item>
                            <ui-list-item sub>
                                이진호<hr v/>
                                <lego-icon>display_password</lego-icon> 50<hr v/>
                                <lego-icon>recommend</lego-icon> 0<hr v/>
                                <lego-icon>comment</lego-icon> 3
                            </ui-list-item>
                        </template>
                    </ui-list>
                </ui-list-group>
            </ui-list-container>

        </ui-container-box>

    </ui-page-box>
</template>

<script>
export default {
    name: 'gnb',
    data() {
        return {
            radioValue: '',
            checkValue: true,
            list: [1,2,3]
        }
    }
}
</script>