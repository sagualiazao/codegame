<template>
<div class="main-page">
    <h1>{{ msg }}</h1>
</div>
</template>

<script>
export default {
    name: 'main-page',
    data () {
        return {
            msg: '看到这行字，说明它正常了'
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
    font-weight: normal;
}

</style>
