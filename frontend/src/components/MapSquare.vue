<template>
<div class="map-square">
    <el-tabs ref="tabs" v-model="activeName" @tab-click="handleClick">
        <el-tab-pane :label="$store.state._const.MAP_SQUARE" name="first" class="map-square-tab">
            <div class="page-block">
                <el-pagination
                :current-page.sync="currentPageAll"
                :page-size="8"
                layout="total, prev, pager, next"
                :total="totalMaps(mapList)">
                </el-pagination>
            </div>
            <div v-for="map in mapList" :key="map[0]" v-if="judgePage(map, mapList, currentPageAll)">
                <div class="map-picture">
                    <a @click="enterMap(map[0])"><img :src="map[3]" class="image" :alt="$store.state._const.WRONG_DISPLAY"></a>
                    <div class="caption">
                        <p class="mapname">
                            {{ $store.state._const.MAP_NAME }}: {{ map[1] }}
                        </p>
                        <p class="author">
                            {{ $store.state._const.MAP_AUTHOR }}: {{ map[2] }}
                        </p>
                        <p class="remarks">
                            {{ $store.state._const.MAP_REMARKS }}: {{ map[4] }}
                        </p>
                        <el-switch
                            @change="handleFavoriteSwitch(map)"
                            v-model="map[5]"
                            :on-text="$store.state._const.IS_FAVORITE"
                            :off-text="$store.state._const.IS_NOT_FAVORITE"
                            :width="80"
                        >
                        </el-switch>
                    </div>
                </div>
            </div><br>
        </el-tab-pane>
        <el-tab-pane :label="$store.state._const.MY_PUBLISHED_MAPS" name="second" class="published-map-tab">
            <div class="page-block">
                <el-pagination
                :current-page.sync="currentPagePublished"
                :page-size="8"
                layout="total, prev, pager, next"
                :total="totalMaps(publishedMapList)">
                </el-pagination>
            </div>
            <div v-for="map in publishedMapList" :key="map[0]" v-if="judgePage(map, publishedMapList, currentPagePublished)">
                <div class="map-picture">
                    <a @click="enterMap(map[0])"><img :src="map[2]" :alt="$store.state._const.WRONG_DISPLAY"></a>
                    <div class="caption">
                        <p class="mapname">
                            {{ $store.state._const.MAP_NAME }}: {{ map[1] }}
                        </p>
                        <p class="remarks">
                            {{ $store.state._const.MAP_REMARKS }}: {{ map[3] }}
                        </p>
                        <p>
                            <i class="el-icon-circle-check" @click="publishClick(map)" :title="$store.state._const.CLICK_TO_CANCEL_PUBLISH">
                                {{ $store.state._const.MAP_PUBLISHED }}
                            </i>
                        </p>
                    </div>
                </div>
            </div>
        </el-tab-pane>
        <el-tab-pane :label="$store.state._const.MY_FAVORITE_MAPS" name="third" class="favorite-map-tab">
            <div class="page-block">
                <el-pagination
                :current-page.sync="currentPageFavorite"
                :page-size="8"
                layout="total, prev, pager, next"
                :total="totalMaps(favoriteMapList)">
                </el-pagination>
            </div>
            <div v-for="map in favoriteMapList()" :key="map[0]" v-if="judgePage(map, favoriteMapList(), currentPageFavorite)">
                <div class="map-picture">
                    <a @click="enterMap(map[0])"><img :src="map[3]" class="image" :alt="$store.state._const.WRONG_DISPLAY"></a>
                    <div class="caption">
                        <p class="mapname">{{ $store.state._const.MAP_NAME }}: {{ map[1] }}</p>
                        <p class="author">{{ $store.state._const.MAP_AUTHOR }}: {{ map[2] }}</p>
                        <p class="remarks">{{ $store.state._const.MAP_REMARKS }}: {{ map[4] }}</p>
                        <i class="el-icon-star-on" @click="changeFavor(map, false)" :title="$store.state._const.CLICK_TO_CANCEL_FAVORITE">
                            {{ $store.state._const.IS_FAVORITE }}
                        </i>
                    </div>
                </div>
            </div>
        </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>
