import Vue from 'vue'
import ResetPasswordForm from '@/components/ResetPasswordForm'
import ElementUI from 'element-ui'

Vue.use(ElementUI)

import { createVue, destroyVM } from '../util'
// 引入这两个包来实现拦截request并作出响应
import Mock from 'mockjs'
import 'whatwg-fetch'

import { cbcDecrypt } from '@/assets/js/util'

Mock.mock(
    'api/login',
    'post',
    function (request) {
        let json = JSON.parse(request.body)
        console.log(json.email)
        console.log(json.captcha)
        console.log(json.password)
        if (json.email === '123456@qq.com') {
            let keyStr = json.captcha
            let crypted = json.password
            let password = cbcDecrypt(keyStr, crypted)
            console.log(password)
            if (password === '123456') {
                return {
                    status: '1',
                    email: '123456@qq.com',
                    id: '001',
                    nickname: '123',
                    gameProgress: 0,
                    hasPaied: false,
                    createdAt: '2017-01-01'
                }
            } else {
                return {
                    status: '0'
                }
            }
        } else {
            return {
                status: '0'
            }
        }
    }
)

describe('ResetPasswordForm.vue',() => {
	let vm
    beforeEach(() => {
        vm = createVue(SigninForm, true)
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

    it('store挂载成功', function () {
    	expect(vm.$store.state.loginStatus).to.equal(false)
        expect(vm.$store.state.userEmail).to.equal(null)
        expect(vm.$store.state.userId).to.equal(null)
        expect(vm.$store.state.userNickName).to.equal(null)
        expect(vm.$store.state.userGameProgress).to.equal(null)
        expect(vm.$store.state.userHasPaied).to.equal(null)
        expect(vm.$store.state.registerDate).to.equal(null)
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(vm.$store.state.textMainPage).to.equal('mainPage')
        expect(vm.$store.state.textGame).to.equal('game')
        expect(vm.$store.state.textMapEditor).to.equal('mapEditor')
        expect(vm.$store.state.textAccountMessage).to.equal('accountMessage')
        expect(vm.$store.state.signinDialog).to.equal(false)
        expect(vm.$store.state.signupDialog).to.equal(false)
        expect(vm.$store.state.resetPasswordDialog).to.equal(false)

    })

    it('vue组件挂载成功', function () {
    	expect(vm.ResetPasswordForm.email).to.equal('')
    	expect(vm.ResetPasswordForm.password).to.equal('')
    	expect(vm.ResetPasswordForm.checkPassword).to.equal('')
    })

    it('resetForm函数', function () {
    	vm.ResetPasswordForm.email = '11111@qq.com'
    	vm.ResetPasswordForm.password = '111111'
    	vm.ResetPasswordForm.checkPassword = '111111'
    	vm.resetForm('ResetPasswordForm')
        expect(vm.ResetPasswordForm.email).to.equal('')
    	expect(vm.ResetPasswordForm.password).to.equal('')
    	expect(vm.ResetPasswordForm.checkPassword).to.equal('')
    })

    it('click reset-button', function () {
    	vm.ResetPasswordForm.email = '11111@qq.com'
    	vm.ResetPasswordForm.password = '111111'
    	vm.ResetPasswordForm.checkPassword = '111111'
    	vm.$el.querySelector('.demo-dynamic #reset-btn').click()
        expect(vm.ResetPasswordForm.email).to.equal('')
    	expect(vm.ResetPasswordForm.password).to.equal('')
    	expect(vm.ResetPasswordForm.checkPassword).to.equal('')
    })

    it('countTime', function () {
    	vm.countTime()
    	expect(vm.sendEmialDisabled).not.to.be.ok
    })
})