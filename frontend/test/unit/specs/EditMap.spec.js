import Vue from 'vue'
import ElementUI from 'element-ui'
import EditMap from '@/components/EditMap'
import { createVue, destroyVM } from '../util'
Vue.use(ElementUI)

// 测试脚本里面应该包括一个或多个describe块，称为测试套件（test suite）
describe('EditMap', () => {
    // 每个describe块应该包括一个或多个it块，称为测试用例（test case）
    let vm

    beforeEach(() => {
        // 创建组件实例
        vm = createVue(EditMap, true)
    })

    afterEach(() => {
        // 清理组件
        destroyVM(vm)
    })

    it('should render correct contents', () => {
        expect(vm.$el.querySelector('.published h2').textContent).to.equal('已发布')
        expect(vm.$el.querySelector('.unpublished h2').textContent).to.equal('未发布')
        expect(vm.activeName === 'map-editor')
        expect(vm.$el.querySelector('.unpublished button').textContent).to.equal('发布地图')
    })

    // it('active-name,#handleClick', async () => {
    //     const paneList = vm.$el.querySelector('.el-tabs__content').children
    //     const tabList = vm.$refs.tabs.$refs.nav.$refs.tabs

    //     expect(tabList[0].classList.contains('is-active')).to.be.true
    //     expect(paneList[0].style.display).to.not.ok

    //     tabList[1].click()
    //     await vm.$nextTick(_ => {
    //         expect(tabList[1].classList.contains('is-active')).to.be.true
    //         expect(paneList[1].style.display).to.not.ok
    //         expect(vm.activeName === 'my-map')
    //     })
    // })
})


getSafeCommandString () {
    let safeCommandString = ''
    let commandList = this.getCommandCodeList()
    console.log(commandList)
    for (let i = 0; i < commandList.length; i++) {
        let safeCode = this.getSafeCode(commandList[i])
        console.log(safeCode)
        if (safeCode === false) {
            safeCommandString = ''
            alert('wrong input!')
            break
        } else {
            safeCommandString += safeCode
        }
    }
    console.log(safeCommandString)
    return safeCommandString
},