/**
* MapSqure 地图广场
*
* @class MapSqure
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import { simpleGet, simplePost, readMap, setCookie } from '@/assets/js/util.js'

export default {
    name: 'map-square',
    store: store,
    data: function () {
        return {
            /**
            *激活的界面
            *
            * @property activeName
            * @type {String}
            * @default 'first'
            */
            activeName: 'first',
            /**
            *所有地图列表
            *
            * @property mapList
            * @type {Object}
            * @default null
            */
            mapList: null,
            /**
            *已发布地图列表
            *
            * @property publishedMapList
            * @type {Object}
            * @default null
            */
            publishedMapList: null,
            /**
            *地图广场列表页码
            *
            * @property currentPage
            * @type {Number}
            * @default 1
            */
            currentPageAll: 1,
            /**
            *我发布的地图列表页码
            *
            * @property currentPage
            * @type {Number}
            * @default 1
            */
            currentPagePublished: 1,
            /**
            *我收藏的地图列表页码
            *
            * @property currentPage
            * @type {Number}
            * @default 1
            */
            currentPageFavorite: 1
        }
    },
    /**
    *
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
        *初始化函数, 读取所有地图, 收藏地图, 已发布地图
        *
        *@method init
        */
        init: function () {
            this.readMapList()
            this.readPublishedMapList()
        },
        /**
        *切换标签页
        * @method handleClick
        * @param {Object} tab 标签页
        * @param {Event} event 事件
        */
        handleClick: function (tab, event) {},
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
        *点击发布按钮的相应函数
        * @method publishClick
        * @param {Object} map
        * @param {Boolean} status
        */
        publishClick: function (map) {
            let i = this.publishedMapList.indexOf(map)
            this.publishedMapList.splice(i, i + 1)
            this.cancelPublishStatus(map[0])
        },
        /**
        *改变收藏状态
        * @method changeFavor
        * @param {Object} map
        * @param {Boolean} status
        */
        changeFavor (map, status) {
            map[5] = status
            this.changeFavoriteMap(map[0], status)
        },
        /**
        *读取数据库所有地图列表
        * @method readMyMapList
        */
        readMapList: async function () {
            let response = await simpleGet('api/read-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                if (obj.number > 0) {
                    let list = JSON.parse(obj.data)
                    this.mapList = list
                    // 返回一个数组对象, for map in mapList
                    // map[0]: id 地图id
                    // map[1]: name 地图名称
                    // map[2]: author 地图作者
                    // map[3]: img 地图缩略图
                    // map[4]: remarks 地图说明
                    // map[5]: favorite 收藏状态
                }
            } else if (await obj.status === '0') {
                this.$message.error(this.$store.state._const.LOAD_FAILURE)
            }
        },
        /**
        *读取数据库所有已发布地图列表
        * @method readPublishedMapList
        */
        readPublishedMapList: async function () {
            let response = await simpleGet('api/read-published-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                if (obj.number > 0) {
                    let list = JSON.parse(obj.data)
                    this.publishedMapList = list
                    // 返回一个数组对象, for map in mapList
                    // map[0]: id 地图id
                    // map[1]: name 地图名称
                    // map[2]: img 地图缩略图
                    // map[3]: remarks 地图说明
                    // map[4]: published 发布状态
                }
            } else if (await obj.status === '0') {
                this.$message.error(this.$store.state._const.LOAD_FAILURE)
            }
        },
        /**
        *更改数据库收藏地图列表
        * @method changeFavoriteMap
        */
        changeFavoriteMap: async function (id, status) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            simplePost('api/change-favorite', jsonObj)
        },
        /**
        *更改数据库发布地图列表
        * @method cancelPublishStatus
        */
        cancelPublishStatus: async function (id) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            await simplePost('api/change-publish', jsonObj)
            await this.readPublishedMapList()
            await this.readMapList()
        },
        /**
        *判断地图是否应该在当前页码中显示
        * @method judgePage
        * @param {Object} map
        * @param {Object} list
        * @param {Number} page
        */
        judgePage: function (map, list, page) {
            let i = list.indexOf(map)
            let begin = page * 8 - 8
            let end = page * 8
            if (begin <= i && i < end) {
                return true
            }
            return false
        },
        /**
        *计算制定列表的地图总数
        * @method totalMaps
        * @param {Object} list
        */
        totalMaps: function (list) {
            if (list === null) {
                return 0
            } else {
                return list.length
            }
        },
        /**
        *点击地图广场的收藏开关
        * @method handleFavoriteSwitch
        * @param {Object} map
        */
        handleFavoriteSwitch: function (map) {
            let id = map[0]
            let status = map[5]
            this.changeFavoriteMap(id, !status)
        },
        /**
        *返回收藏地图列表
        * @method favoriteMapList
        */
        favoriteMapList: function () {
            if (this.mapList === null) {
                return null
            } else {
                return this.mapList.filter(function (item) {
                    return item[5]
                })
            }
        }
    }
}
</script>

<style scoped>
h1 {
    font-weight: normal;
}
.el-icon-star-on {
    color: orange;
    cursor: pointer;
}
.el-icon-star-off {
    cursor: pointer;
}
.el-tab-pane {
    width: 100%;
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
.el-icon-circle-check {
    color:#FFA07A;
}
.el-pagination {
    vertical-align: center;
    position: absolute;
    bottom: 5%;
}
</style>
