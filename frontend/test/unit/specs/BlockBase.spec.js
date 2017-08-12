import Vue from 'vue'
import BlockBase from '@/components/BlockBase'
import { createVue, destroyVM } from '../util'

describe('BlockBase.vue', () => {
    it('expect the tween to be 2', () => {
        expect(typeof BlockBase.data).to.equal('function')
        const defaultData = BlockBase.data()
        expect(defaultData.tween).to.equal(null)
    })

    it('correctly sets the message when created', () => {
        const vm = new Vue(BlockBase).$mount()
        const defaultData = BlockBase.data()
        expect(defaultData.tween).to.equal(null)
    })
})

describe('blockly', () => {
    let vm
    afterEach(() => {
        destroyVM(vm)
    })

    it('blockly的mounted挂载成功', () => {
        vm = createVue(BlockBase, true)
        expect(vm.direct).to.equal(2)
        expect(vm.workspace).to.exit
    })
})
