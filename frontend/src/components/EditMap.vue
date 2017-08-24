<template>
<div class="edit-map">
    <div id="map1">
        <el-tabs ref="tabs" v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane :label="$store.state._const.EDIT_MAP" name="map-editor">
                <map-editor></map-editor>
            </el-tab-pane>
            <el-tab-pane :label="$store.state._const.MY_DISIGNED_MAPS" name="my-map">
                <div class="page-block">
                    <el-pagination
                    :current-page.sync="currentPage"
                    :page-size="8"
                    layout="total, prev, pager, next"
                    :total="totalMaps()">
                    </el-pagination>
                </div>
                <div v-for="map in myMapList" :key="map[0]" v-if="judgePage(map)">
                    <div class="map-picture">
                        <a @click="enterMap(map[0])"><img :src="map[2]" :alt="$store.state._const.WRONG_DISPLAY"></a>
                        <div class="caption">
                            <p class="mapname">
                                {{ $store.state._const.MAP_NAME }}: {{ map[1] }}
                            </p>
                            <p class="remarks">
                                {{ $store.state._const.MAP_REMARKS }}: {{ map[3] }}
                            </p>
                        </div>
                        <el-switch
                            @change="handlePublishSwitch(map[4], map[0])"
                            v-model="map[4]"
                            :on-text="$store.state._const.MAP_PUBLISHED"
                            :off-text="$store.state._const.MAP_UNPUBLISHED"
                            :width="80"
                        >
                        </el-switch>
                        <i class="el-icon-delete" @click="deleteClick(map)">
                            {{ $store.state._const.DELETE_MAP }}
                        </i>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</div>
</template>


