// 引入要测试的组件
import MenuBarLogged from '@/components/MenuBarLogged'
// 使用element的引入element
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
// 引入util的封装
import { createVue, destroyVM } from '../util'

describe('MenuBarLogged.vue', () => {
    let vm

    beforeEach(() => {
        vm = createVue(MenuBarLogged, true)
    })

    afterEach(() => {
        vm.$store.state.loginStatus = false
        vm.$store.state.userEmail = null
        vm.$store.state.userId = null
        vm.$store.state.userNickName = null
        vm.$store.state.userGameProgress = null
        vm.$store.state.userHasPaied = null
        vm.$store.state.registerDate = null
        vm.$store.state.currentMenbar = 'menu-bar-unlogged'
        vm.$store.state.textMainPage = 'mainPage'
        vm.$store.state.textGame = 'game'
        vm.$store.state.textMapEditor = 'mapEditor'
        vm.$store.state.textAccountMessage = 'accountMessage'
        vm.$store.state.signinDialog = false
        vm.$store.state.signupDialog = false
        vm.$store.state.resetPasswordDialog = false
        destroyVM(vm)
    })

    it('点击按钮注销', () => {
        let buttonElm = vm.$el.querySelector('.signout-button')
        buttonElm.click()
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(vm.$store.state.loginStatus).to.equal(false)
    })
})
