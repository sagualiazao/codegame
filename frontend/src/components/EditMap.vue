<template>
<div class="edit-map">
    <div id="map1">
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane label="制作地图" name="first">
                <div class="map-scene" @drop="drop($event)" @dragover="allowDrop($event)">地图</div>
                <div class="materials" @drop="drop($event)" @dragover="allowDrop($event)">素材库
                    <img src="../assets/logo.png" draggable="true" @dragstart="drag($event)" id="drag1">
                    <img src="../assets/timg.jpeg" draggable="true" @dragstart="drag($event)" id="drag2">
                    <img src="../assets/mat1.jpg" draggable="true" @dragstart="drag($event)" id="drag3">
                    <img src="../assets/mat2.jpeg" draggable="true" @dragstart="drag($event)" id="drag4">
                    <img src="../assets/mat3.jpg" draggable="true" @dragstart="drag($event)" id="drag5">
                    <img src="../assets/mat4.jpg" draggable="true" @dragstart="drag($event)" id="drag6">
                    <img src="../assets/mat5.jpg" draggable="true" @dragstart="drag($event)" id="drag7">
                    <img src="../assets/mat6.jpg" draggable="true" @dragstart="drag($event)" id="drag8">
                    <img src="../assets/mat7.jpg" draggable="true" @dragstart="drag($event)" id="drag9">
                    <img src="../assets/mat8.jpg" draggable="true" @dragstart="drag($event)" id="drag10">
                    <img src="../assets/mat9.jpg" draggable="true" @dragstart="drag($event)" id="drag11">
                </div>
                <button type="save-map" @click="saveClick">保存地图</button>
                <h1>在这里创建地图</h1>
            </el-tab-pane>
            <el-tab-pane label="我做的地图" name="second">
                <div class="published">
                    <h2>已发布</h2>
                    <img src="../assets/pc5.jpg">
                    <img src="../assets/pc8.jpg">
                    <img src="../assets/pc10.jpg">
                </div>
                <div class="unpublished">
                    <h2>未发布</h2>
                    <img src="../assets/pc13.jpg">
                    <img src="../assets/pc14.jpg">
                    <img src="../assets/pc15.jpg">
                    <img src="../assets/pc16.jpg">
                    <img src="../assets/pc17.jpg">
                    <img src="../assets/pc18.jpg">
                    <button type="publish-map" @click="publishClick">发布地图</button>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</div>
</template>

<script>
export default {
    name: 'edit-map',
    data: function () {
        return {
            activeName: 'first',
            activeIndex: 'published',
            msg: '看到这行字，说明它正常了'
        }
    },
    methods: {
        handleClick (tab, event) {
            console.log(tab, event)
        },
        allowDrop: function (event) {
            event.preventDefault()
        },
        drag: function (event) {
            event.dataTransfer.setData('Text', event.target.id)
        },
        drop: function (event) {
            event.preventDefault()
            var da = event.dataTransfer.getData('Text')
            event.target.appendChild(document.getElementById(da))
        },
        saveClick () {
            // 这里保存地图
        },
        publishClick () {
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
.published img, .unpublished img {
    width: 400px;
    height: 300px;
}
#map1 {
    margin-top: -25px;
}
.map-scene, .materials {
    display: inline;
}
.map-scene img, .materials img {
    width: 70px;
    height: 60px;
}
.map-scene {
    float: left;
    width: 580px;
    height: 500px;
    background-color: #98FB98;
    border:2px solid #ADD8E6;
}
.materials {
    float: right;
    width: 580px;
    height: 500px;
    background-color: #FFDEAD;
    border: 2px solid #F0E68C;
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