<script>
/**
* EditMap 组件中完成制作地图的功能
*
* @class EditMap
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import MapEditor from './MapEditor'
import { simpleGet, simplePost, readMap, setCookie } from '@/assets/js/util.js'

export default {
    name: 'edit-map',
    store: store,
    data: function () {
        return {
            /**
            *激活的界面
            *
            * @property activeName
            * @type {String}
            * @default 'map-editor'
            */
            activeName: 'map-editor',
            /**
            *我的地图列表
            *
            * @property myMapList
            * @type {Object}
            * @default null
            */
            myMapList: null,
            /**
            *我的地图列表页码
            *
            * @property currentPage
            * @type {Number}
            * @default 1
            */
            currentPage: 1
        }
    },
    components: {
        MapEditor
    },
    /**
    *vue组件的mounted函数, 判断登录状态, 调用初始化函数
    *
    *@method mounted
    */
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message({
                    message: this.$store.state._const.LOGIN_FIRST,
                    type: 'warning'
                })
                this.$router.push('/')
            } else {
                this.init()
            }
        } else {
            this.init()
        }
    },
    methods: {
        /**
        *初始化函数, 调用readMyMapList函数
        *
        *@method init
        */
        init: function () {},
        /**
        *切换标签页
        * @method handleClick
        * @param {Object} tab 标签页
        * @param {Event} event 事件
        */
        handleClick: function (tab, event) {
            if (this.activeName === 'my-map') {
                this.readMyMapList()
            }
        },
        /**
        *点击发布按钮的相应函数
        * @method publishClick
        * @param {Object} map
        * @param {Boolean} status
        */
        publishClick: function (map, status) {
            map[4] = status
            this.changePublishStatus(map[0], status)
        },
        /**
        *点击删除按钮的相应函数
        * @method deleteClick
        * @param {Object} map
        */
        deleteClick (map) {
            let i = this.myMapList.indexOf(map)
            let successMsg = this.$store.state._const.DELETE_SUCCESS
            let failureMsg = this.$store.state._const.DELETE_FAILURE
            let deleteMap = this.deleteMap
            let id = map[0]
            this.$confirm(
                this.$store.state._const.DELETE_CONFIRM_INFORMATION,
                this.$store.state._const.TIPS,
                {
                    confirmButtonText: this.$store.state._const.CONFIRM,
                    cancelButtonText: this.$store.state._const.CANCEL,
                    type: 'warning'
                }).then(() => {
                    this.myMapList.splice(i, 1)
                    deleteMap(id)
                    this.$message({
                        type: 'success',
                        message: successMsg
                    })
                }).catch(() => {
                    this.$message.error(failureMsg)
                })
        },
        /**
        *进入地图游戏界面
        * @method enterMap
        * @param {Number} id
        */
        enterMap: async function (id) {
            this.$store.commit('changeLevelMode', false)
            let response = await readMap(false, id)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$store.commit('changeMap', obj)
                setCookie('levelMode', this.$store.state.levelMode.toString())
                setCookie('mapId', obj.id.toString())
                setCookie('mapString', obj.map)
                setCookie('mapName', obj.name)
                setCookie('mapTips', obj.tips)
                setCookie('mapCodes', obj.codes)
                setCookie('mapMode', JSON.stringify(obj.mode))
                setCookie('mapAuthor', obj.author)
                this.$router.push('/BlockBase')
            }
        },
        /**
        *读取数据库地图列表
        * @method readMyMapList
        */
        readMyMapList: async function () {
            let response = await simpleGet('api/read-my-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                if (obj.number > 0) {
                    let list = JSON.parse(obj.data)
                    this.myMapList = list
                    // 返回一个数组对象, for map in mapList
                    // map[0]: id 地图id
                    // map[1]: name 地图名称
                    // map[2]: img 地图缩略图
                    // map[3]: remarks 地图说明
                    // map[4]: favorite 收藏发布状态
                }
            } else if (await obj.status === '0') {
                this.$message.error(this.$store.state._const.LOAD_FAILURE)
            }
        },
        /**
        *更改发布状态
        * @method changePublishStatus
        * @param {Number} id
        * @param {Boolean} status
        */
        changePublishStatus: async function (id, status) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            simplePost('api/change-publish', jsonObj)
        },
        /**
        *删除地图
        * @method deleteMap
        * @param {Number} id
        */
        deleteMap: async function (id) {
            let jsonObj = {
                'mapid': id
            }
            simplePost('api/delete-map', jsonObj)
        },
        /**
        *删除地图提示确认的响应函数
        * @method confirmDelete
        * @param {Number} id
        */
        confirmDelete: function (id) {

        },
        /**
        *判断地图是否应该在当前页码中显示
        * @method judgePage
        * @param {Object} map
        */
        judgePage: function (map) {
            let i = this.myMapList.indexOf(map)
            let begin = this.currentPage * 8 - 8
            let end = this.currentPage * 8
            if (begin <= i && i < end) {
                return true
            }
            return false
        },
        /**
        *计算地图总数
        * @method totalMaps
        */
        totalMaps: function () {
            if (this.myMapList === null) {
                return 0
            } else {
                return this.myMapList.length
            }
        },
        /**
        *点击发布开关的相应函数
        * @method handlePublishSwitch
        * @param {Boolean} status
        * @param {Number} id
        */
        handlePublishSwitch: function (status, id) {
            this.changePublishStatus(id, !status)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
h2 {
    color:#808000;
}
.edit-map {
    min-height: 800px;
}
div.map-picture {
    border: 1px solid #BFBFBF;
    text-align: center;
    float: left;
    width: 20%;
    height: auto;
    margin: 2%;
    display: block;
    /*box-sizing: border-box;*/
    overflow: hidden;
}
div.map-picture:hover {
    border: 1px solid #777;
}
.caption {
    text-align: center;
    font-weight: normal;
    width: 100%;
    font-size: 0.7em;
    margin: 10px 5px 10px 5px;
  }
  .map-picture a {
      display: block;
  }
  /*.map-picture a p {
      display: none;
      transform: scale(1);
  }*/
.map-picture img {
    width: 80%;
    height: auto;
    display: block;
    margin: 10%;
}
img {
    opacity: 0.8;
    filter: alpha(opacity = 40); /* For IE8 and earlier */
    transition: all 0.5s;
}
img:hover {
    opacity: 1.0;
    filter: alpha(opacity = 100); /* For IE8 and earlier */
    transform: scale(1.2);
    /*border: 1px solid #333333;*/
    /*box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);*/
    overflow: hidden;
}
@media only screen and (max-width: 700px){
    .map-picture {
        width: 49.99999%;
        margin: 6px 0;
    }
}
.el-icon-delete {
    float: right;
    margin-right: 2px;
    color: #4169E1;
    cursor: pointer;
}
button {
    display: inline-block;
    margin-top: 30px;
    margin-bottom: 10px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: white;
    background-color: #8FBC8F;
    border: none;
    border-radius: 15px;
    box-shadow: 5px 5px  5px #333;
}
button:hover {
    background-color: #D19275;
}
button:active {
    background-color: #D19275;
    box-shadow: 3px 5px #333;
    transform: translateY(4px);
}
.page-block {
    width: 100%;
}
.el-pagination {
    vertical-align: center;
    position: fixed;
    margin-left: 40%;
    bottom: 0px;
    z-index: 9999;
}
</style>
