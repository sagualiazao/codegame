<template>
<div class="map-square">
    <el-tabs ref="tabs" v-model="activeName" @tab-click="handleClick">
        <el-tab-pane :label="$store.state._const.MAP_SQUARE" name="first" class="map-square-tab">
            <div v-for="(map, index) in mapList">
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
                        <div v-if="map[5] === true">
                            <i class="el-icon-star-on" @click="changeFavor(map, false)" :title="$store.state._const.CLICK_TO_CANCEL_FAVORITE">
                                {{ $store.state._const.IS_FAVORITE }}
                            </i>
                        </div>
                        <div v-else>
                            <i class="el-icon-star-off" @click="changeFavor(map, true)" :title="$store.state._const.CLICK_TO_FAVORITE">
                                {{ $store.state._const.IS_NOT_FAVORITE }}
                            </i>
                        </div>
                    </div>
                </div>
            </div><br>
            <div class="page-block">
                <el-pagination @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentPage4"
                :page-sizes="[8, 10, 12, 16]"
                :page-size="8"
                layout="total, sizes, prev, pager, next, jumper"
                :total="100">
                </el-pagination>
            </div>
        </el-tab-pane>
        <el-tab-pane :label="$store.state._const.MY_PUBLISHED_MAPS" name="second" class="published-map-tab">
            <div v-for="map in publishedMapList">
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
            <div v-for="map in favoriteMapList">
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
            activeName: 'first',
            mapList: null,
            publishedMapList: null,
            favoriteMapList: null,
            currentPage4: 1
        }
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message(this.$store.state._const.LOGIN_FIRST)
                this.$router.push('/')
            } else {
                this.init()
            }
        } else {
            this.init()
        }
    },
    methods: {
        init: function () {
            this.readMapList()
            this.readFavoriteMapList()
            this.readPublishedMapList()
        },
        handleClick: function (tab, event) {},
        enterMap: async function (id) {
            this.$store.commit('changeLevelMode', false)
            let response = await readMap(false, id)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$store.commit('changeMap', obj)
                setCookie('levelMode', this.$store.state.levelMode.toString())
                setCookie('mapId', this.$store.state.mapId.toString())
                setCookie('mapString', this.$store.state.mapString)
                this.$router.push('/BlockBase')
            }
        },
        publishClick: function (map) {
            map[4] = false
            this.cancelPublishStatus(map[0])
        },
        changeFavor (map, status) {
            map[5] = status
            this.changeFavoriteMap(map[0], status)
        },
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
                this.$message(this.$store.state._const.LOAD_FAILURE)
            }
        },
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
                this.$message(this.$store.state._const.LOAD_FAILURE)
            }
        },
        readFavoriteMapList: async function () {
            let response = await simpleGet('api/read-favorite-map-list')
            let obj = await response.json()
            if (await obj.status === '1') {
                if (obj.number > 0) {
                    let list = JSON.parse(obj.data)
                    this.favoriteMapList = list
                    // 返回一个数组对象, for map in mapList
                    // map[0]: id 地图id
                    // map[1]: name 地图名称
                    // map[2]: author 地图作者
                    // map[3]: img 地图缩略图
                    // map[4]: remarks 地图说明
                }
            } else if (await obj.status === '0') {
                this.$message(this.$store.state._const.LOAD_FAILURE)
            }
        },
        changeFavoriteMap: async function (id, status) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            await simplePost('api/change-favorite', jsonObj)
            await this.$router.go(0)
            // await this.readMapList()
            // await this.readFavoriteMapList()
        },
        cancelPublishStatus: async function (id) {
            let jsonObj = {
                'mapid': id,
                'status': Number(status).toString()
            }
            await simplePost('api/change-publish', jsonObj)
            await this.readPublishedMapList()
            await this.readMapList()
        },
        handleSizeChange (val) {
            console.log(`每页 ${val} 条`)
        },
        handleCurrentChange (val) {
            console.log(`当前页: ${val}`)
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
