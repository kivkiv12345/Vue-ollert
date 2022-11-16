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
    },
    isSelectedList: {
        type: Boolean,
        required: true,
    },
    selectedCard: {
        type: Number,
        required: false
    },
    movingCard: {
        type: Number,
        required: false
    },
    isMovingList: {
        type: Boolean,
        required: true,
    }
})
</script>
<script>
import Card from './Card.vue';
export default {
    mounted() {
        document.getElementById('list-' + this.indent).addEventListener('mouseenter', this.mouseEnteredList)
        document.getElementById('list-' + this.indent).addEventListener('mouseleave', this.mouseLeftList);

        console.log(this.indent)

        console.log(this.items);
    },
    methods: {
        mouseEnteredCard(row) {
            this.$emit("mouseEntered", row, true);
        },
        mouseEnteredList() {
            this.$emit("mouseEntered", this.indent, false);
        },
        mouseLeftCard(row) {
            //                              true if we have left a card false if we have left a list
            this.$emit("mouseLeft", row, true);
        },
        mouseLeftList() {
            this.$emit("mouseLeft", this.list, false)
        },
        selectCard(row) {
            this.$emit('selectCard', this.indent, row);
        },
    }
}
</script>

<template>
    <!-- <p v-if="isSelectedList">
        {{ isSelectedList }}
    </p> -->
    <div class="task-body" v-bind:id="'list-' + indent">
        <h2 class="list-header">
            {{ name }}
        </h2>
        <div class="items unselectable">
            <Card v-for="x, i in items" :name="x.name" :indent="i" :row="indent" :description="x.description"
                :selected="isSelectedList && i == selectedCard && !isNaN(movingCard)"
                :moving="!isNaN(movingCard) && movingCard == i && isMovingList" @mouse-entered="mouseEnteredCard"
                :order="x.order" @mouse-left="mouseLeftCard" @select-card="selectCard">

            </Card>
            <div class="body body-color" v-if="isSelectedList && isNaN(selectedCard) && !isNaN(movingCard)">

            </div>
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