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
                    { label:'LNB - Stack 03', linkto:'/template/LNBStack03', key:'LNBStack03', isSelected: false },
                    { label:'LNB - Stack 04', linkto:'/template/LNBStack04', key:'LNBStack04', isSelected: false },
                    { label:'LNB - Stack 05', linkto:'/template/LNBStack05', key:'LNBStack05', isSelected: false },
                    { label:'LNB - Stack 06', linkto:'/template/LNBStack06', key:'LNBStack06', isSelected: false },
                    { label:'LNB - Stack 07', linkto:'/template/LNBStack07', key:'LNBStack07', isSelected: false },
                    { label:'LNB - Stack 08', linkto:'/template/LNBStack08', key:'LNBStack08', isSelected: false },
                    { label:'LNB - Stack 09', linkto:'/template/LNBStack09', key:'LNBStack09', isSelected: false },
                    { label:'LNB - Stack 10', linkto:'/template/LNBStack10', key:'LNBStack10', isSelected: false },
                    { label:'LNB - Stack 11', linkto:'/template/LNBStack11', key:'LNBStack11', isSelected: false },
                  ]
                },
                
                { 
                  label: 'Split with LNB' ,
                  menus: [
                    { label:'LNB - Split 01', linkto:'/template/LNBSplit01', key:'LNBSplit01', isSelected: false },
                    { label:'LNB - Split 02', linkto:'/template/LNBSplit02', key:'LNBSplit02', isSelected: false },
                    { label:'LNB - Split 03', linkto:'/template/LNBSplit03', key:'LNBSplit03', isSelected: false },
                    { label:'LNB - Split 04', linkto:'/template/LNBSplit04', key:'LNBSplit04', isSelected: false },
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
                },

                { 
                  label: 'Stack' ,
                  menus: [
                    { label:'Stack 01', linkto:'/template/Stack01', key:'Stack01', isSelected: false },
                    { label:'Stack 02', linkto:'/template/Stack02', key:'Stack02', isSelected: false },
                    { label:'Stack 03', linkto:'/template/Stack03', key:'Stack03', isSelected: false },
                    { label:'Stack 04', linkto:'/template/Stack04', key:'Stack04', isSelected: false },
                    { label:'Stack 05', linkto:'/template/Stack05', key:'Stack05', isSelected: false },
                    { label:'Stack 06', linkto:'/template/Stack06', key:'Stack06', isSelected: false },
                    { label:'Stack 07', linkto:'/template/Stack07', key:'Stack07', isSelected: false },
                  ]
                },

                { 
                  label: 'Split' ,
                  menus: [
                    { label:'Split 01', linkto:'/template/Split01', key:'Split01', isSelected: false },
                    { label:'Split 02', linkto:'/template/Split02', key:'Split02', isSelected: false },
                    { label:'Split 03', linkto:'/template/Split03', key:'Split03', isSelected: false },
                    { label:'Split 04', linkto:'/template/Split04', key:'Split04', isSelected: false },
                  ]
                },

                {
                  label: 'Complex',
                  menus: [
                    { label:'Complex 01', linkto:'/template/Complex01', key:'Complex01', isSelected: false },
                    { label:'Complex 02', linkto:'/template/Complex02', key:'Complex02', isSelected: false },
                    { label:'Complex 03', linkto:'/template/Complex03', key:'Complex03', isSelected: false },
                  ]
                },

                { 
                  label:'Popup',
                  menus: [
                    { label:'Popup X-large', linkto:'/template/PopupXL', key:'PopupXL', isSelected: false },
                    { label:'Popup Large', linkto:'/template/PopupL', key:'PopupL', isSelected: false },
                    { label:'Popup Medium', linkto:'/template/PopupM', key:'PopupM', isSelected: false },
                    { label:'Popup Small', linkto:'/template/PopupS', key:'PopupS', isSelected: false },
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