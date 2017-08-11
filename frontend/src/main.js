// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import Router from 'vue-router'
import 'element-ui/lib/theme-default/index.css'
import Blockly from './blockly'
import MainPage from './components/MainPage'
import SelectLevel from './components/SelectLevel'
import BlockBase from './components/BlockBase'
import MapEditor from './components/MapEditor'
import MapSquare from './components/MapSquare'
import UserInfo from './components/UserInfo'
import EditorBase from './components/EditorBase.vue'
import EditMap from './components/EditMap'

global.Blockly = Blockly
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/',
            name: 'MainPage',
            component: MainPage
        },
        {
            path: '/SelectLevel',
            name: 'SelectLevel',
            component: SelectLevel
        },
        {
            path: '/BlockBase',
            name: 'BlockBase',
            component: BlockBase
        },
        {
            path: '/MapEditor',
            name: 'MapEditor',
            component: MapEditor
        },
        {
            path: '/MapSquare',
            name: 'MapSquare',
            component: MapSquare
        },
        {
            path: '/UserInfo',
            name: 'UserInfo',
            component: UserInfo
        },
        {
            path: '/EditorBase',
            name: 'EditorBase',
            component: EditorBase
        },
        {
            path: '/EditMap',
            name: 'EditMap',
            component: EditMap
        }
    ]
})
/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    template: '<App/>',
    components: { App }
})
