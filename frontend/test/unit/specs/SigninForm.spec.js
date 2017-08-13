import SigninForm from '@/components/SigninForm'

import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)

import { createVue, destroyVM } from '../util'
// 引入这两个包来实现拦截request并作出响应
import Mock from 'mockjs'
import 'whatwg-fetch'

// 在这里定义拦截请求的方法
Mock.mock(
    'abc', // 要拦截的url
    'get', // 要拦截的请求方式
    { // 要返回的响应信息,也可以是有返回值的函数
        'status': '0'
    }
)

describe('signin-form', () => {
    let vm
    beforeEach(() => {
        vm = createVue(SigninForm, true)
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('mounted挂载成功', () => {
        expect(vm.loginForm.email).to.equal('')
        expect(vm.loginForm.password).to.equal('')
    })

    // 这是一个发送请求的测试
    it('request测试', async function () {
        let response = await fetch('abc')
        let obj = await response.json()
        await expect(obj.status).to.equal('0')
    })

    it('request之后的测试', function () {
        expect(vm.loginForm.password).to.equal('')
    })
})
