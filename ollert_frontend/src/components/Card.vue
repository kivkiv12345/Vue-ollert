<script setup>
defineProps({
    name: {
        type: String,
        required: false,
    },
    row: {
        type: Number,
        required: true,
    },
    indent: {
        type: Number,
        required: true,
    },
    description: {
        type: String,
        required: false,
    }
})
</script>

<script>

export default {
    data() {
        return {
            "body_id": "card-" + this.row + "-" + this.indent,
        }
    },
    mounted() {
        let body = document.getElementById(this.body_id);
        body.addEventListener('mouseenter', this.mouseEnter);
        body.addEventListener('mouseleave', this.mouseLeft);
        body.addEventListener('mousedown', this.selectCard);
    },
    methods: {
        mouseEnter(pos) {
            // console.log(this.row + "-" + this.indent);
            this.$emit("mouseEntered", this.indent);
        },
        mouseLeft(pos) {
            this.$emit("mouseLeft", this.indent);
        },
        selectCard(pos) {
            this.$emit('selectCard', this.indent);
        },
    }
}
</script>

<template>
    <div class="body" v-bind:id="body_id">
        <h4 class="card-header">
            {{ name }}
        </h4>
        <p class="description">
            {{ this.row }}
            {{ this.indent }}
            {{ this.description }}

        </p>
    </div>
</template>

<style>
div.body {
    background-color: burlywood;
    border-radius: 5pt;
    min-height: 30pt;
    margin: 10pt;
    padding-top: 5px;
    padding-bottom: 5px;
}

.card-header {
    background-color: antiquewhite;
    border-radius: 5pt;
    padding: 5px;
    padding-left: 10pt;
    margin: 5px;
    margin-top: 1pt;
    margin-bottom: 0;
}

p.description {
    padding: 4pt;
    background-color: antiquewhite;
    border-radius: 5pt;
    margin: 5px;
    margin-bottom: 0;
    text-overflow: ellipsis;
}
</style>