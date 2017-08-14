import SigninForm from '@/components/SigninForm'

import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)
// import Router from 'vue-router'
// Vue.use(Router)

import { createVue, destroyVM } from '../util'

import Mock from 'mockjs'
import 'whatwg-fetch'

import { cbcDecrypt } from '@/assets/js/util'

// 为login定义了一个用户123456@qq.com, 123456
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

describe('signin-form', function () {
    let vm
    beforeEach(function () {
        vm = createVue(SigninForm, true)
    })

    afterEach(function () {
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

    it('获取DOM元素', function () {
        expect(vm.$el.querySelector('.demo-ruleForm .form-email-item').textContent).to.equal('邮箱')
        expect(vm.$el.querySelector('.demo-ruleForm .form-password-item').textContent).to.equal('密码')
        expect(vm.$el.querySelector('.demo-ruleForm .form-forget-password-item').textContent).to.equal('忘记密码')
        expect(vm.$el.querySelector('.demo-ruleForm .form-commit-item').textContent).to.equal('提交 重置')
    })

    it('vue组件挂载成功', function () {
        expect(vm.loginForm.email).to.equal('')
        expect(vm.loginForm.password).to.equal('')
    })

    it('#resetForm()', function () {
        vm.loginForm.email = '123456@qq.com'
        vm.loginForm.password = '111111'
        vm.resetForm('loginForm')
        expect(vm.loginForm.email).to.equal('')
        expect(vm.loginForm.password).to.equal('')
    })

    it('click reset-button', function () {
        vm.loginForm.email = '123456@qq.com'
        vm.loginForm.password = '111111'
        vm.$el.querySelector('.demo-ruleForm #reset-button').click()
        expect(vm.loginForm.email).to.equal('')
        expect(vm.loginForm.password).to.equal('')
    })

    it('#resetPasswordChange()', function () {
        vm.resetPasswordChange()
        expect(vm.$store.state.resetPasswordDialog).to.equal(true)
        expect(vm.$store.state.signinDialog).to.equal(false)
    })

    it('click reset-password-button', function () {
        vm.$el.querySelector('.demo-ruleForm #reset-password-button').click()
        expect(vm.$store.state.resetPasswordDialog).to.equal(true)
        expect(vm.$store.state.signinDialog).to.equal(false)
    })

    it('登录成功', async function () {
        vm.loginForm.email = '123456@qq.com'
        vm.loginForm.password = '123456'
        await vm.login()
        await expect(vm.$store.state.loginStatus).to.equal(true)
        await expect(vm.$store.state.userEmail).to.equal('123456@qq.com')
        await expect(vm.$store.state.userId).to.equal('001')
        await expect(vm.$store.state.userNickName).to.equal('123')
        await expect(vm.$store.state.userGameProgress).to.equal(0)
        await expect(vm.$store.state.userHasPaied).to.equal(false)
        await expect(vm.$store.state.signinDialog).to.equal(false)
        await expect(vm.$store.state.currentMenbar).to.equal('menu-bar-logged')
    })

    it('密码错误', async function () {
        vm.loginForm.email = '123456@qq.com'
        vm.loginForm.password = '111111'
        await vm.login()
        await expect(vm.$store.state.loginStatus).to.equal(false)
    })

    it('用户不存在', async function () {
        vm.loginForm.email = '111111@qq.com'
        vm.loginForm.password = '111111'
        await vm.login()
        await expect(vm.$store.state.loginStatus).to.equal(false)
    })

    // it('#submitForm("loginForm") 登录成功', async function () {
    //     vm.loginForm.email = '123456@qq.com'
    //     vm.loginForm.password = '123456'
    //     await vm.submitForm('loginForm')
    //     await expect(vm.$store.state.loginStatus).to.equal(true)
    //     await expect(vm.$store.state.userEmail).to.equal('123456@qq.com')
    //     await expect(vm.$store.state.userId).to.equal('001')
    //     await expect(vm.$store.state.userNickName).to.equal('123')
    //     await expect(vm.$store.state.userGameProgress).to.equal(0)
    //     await expect(vm.$store.state.userHasPaied).to.equal(false)
    //     await expect(vm.$store.state.signinDialog).to.equal(false)
    //     await expect(vm.$store.state.currentMenbar).to.equal('menu-bar-logged')
    // })

    it('#submitForm("loginForm") 表单填写错误,邮箱和密码为空', async function () {
        await vm.submitForm('loginForm')
    })

    it('#submitForm("loginForm") 表单填写错误,邮箱为空', async function () {
        vm.loginForm.email = '123456@qq.com'
        await vm.submitForm('loginForm')
    })

    it('#submitForm("loginForm") 表单填写错误,密码为空', async function () {
        vm.loginForm.password = '123456@qq.com'
        await vm.submitForm('loginForm')
    })

    it('#submitForm("loginForm") 表单填写错误,邮箱格式错误', async function () {
        vm.loginForm.password = '123456com'
        vm.loginForm.password = '123456'
        await vm.submitForm('loginForm')
    })

    it('#submitForm("loginForm") 表单填写错误,密码长度不足', async function () {
        vm.loginForm.email = '123456@qq.com'
        vm.loginForm.password = '12345'
        await vm.submitForm('loginForm')
    })
})
