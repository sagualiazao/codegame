// import Vue from 'vue'
// import ElementUI from 'element-ui'
// import MapSquare from '@/components/MapSquare'
// import { createVue, destroyVM } from '../util'

// Vue.use(ElementUI)

// describe('MapSquare.vue', () => {
//     let vm
//     // 在每个测试之前执行的
//     beforeEach(() => {
//         // 创建组件实例
//         vm = createVue(MapSquare, true)
//     })

//     afterEach(() => {
//         // 清理组件
//         destroyVM(vm)
//     })

//     it('sets the correct defaultData', () => {
//         expect(typeof MapSquare.data).to.equal('function')
//         const defaultData = MapSquare.data()
//         expect(defaultData.activeName).to.equal('first')
//     })

//     it('should render correct contents', () => {
//         expect(vm.$el.querySelector('.map-square-tab h1').textContent).to.equal('这是地图广场')
//         expect(vm.$el.querySelector('.published-map-tab h1').textContent).to.equal('这是我发布的地图')
//         expect(vm.$el.querySelector('.favorite-map-tab h1').textContent).to.equal('这是我收藏的地图')
//     })

//     it('active-name,#handleClick', done => {
//         vm = createVue(MapSquare, true)
//         setTimeout(_ => {
//             const paneList = vm.$el.querySelector('.el-tabs__content').children
//             const tabList = vm.$refs.tabs.$refs.nav.$refs.tabs

//             expect(tabList[0].classList.contains('is-active')).to.be.true
//             expect(paneList[0].style.display).to.not.ok

//             tabList[1].click()
//             vm.$nextTick(_ => {
//                 expect(tabList[1].classList.contains('is-active')).to.be.true
//                 expect(paneList[1].style.display).to.not.ok
//                 expect(vm.activeName === 'second')
//                 done()
//             })
//         }, 100)
//     })
// })
