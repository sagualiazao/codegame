import SelectLevel from '@/components/SelectLevel'
import { createVue, destroyVM } from '../util'
import ElementUI from 'element-ui'
Vue.use(ElementUI)

describe('SelectLevel.vue', () => {
    let vm
    beforeEach(() => {
        vm = createVue(SelectLevel, true)
    })

    afterEach(() => {
        destroyVM(vm)
    })

    it('点击继续游戏按钮', () => {
        // TODO 点击继续游戏按钮切换到游戏界面
    })

})
