<template>
  <div>
      <ui-gnb style="position: fixed; width: 100%; z-index:999;">
          <template v-slot:lead>
              <ui-gnb-menus :menus="menus">
                <template v-slot="{ menu }" >
                  <div class="template-type">
                    <div class="template-type__label">{{menu.label}}</div>
                    <div class="template-type__menus">
                      <router-link v-for="item in menu.menus" 
                        :key="item.key" :to="item.linkto"
                        :class="[
                          { 'template-type__menus-item' : true },
                          { 'template-type__menus-item--selected' : item.isSelected }
                        ]"
                      >
                        {{item.label}}
                      </router-link>
                    </div>
                  </div>
                </template>
              </ui-gnb-menus>
          </template>
      </ui-gnb>
      
      <router-view class="pt80 pb80" />

  </div>
</template>

<script>
export default {
    data() {
        return {
            menus: [
                { 
                  label: 'Stack with LNB' ,
                  menus: [
                    { label:'LNB - Stack 01', linkto:'/template/LNBStack01', key:'LNBStack01', isSelected: false },
                    { label:'LNB - Stack 02', linkto:'/template/LNBStack02', key:'LNBStack02', isSelected: false },                    
                  ]
                },
                
                { 
                  label: 'Split with LNB' ,
                  menus: [
                    { label:'LNB - Split 01', linkto:'/template/LNBSplit01', key:'LNBSplit01', isSelected: false },
                    { label:'LNB - Split 02', linkto:'/template/LNBSplit02', key:'LNBSplit02', isSelected: false },                  
                  ]
                },

                { 
                  label: 'Complex with LNB' ,
                  menus: [
                    { label:'LNB - Complex 01', linkto:'/template/LNBComplex01', key:'LNBComplex01', isSelected: false },
                    { label:'LNB - Complex 02', linkto:'/template/LNBComplex02', key:'LNBComplex02', isSelected: false },
                    { label:'LNB - Complex 03', linkto:'/template/LNBComplex03', key:'LNBComplex03', isSelected: false },
                    { label:'LNB - Complex 04', linkto:'/template/LNBComplex04', key:'LNBComplex04', isSelected: false },
                  ]
                }                
            ]
        }
    },
    watch: {
      '$route' (to, from) {
        this.menus.forEach(function(menu){
          menu.menus.forEach(function(item){
            item.isSelected = (to.path.includes(item.linkto));
          })
        })
      }
    }
}
</script>

<style lang="scss" scoped>
.template-type {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.template-type__menus {
  position: absolute;
  display: none;
  top: 70px;
  left: 0;
  width: 200px;

  flex-flow: column nowrap;
  background-color: white;
  border: 1px solid #CCCCCC;
}
.template-type:hover .template-type__menus {
  display: flex;
}
.template-type__menus-item {
  padding: 16px 24px;
}
.template-type__menus-item:hover {
  cursor: pointer;
  background-color: #F7F7F7;
}
.template-type__menus-item--selected {
  background: #F7F5FB;
  font-weight: bold;
  color: #553CA5;
}

</style>