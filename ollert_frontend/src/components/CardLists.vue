<script setup>
defineProps({
    name: {
        type: String,
        required: true,
    },
    items: {
        type: Array,
        required: true
    },
    indent: {
        type: Number,
        required: true
    }
})
</script>
<script>
import Card from './Card.vue';
export default {
    mounted() {
        // document.getElementById('list-' + this.indent).addEventListener('mousemove', (pos) => console.log(this.indent + ":" + pos))
        console.log(this.indent)
    },
    methods: {
        mouseEntered(list, row) {
            this.$emit("mouseEntered", list, row);
        },
        mouseLeft(list, row) {
            this.$emit("mouseLeft", list, row);
        },
        selectCard(list, row) {
            this.$emit('selectCard', list, row);
        },
    }
}
</script>

<template>
    <div class="task-body" v-bind:id="'list-' + this.indent">
        <h2 class="list-header">
            {{ name }}
        </h2>
        <div class="items">
            <Card v-for="x, i in items" :name="x.name" :indent="i" :row="indent" @mouse-entered="mouseEntered"
                @mouse-left="mouseLeft" @select-card="selectCard" class="unselectable">

            </Card>
        </div>
    </div>
</template>
<style>
.list-header {
    background-color: burlywood;
    border-radius: 10pt;
    padding: 5px;
    padding-left: 10pt;
    margin-top: 1pt;
}

div.task-body {
    background-color: antiquewhite;
    width: 200px;
    min-height: 100px;
    border-radius: 10px;
    padding: 2pt;
    margin: 10pt 1pt;
}

*.unselectable {
    -moz-user-select: -moz-none;
    -khtml-user-select: none;
    -webkit-user-select: none;

    /*
     Introduced in IE 10.
     See http://ie.microsoft.com/testdrive/HTML5/msUserSelect/
   */
    -ms-user-select: none;
    user-select: none;
}
</style>