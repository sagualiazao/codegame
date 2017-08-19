<template>
<div class="map-square">
    <el-tabs ref="tabs" v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="地图广场" name="first" class="map-square-tab">
            <div v-for="map in mapList">
                <a href="">
                    <img src="" alt="mapp">
                </a>
                <!-- <map name="game-map" id="game-map">
                    <area shape="circle" coords="x, y, R" href="" alt="mapp" />
                </map> -->
                <div class="caption">
                    <p class="mapname">地图名</p>
                    <p class="author">作者</p>
                </div>
            </div>
            <button type="playMap" @click="playClick">试玩</button>
            <h1>这是地图广场</h1>
            <div v-if="isFavorite === false">
                <!-- <a href="#MapSquare" @click="changeFavor()"><i class="el-icon-star-off"></i>收藏</a> -->
                <i class="el-icon-star-off" @click="changeFavor" title="点击收藏地图">收藏</i>
            </div>
            <div v-else>
                <i class="el-icon-star-on" @click="changeFavor">已收藏</i>
            </div>
        </el-tab-pane>
        <el-tab-pane label="我发布的地图" name="second" class="published-map-tab">
            <div v-for="publishedMap in publishedMapList">
                <a href="">
                    <img src="" alt="mapp">
                </a>
                <div class="caption">
                    <p class="mapname">地图名</p>
                </div>
            </div>
            <h1>这是我发布的地图</h1>
        </el-tab-pane>
        <el-tab-pane label="我收藏的地图" name="third" class="favorite-map-tab">
            <div v-for="favoriteMap in favoriteMapList">
                <a href="">
                    <img src="" alt="mapp">
                </a>
                <div class="caption">
                    <p class="mapname">地图名</p>
                    <p class="author">作者</p>
                </div>
            </div>
            <h1>这是我收藏的地图</h1>
        </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>
export default {
    name: 'map-square',
    data: function () {
        return {
            msg: '看到这行字，说明它正常了',
            activeName: 'first',
            isFavorite: false
        }
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                alert('请先登录噢!')
                this.$router.push('/')
            } else {
                this.readMapList()
                this.readFavoriteMapList()
                this.readPublishedMapList()
            }
        } else {
            this.readMapList()
            this.readFavoriteMapList()
            this.readPublishedMapList()
        }
    },
    methods: {
        handleClick (tab, event) {
        },
        playClick () {
        },
        collect () {
        },
        changeFavor () {
            if (this.isFavorite === true) {
                this.isFavorite = false
            } else {
                this.isFavorite = true
            }
        },
        readMapList: async function () {
            let response = await fetch('api/read-mapList', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
            let obj = await response.json()
            if (await obj.status === '1') {
//
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        readPublishedMapList: async function () {
            let response = await fetch('api/read-publishedMapList', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
            let obj = await response.json()
            if (await obj.status === '1') {
//
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        readFavoriteMapList: async function () {
            let response = await fetch('api/read-favoriteMapList', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
            let obj = await response.json()
            if (await obj.status === '1') {
//
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        }
    },
    compute: {
        mapList: function () {
            return this.readMapList()
        },
        publishedMapList: function () {
            return this.readPublishedMapList()
        },
        favoriteMapList: function () {
            return this.readFavoriteMapList()
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
.el-icon-star-on {
    color: orange;
}
img {
    width: 300px;
    height: 200px;
}
img {
    opacity: 0.4;
    filter: alpha(opacity = 40); /* For IE8 and earlier */
}
img:hover {
    opacity: 1.0;
    filter: alpha(opacity = 100); /* For IE8 and earlier */
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
</style>
